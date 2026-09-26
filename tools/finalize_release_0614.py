"""Assemble an explicit release allowlist and checksums; never uploads. Dry-run."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile
from apply_vita_release import sha

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'work/release_0.6.14'
ISO_NAMES = ('SRW-Z3-English-0.6.14.iso.xdelta', 'SRW-Z3-English-0.6.13-to-0.6.14.iso.xdelta')
ZIP_NAMES = ('SRW-Z3-Vita3K-0.6.14-from-original.zip',
             'SRW-Z3-Vita3K-0.6.14-test16-linkfix-v3-to-0.6.14.zip',
             'SRW-Z3-Save-Converter-0.6.14.zip')
SOURCES = '''platforms/ps3/build_release_0614.py
platforms/ps3/build_link_background_update.py
platforms/ps3/build_date_card_update.py
platforms/ps3/build_dialogue_link_update.py
platforms/vita/build_link_background_patch.py
platforms/vita/build_link_background_install.py
platforms/vita/build_date_center_patch.py
platforms/vita/link_background.py
platforms/vita/main_link_background.py
platforms/vita/link_identity_geometry.py
platforms/vita/dialogue_link_scene.py
platforms/vita/date_card_centering.py
platforms/vita/ui_text.py
tools/apply_vita_release.py
tools/package_vita_release.py
tools/finalize_release_0614.py
tools/convert_z3_saves.py
tools/test_save_conversion.py
tools/test_apply_vita_release.py
tools/test_build_version.py
tools/test_iso_patch_cli.py
tools/test_ps3_date_cards.py
tools/test_ps3_link_identity.py
tools/test_main_link_background_layout.py
tools/test_link_background_layout.py
tools/test_president_report_layout.py
tools/test_vita_link_background.py
tools/test_vita_date_centering.py
tools/release.py
tools/release_patch.py
tools/iso_patch.py
tools/build_ui.py
tools/check_issue_fixes.py
tools/eboot.py
tools/link_background_layout.py
tools/main_link_background_layout.py
tools/link_identity_geometry.py
tools/dialogue_link_scene.py
tools/date_card_layout.py
tools/president_report_layout.py
tools/startup_menu_layout.py
tools/deploy.py
tools/apply_xdelta.py
docs/SAVE_CONVERTER_RELEASE.md
docs/RELEASE_0.6.14.md
releases/0.6.14.json
build_version.json'''.splitlines()


def info(path):
    return dict(bytes=path.stat().st_size, sha256=sha(path))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write',action='store_true')
    a=ap.parse_args()
    inputs={n:ROOT/'releases/0.6.14_xdelta'/n for n in ISO_NAMES}
    inputs.update({n:OUT/n for n in ZIP_NAMES})
    for n,p in inputs.items():
        assert p.is_file() and p.stat().st_size > 0,n
        print(n,p.stat().st_size,flush=True)
    for n in SOURCES:
        assert (ROOT/n).is_file() and Path(n).suffix in ('.py','.md','.json'),n
    print('Tool supplement:',len(SOURCES),'explicit source/document/hash files. No game data.')
    print('Additional assets: README, release hash manifest and SHA256SUMS.')
    if not a.write:
        print('DRY RUN: no files written.');return
    for n in ISO_NAMES:
        dest=OUT/n
        assert not dest.exists()
        shutil.copy2(inputs[n],dest)
        assert info(dest)==info(inputs[n])
    toolzip=OUT/'SRW-Z3-0.6.14-Tool-Updates.zip'
    with zipfile.ZipFile(str(toolzip),'x',zipfile.ZIP_DEFLATED) as z:
        for n in SOURCES:z.write(str(ROOT/n),n)
        z.writestr('README.md','Source/tool overlay for the tagged SRW-Z3 repository. See docs/RELEASE_0.6.14.md. No game data included. Local baseline game files are required for builders.\n')
    with zipfile.ZipFile(str(toolzip)) as z:
        assert z.testzip() is None and len(z.infolist())==len(SOURCES)+1
        for n in SOURCES:assert hashlib.sha256(z.read(n)).hexdigest()==sha(ROOT/n)
    guide=OUT/'README-0.6.14.md'
    assert not guide.exists()
    shutil.copy2(ROOT/'docs/RELEASE_0.6.14.md',guide)
    assets=list(ISO_NAMES)+list(ZIP_NAMES)+[toolzip.name,guide.name]
    manifest=dict(schema=1,version='0.6.14',platforms=['PS3/RPCS3','Vita3K'],
                  partial_translation=True,ps3_untranslated_mission_variants=1034,
                  ps3_combined_build_runtime_tested=False,
                  prior_link_fixes_user_confirmed=True,
                  ps3_target_image=info(ROOT/'work/release_image_0.6.14.iso'),
                  ps3_snapshot=json.loads((ROOT/'releases/0.6.14.json').read_text()),
                  assets={n:info(OUT/n) for n in assets})
    (OUT/'RELEASE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    assets.append('RELEASE_MANIFEST.json')
    (OUT/'SHA256SUMS.txt').write_text(''.join(sha(OUT/n)+'  '+n+'\n' for n in assets))
    assets.append('SHA256SUMS.txt')
    # A local plan, NOT a release asset. No wildcard upload should be used.
    (OUT/'UPLOAD_PLAN.json').write_text(json.dumps(assets,indent=2)+'\n')
    print('Prepared',len(assets),'explicit release assets. Ready for upload only after decode checks pass.')


if __name__=='__main__':main()
