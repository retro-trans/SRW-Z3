"""Build a CFW-only hardware-test ISO from a validated RPCS3 snapshot.

Dry-run by default; --write requires a new output directory. Nothing is installed.
Uses a locally compiled PSL1GHT fself (see CFW_TEST.md) and pycdlib 1.15.0.
No signing keys, licenses or game files are downloaded or published.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from isoread import ISO9660
from iso_patch import Iso, shipped_paths

SECTOR = 2048
BLOCK = 4 << 20
SPLIT = 2 << 30  # sector aligned, comfortably below FAT32's per-file limit
SOURCE_MD5 = "2cfedd95e5bdde49550cffa21c3c29a3"
SOURCE_SIZE = 4431872000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path, algorithm="sha256"):
    h = hashlib.new(algorithm)
    with Path(path).open("rb") as stream:
        for data in iter(lambda: stream.read(BLOCK), b""):
            h.update(data)
    return h.hexdigest()


def bounded_hash(stream, offset, length):
    stream.seek(offset)
    h = hashlib.sha256()
    while length:
        data = stream.read(min(length, BLOCK))
        require(data, "Unexpected EOF during verification")
        h.update(data)
        length -= len(data)
    return h.hexdigest()


def safe_relative(name):
    path = Path(name.lstrip("/"))
    require(not path.is_absolute() and ".." not in path.parts and
            ":" not in name and "\\" not in name, "Unsafe archive path: " + name)
    return path


def control_records(data):
    require(data[:4] == b"SCE\0", "Expected SELF, not plain ELF")
    offset, size = struct.unpack_from(">QQ", data, 0x58)
    end = offset + size
    require(end <= len(data), "Control table outside SELF")
    result = {}
    while offset < end:
        kind, length, more = struct.unpack_from(">IIQ", data, offset)
        require(length >= 16 and offset + length <= end and kind not in result,
                "Invalid or duplicate SELF control record")
        result[kind] = (offset, length)
        offset += length
        require(bool(more) == (offset < end), "Invalid control record chain")
    return result


def elf_headers(data):
    require(data[:6] == b"\x7fELF\x02\x02" and len(data) >= 64,
            "Expected big-endian ELF64")
    kind, machine = struct.unpack_from(">HH", data, 16)
    require(kind == 2 and machine == 21, "Expected PS3 PPU executable")
    phoff = struct.unpack_from(">Q", data, 32)[0]
    ehsize, phsize, phnum = struct.unpack_from(">HHH", data, 52)
    require(ehsize == 64 and phsize == 56 and 0 < phnum < 64 and
            phoff + phnum * phsize <= len(data), "Invalid ELF program table")
    headers = [struct.unpack_from(">IIQQQQQQ", data, phoff + i * phsize)
               for i in range(phnum)]
    for typ, flags, offset, va, pa, filesz, memsz, align in headers:
        require(offset + filesz <= len(data), "ELF segment extends beyond file")
        if typ == 1:
            require(memsz >= filesz, "LOAD segment memory too small")
    return phoff, headers


def retain_application_metadata(wrapped, original):
    """Keep retail auth/vendor/type/version and capabilities, not signatures."""
    result = bytearray(wrapped)
    dst = struct.unpack_from(">Q", result, 0x28)[0]
    src = struct.unpack_from(">Q", original, 0x28)[0]
    require(dst + 32 <= len(result) and src + 32 <= len(original), "Invalid APP_INFO")
    result[dst:dst + 32] = original[src:src + 32]
    old = control_records(original)[1]
    new = control_records(result)[1]
    require(old[1] == new[1] == 48, "Unexpected capability record length")
    result[new[0] + 16:new[0] + 48] = original[old[0] + 16:old[0] + 48]
    return bytes(result)


def verify_self(wrapped, elf, original):
    phoff, headers = elf_headers(elf)
    require(wrapped[:4] == b"SCE\0", "EBOOT is not a SELF")
    require(struct.unpack_from(">IHH", wrapped, 4) == (2, 0x8000, 1),
            "Expected CFW fake-SELF header")
    payload, size = struct.unpack_from(">QQ", wrapped, 16)
    require(size == len(elf) and len(wrapped) == payload + size,
            "SELF payload size mismatch")
    require(wrapped[payload:] == elf, "SELF changed executable payload")
    eoff, poff = struct.unpack_from(">QQ", wrapped, 0x30)
    require(wrapped[eoff:eoff + 64] == elf[:64], "Embedded ELF header differs")
    require(wrapped[poff:poff + 56 * len(headers)] == elf[phoff:phoff + 56 * len(headers)],
            "SELF program headers differ")
    section = struct.unpack_from(">Q", wrapped, 0x48)[0]
    for i, header in enumerate(headers):
        offset, length, comp, zero1, zero2, enc = struct.unpack_from(">QQIIII", wrapped, section + i * 32)
        require((offset, length, comp, zero1, zero2, enc) ==
                (payload + header[2], header[5], 1, 0, 0, 2 if header[0] == 1 else 0),
                "SELF segment mapping mismatch")
    dst = struct.unpack_from(">Q", wrapped, 0x28)[0]
    src = struct.unpack_from(">Q", original, 0x28)[0]
    require(wrapped[dst:dst + 32] == original[src:src + 32], "APP_INFO changed")
    require(struct.unpack_from(">I", wrapped, dst + 12)[0] == 4, "Not a disc application SELF")
    controls = control_records(wrapped)
    oldcap, cap = control_records(original)[1][0], controls[1][0]
    require(wrapped[cap + 16:cap + 48] == original[oldcap + 16:oldcap + 48], "Capabilities changed")
    d = controls[2][0]
    require(wrapped[d + 36:d + 56] == hashlib.sha1(elf).digest(), "SELF digest mismatch")
    return {"format": "CFW fake SELF (not retail-signed)", "program_segments": len(headers),
            "payload_sha256": hashlib.sha256(elf).hexdigest(), "payload_byte_identical": True}


def stamp_disc(path):
    """PS3 plaintext ranges per ps3netsrv VIsoFile::write, one whole-disc range."""
    path = Path(path)
    require(path.stat().st_size % SECTOR == 0, "Non-sector-aligned ISO")
    sectors = path.stat().st_size // SECTOR
    # Match the conservative 32-sector tail padding used by ps3netsrv.
    padding = 32 + (-sectors % 32)
    sectors += padding
    with path.open("r+b") as stream:
        stream.seek(0, 2)
        stream.write(bytes(padding * SECTOR))
        system = bytearray(16 * SECTOR)
        struct.pack_into(">IIII", system, 0, 1, 0, 0, sectors - 1)
        system[SECTOR:SECTOR + 12] = b"PlayStation3"
        system[SECTOR + 16:SECTOR + 48] = b"BLJS-10256".ljust(32, b" ")
        stream.seek(0)
        stream.write(system)
        for lba in range(16, 32):
            stream.seek(lba * SECTOR)
            descriptor = stream.read(SECTOR)
            require(descriptor[1:6] == b"CD001", "Unexpected ISO descriptor")
            if descriptor[0] == 255:
                break
            if descriptor[0] in (1, 2):
                stream.seek(lba * SECTOR + 80)
                stream.write(struct.pack("<I", sectors) + struct.pack(">I", sectors))


def verify_disc_header(path):
    sectors = Path(path).stat().st_size // SECTOR
    with Path(path).open("rb") as stream:
        system = stream.read(16 * SECTOR)
        require(struct.unpack_from(">IIII", system) == (1, 0, 0, sectors - 1), "Stale disc ranges")
        require(system[SECTOR:SECTOR + 12] == b"PlayStation3", "Missing PS3 identifier")
        require(system[SECTOR + 16:SECTOR + 26] == b"BLJS-10256", "Wrong disc title ID")
        require(system[0xF70:0x1000] == bytes(0x90), "Stale disc encryption marker")
        iso = Iso(stream)
        require(len(iso.trees) == 2, "Expected primary and Joliet trees")
        for lba in range(16, 32):
            stream.seek(lba * SECTOR)
            descriptor = stream.read(SECTOR)
            require(descriptor[1:6] == b"CD001", "Invalid volume descriptor")
            if descriptor[0] == 255:
                break
            if descriptor[0] not in (1, 2):
                continue
            stream.seek(lba * SECTOR + 80)
            v = stream.read(8)
            require(struct.unpack("<I", v[:4])[0] == sectors == struct.unpack(">I", v[4:])[0],
                    "Volume length mismatch")
    return {"plaintext_regions": 1, "sectors": sectors, "encrypted_regions": 0}


def split_iso(source, directory, chunk_size=SPLIT):
    require(0 < chunk_size < 2**32 and chunk_size % SECTOR == 0, "Invalid FAT32 split size")
    source, directory = Path(source), Path(directory)
    require(not list(directory.glob(source.name + ".*")), "Existing split parts; refusing overwrite")
    parts = []
    with source.open("rb") as src:
        left = source.stat().st_size
        while left:
            part = directory / (source.name + "." + str(len(parts)))
            size = min(left, chunk_size)
            with part.open("xb") as out:
                remaining = size
                while remaining:
                    data = src.read(min(remaining, BLOCK))
                    require(data, "Unexpected EOF splitting ISO")
                    out.write(data)
                    remaining -= len(data)
            parts.append({"name": part.name, "bytes": size, "sha256": digest(part)})
            left -= size
    return parts


def verify_parts(source, directory, parts):
    joined = hashlib.sha256()
    for part in parts:
        path = Path(directory) / part["name"]
        require(path.stat().st_size == part["bytes"] < 2**32, "Invalid split file length")
        require(digest(path) == part["sha256"], "Split part changed")
        with path.open("rb") as stream:
            for data in iter(lambda: stream.read(BLOCK), b""):
                joined.update(data)
    require(joined.hexdigest() == digest(source), "Rejoined ISO differs from full ISO")
    return joined.hexdigest()


def read_inventory(source):
    readers = [ISO9660(str(source)), ISO9660(str(source), joliet=False)]
    try:
        joliet, primary = [dict(reader.walk()) for reader in readers]
        lookup = {}
        for name, entry in primary.items():
            key = (entry["lba"], entry["size"])
            require(key not in lookup, "Ambiguous original file extents")
            lookup[key] = name
        require(len(joliet) == len(primary) == 554, "Unexpected disc inventory")
        names = {name: lookup[(entry["lba"], entry["size"])] for name, entry in joliet.items()}
        return joliet, names
    finally:
        for reader in readers:
            reader.fh.close()


def preflight(source, build, output, fself):
    require(not output.exists(), "Output already exists; choose a new directory")
    require(fself.is_file(), "Compile PSL1GHT fself first; see CFW_TEST.md")
    require(source.stat().st_size == SOURCE_SIZE, "Wrong original ISO size")
    print("Verifying original ISO and every snapshot file...", flush=True)
    require(digest(source, "md5") == SOURCE_MD5, "Wrong original ISO hash")
    manifest = json.loads((build / "build_manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("ui_regression_checks") is True, "Snapshot lacks validated build stamp")
    require(manifest.get("version") == manifest.get("title_footer_version"), "Mixed snapshot version")
    for name, info in manifest["files"].items():
        safe_relative(name)
        path = build / name
        require(path.stat().st_size == info["bytes"] and digest(path) == info["sha256"],
                "Snapshot hash mismatch: " + name)
    paths = {"/" + "/".join(segments): name for name, segments in shipped_paths().items()}
    inventory, names = read_inventory(source)
    require(set(paths) <= set(inventory), "Patch contains files absent from original")
    require(set(paths.values()) <= set(manifest["files"]), "Incomplete snapshot")
    elf_headers((build / "EBOOT.BIN").read_bytes())
    require(shutil.disk_usage(output.parent).free > 20 * 2**30, "Need 20 GiB free for preparation")
    print("Base %s: %d game replacements; %d original disc files; FAT32 parts <= 2 GiB." %
          (manifest["version"], len(paths), len(inventory)), flush=True)
    print("Only a NEW output directory will be written: " + str(output), flush=True)
    print("No install, existing ISO replacement, firmware change, or public release.", flush=True)
    return manifest, paths, inventory, names


def build_package(source, build, output, fself, state):
    import pycdlib
    manifest, replacements, inventory, primary_names = state
    output.mkdir()
    stage = output / "intermediate_disc"
    stage.mkdir()
    delivery = output / "PS3ISO"
    delivery.mkdir()
    original_self = None
    expected = {}
    print("Preparing a clean disc tree from verified source + snapshot...", flush=True)
    with source.open("rb") as stream:
        for name, entry in inventory.items():
            target = stage / safe_relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            if name == "/PS3_GAME/USRDIR/EBOOT.BIN":
                stream.seek(entry["lba"] * SECTOR)
                original_self = stream.read(entry["size"])
            if name in replacements:
                shutil.copyfile(build / replacements[name], target)
                wanted = manifest["files"][replacements[name]]["sha256"]
            else:
                wanted = bounded_hash(stream, entry["lba"] * SECTOR, entry["size"])
                stream.seek(entry["lba"] * SECTOR)
                remaining = entry["size"]
                with target.open("xb") as out:
                    while remaining:
                        data = stream.read(min(remaining, BLOCK))
                        require(data, "Source ISO ended early")
                        out.write(data)
                        remaining -= len(data)
            require(digest(target) == wanted, "Staged file differs: " + name)
            expected[name] = {"bytes": target.stat().st_size, "sha256": wanted}
    elf = (build / "EBOOT.BIN").read_bytes()
    raw_self = output / "fself_generated.bin"
    subprocess.run([str(fself), str(build / "EBOOT.BIN"), str(raw_self)], check=True)
    wrapped = retain_application_metadata(raw_self.read_bytes(), original_self)
    self_report = verify_self(wrapped, elf, original_self)
    eboot = stage / "PS3_GAME/USRDIR/EBOOT.BIN"
    eboot.write_bytes(wrapped)
    expected["/PS3_GAME/USRDIR/EBOOT.BIN"] = {"bytes": len(wrapped), "sha256": digest(eboot)}
    print("CFW SELF verified: all %d ELF bytes preserved." % len(elf), flush=True)
    image_name = "SRW-Z3-English-%s-CFW-test1.iso" % manifest["version"]
    image = output / image_name
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident="PS3VOLUME", sys_ident="PLAYSTATION3")
    directories = {str(parent).replace("\\", "/") for name in inventory
                   for parent in Path(name).parents if str(parent) not in ("/", "\\", ".")}
    for directory in sorted(directories, key=lambda p: (p.count("/"), p)):
        iso.add_directory(iso_path=directory, joliet_path=directory)
    for name in sorted(inventory):
        iso.add_file(str(stage / safe_relative(name)), iso_path=primary_names[name] + ";1",
                     joliet_path=name)
    print("Writing fresh ISO9660 + Joliet image (no stale UDF tree)...", flush=True)
    iso.write(str(image))
    iso.close()
    stamp_disc(image)
    header_report = verify_disc_header(image)
    print("Re-reading every file from BOTH ISO trees...", flush=True)
    for joliet in (True, False):
        reader = ISO9660(str(image), joliet=joliet)
        try:
            actual = dict(reader.walk())
            keys = set(inventory) if joliet else set(primary_names.values())
            require(set(actual) == keys, "Disc file inventory changed")
            for name, want in expected.items():
                entry = actual[name if joliet else primary_names[name]]
                require(entry["size"] == want["bytes"] and
                        bounded_hash(reader.fh, entry["lba"] * SECTOR, entry["size"]) == want["sha256"],
                        "ISO file verification failed: " + name)
        finally:
            reader.fh.close()
    print("Splitting for FAT32 and verifying concatenated contents...", flush=True)
    parts = split_iso(image, delivery)
    sha = verify_parts(image, delivery, parts)
    report = {"schema": 1, "base_version": manifest["version"], "package": "CFW-test1",
              "hardware_tested": False, "target": "CFW with Cobra/fake-SELF support",
              "original_iso_md5": SOURCE_MD5,
              "base_manifest_sha256": digest(build / "build_manifest.json"),
              "fself_tool_sha256": digest(fself), "self": self_report, "disc": header_report,
              "fself_upstream_commit": "f649a08fd536a9e27c08c7db2d93a2d7ee4c3bbe",
              "fself_local_patch": "missing .sceversion guard documented in CFW_TEST.md",
              "iso": {"name": image_name, "bytes": image.stat().st_size, "sha256": sha},
              "parts": parts, "disc_files_verified_each_tree": len(expected), "files": expected,
              "translation_complete": manifest.get("translation_complete", False),
              "untranslated_mission_variants": manifest.get("untranslated_mission_variants"),
              "rpcs3_installation_modified": False}
    # Completion marker is written last: a failed/incomplete package has no audit.
    (output / "CFW_AUDIT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("VERIFIED HARDWARE-TEST PACKAGE: " + str(output), flush=True)
    print("Actual console boot/gameplay still UNTESTED.", flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fself", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    source, build, out, fself = [p.resolve() for p in (args.source, args.build, args.out, args.fself)]
    require(ROOT / "work" in out.parents, "Output must be a new directory under ignored work/")
    state = preflight(source, build, out, fself)
    if args.write:
        build_package(source, build, out, fself, state)
    else:
        print("Dry-run passed. Add --write to create this CFW hardware-test package.")


if __name__ == "__main__":
    main()
