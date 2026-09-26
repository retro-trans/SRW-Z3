"""Read-only PKG/RIF identity check. Never prints keys, zRIF or account IDs.

Optional --report writes ONLY the displayed non-secret JSON after a dry run.
Matching headers establish compatibility of identity, not successful decryption.
Offsets follow TheOfficialFloW/NoNpDrm's SceNpDrmLicense structure.
"""
import argparse
import json
from pathlib import Path
import re
import struct


def content_id(data):
    value = data.split(b"\0", 1)[0]
    if not re.fullmatch(rb"[A-Z]{2}[0-9]{4}-PCSG[0-9]{5}_[0-9]{2}-[A-Z0-9_]{16}", value):
        raise ValueError("Unexpected or malformed content ID (value suppressed)")
    return value


def inspect(header, actual_size, license_data):
    if len(header) < 0x80 or header[:4] != b"\x7fPKG":
        raise ValueError("Not a supported PKG header")
    if len(license_data) != 512:
        raise ValueError("Expected a 512-byte Vita RIF")
    pkg_id = content_id(header[0x30:0x60])
    rif_id = content_id(license_data[0x10:0x40])
    version, version_flag, kind = struct.unpack_from(">HHH", license_data)
    return {
        "title_id": pkg_id.decode("ascii").split("-")[1][:9],
        "pkg_size_matches_header": struct.unpack_from(">Q", header, 0x18)[0] == actual_size,
        "license_size_bytes": len(license_data),
        "full_content_id_matches": pkg_id == rif_id,
        "nonpdrm_header_fields": (version, version_flag, kind) == (1, 1, 1),
        "nonpdrm_account_marker": struct.unpack_from("<Q", license_data, 8)[0] == 0x0123456789abcdef,
        "license_key_present": any(license_data[0x50:0x60]),
        "cryptographic_validity_verified": False,
        "pfs_decryption_performed": False,
        "network_used_for_license": False,
        "secret_values_logged": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pkg", required=True, type=Path)
    parser.add_argument("--license", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    with args.pkg.open("rb") as source:
        header = source.read(128)
    # Bound the read even if a wrong file was passed. No raw values are returned.
    with args.license.open("rb") as source:
        license_data = source.read(513)
    report = inspect(header, args.pkg.stat().st_size, license_data)
    result = json.dumps(report, indent=2) + "\n"
    print(result, end="")
    if args.report:
        permitted = Path(__file__).resolve().parents[2] / "work" / "vita"
        if permitted not in args.report.resolve().parents:
            raise ValueError("Report must be under ignored work/vita")
        with args.report.open("x", encoding="utf-8") as output:
            output.write(result)
    else:
        print("Read-only check complete; no files written.")


if __name__ == "__main__":
    main()
