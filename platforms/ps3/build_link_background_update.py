"""Minimal RPCS3 link-background update for the inspected older English EBOOT.

Dry-run by default. Never installs, changes fonts, or repackages a physical ISO.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
import eboot
import link_background_layout as links

SOURCE_SHA = '635cf35d2e30f99e8b6a3e8ad9207f62feba9ffb356459e057ce40a6bd8110f4'
V1_SHA = '95f4a80073cbc404e3ae4c2796c26e0648da3d3b765774074b8a93265ad10a1a'
V2_SHA = 'a414df32b5bffc8ac86877a5b01cb3d2ae4123f3dbab51d5088d3506c5544c3e'
UI_SHA = '25b31e62c3a7f84852ac371e07a34628f34a43df117ef5add18fbb77acf37d8b'
UI_PATH = 'PS3_GAME/USRDIR/DATA/AIDDATA/AIDDATAPACK.CPK'
ZIP_NAME = 'SRW-Z3-PS3-RPCS3-link-background-v3-menu-update.zip'
GUIDE = '''# PS3 / RPCS3 link-background and startup-menu update v3

For the inspected older English executable only (shared by local builds
0.6.10, 0.6.11 and 0.6.12). This is NOT a Vita patch or a physical-console
SELF/ISO. Do not replace an executable from a newer or different build.

Required original EBOOT.BIN SHA256:
635cf35d2e30f99e8b6a3e8ad9207f62feba9ffb356459e057ce40a6bd8110f4
Or the first link-background update from that same build:
95f4a80073cbc404e3ae4c2796c26e0648da3d3b765774074b8a93265ad10a1a
Or v2:
a414df32b5bffc8ac86877a5b01cb3d2ae4123f3dbab51d5088d3506c5544c3e

Required AIDDATAPACK.CPK SHA256:
25b31e62c3a7f84852ac371e07a34628f34a43df117ef5add18fbb77acf37d8b

Close RPCS3 fully. Back up EBOOT.BIN and DATA/AIDDATA/AIDDATAPACK.CPK from
PS3_GAME/USRDIR outside the game folder. Verify the source hashes above,
then copy BOTH files from this ZIP to their matching paths. Keep all other
fonts, translations and saves. Do not delete/reinstall the game.
The configured game inspected here is E:/Projects/SRW Z3/game/.

Restart and select Kei, Kira, Destruction Incident and Regeneration War
in BOTH dialogue and backlog. The background should start at the selected
text and fit its rendered width. Also check Alto/ZEXIS, scroll, switch short
and long selections, open linked library entries and return normally.
Automated checks passed; in-game visual verification is still required.
Also check Scenario Select, Main Scenario, Tutorial Scenario, and the DOB
month/day display (for example 5/28). Date values and editing are unchanged.
Restore both backed-up files with RPCS3 closed to roll back.

The first update, 0.6.13 and physical-console test-06 only contained the
secondary-path fix. V2 added primary term geometry. V3 additionally fixes the
separate speaker-name widgets and translated glossary identity comparison.
However, this package matches the older RPCS3 build ONLY: do not install it
over 0.6.13 or on physical PS3. Those require their own matching build.
No installation occurs automatically.
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def patch(original):
    source_sha = digest(original)
    if source_sha not in (SOURCE_SHA,V1_SHA,V2_SHA):
        raise ValueError('Wrong EBOOT: this update only accepts the inspected older English build')
    changed = bytearray(original)
    import link_identity_geometry as identity
    if source_sha == V2_SHA:
        ranges = identity.apply(changed, eboot._segments(changed))
    elif source_sha == V1_SHA:
        import main_link_background_layout as primary
        ranges = primary.apply(changed, eboot._segments(changed))
        ranges.extend(identity.apply(changed, eboot._segments(changed)))
    else:
        ranges = links.apply(changed, eboot._segments(changed))
    allowed = {i for lo, hi in ranges for i in range(lo, hi)}
    actual = {i for i, (a, b) in enumerate(zip(original, changed)) if a != b}
    if len(changed) != len(original) or not actual <= allowed:
        raise ValueError('Unrelated executable bytes changed')
    links.check(changed)
    identity.check(changed)
    return bytes(changed), ranges, len(actual)


def patch_ui(source):
    from cpk import CPK
    import startup_menu_layout as menu
    cpk=CPK(str(source))
    if digest(cpk.buf)!=UI_SHA:raise ValueError('Wrong UI archive: matching older English build required')
    result=bytearray(cpk.buf);members=[]
    for entry in cpk.files:
        if entry['id'] not in (0,1):continue
        assert entry['size']==entry['extract'], 'Expected uncompressed, fixed-size UI member'
        raw=cpk.read(entry)
        changed=menu.apply_ui(raw) if entry['id']==0 else menu.apply_art(raw)
        assert len(changed)==entry['size']
        start=entry['offset'];result[start:start+len(changed)]=changed
        members.append(dict(id=entry['id'],offset=start,bytes=len(changed),sha256=digest(changed)))
    assert len(members)==2 and len(result)==len(cpk.buf)
    allowed={i for member in members for i in range(member['offset'],member['offset']+member['bytes'])}
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(cpk.buf,result)))
    return bytes(result),members


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT/'game/PS3_GAME/USRDIR/EBOOT.BIN')
    parser.add_argument('--ui-source',type=Path,default=ROOT/'game'/UI_PATH)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    if (ROOT/'work').resolve() not in out.parents or out.exists():
        raise ValueError('Use a NEW output directory under work')
    original = args.source.read_bytes()
    changed, ranges, count = patch(original)
    ui, members = patch_ui(args.ui_source)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in [('PS3_GAME/USRDIR/EBOOT.BIN', changed), (UI_PATH,ui), ('README-INSTALL.md', GUIDE.encode())]:
            entry = zipfile.ZipInfo(name, (2026, 9, 17, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data, compresslevel=9)
    zipped = stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(zipped)) as archive:
        assert archive.testzip() is None
        assert archive.read('PS3_GAME/USRDIR/EBOOT.BIN') == changed
        assert archive.read(UI_PATH)==ui
    report = dict(source=str(args.source.resolve()), source_sha256=digest(original),
                  eboot_sha256=digest(changed), eboot_bytes=len(changed),
                  changed_bytes=count, allowed_file_ranges=ranges,
                  zip_sha256=digest(zipped), zip_bytes=len(zipped),
                  ui_source_sha256=UI_SHA,ui_sha256=digest(ui),ui_bytes=len(ui),ui_members=members,
                  installed=False, runtime_tested=False, platform='PS3 / RPCS3 only')
    print(json.dumps(report, indent=2))
    if not args.write:
        print('DRY RUN: no files written. Inspect before --write.')
        return
    out.mkdir(parents=True)
    for name, data in [(ZIP_NAME,zipped),('README-INSTALL.md',GUIDE.encode()),
                       ('BUILD_AUDIT.json',(json.dumps(report,indent=2)+'\n').encode())]:
        with (out/name).open('xb') as target:
            target.write(data)
        assert (out/name).read_bytes() == data
    assert args.source.read_bytes() == original
    print('Saved verified update:', out)


if __name__ == '__main__':
    main()
