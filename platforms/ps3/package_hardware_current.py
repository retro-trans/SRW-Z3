"""Package a validated current-source build for local PS3 hardware testing.

Dry-run by default. Reuses the guarded two-LOAD fold and original disc
metadata. Does not number builds, publish, or install anything.

The image keeps the original disc's layout by default (`preserved_iso`), so an
original-to-release xdelta carries only the changed files. `--fresh-layout`
selects the earlier writer, which rebuilds both trees from scratch; that is
the layout of the user-confirmed 0.6.15-hardware-test1 and is kept for
regression comparison. Both apply the same disc-header fix.
"""
import argparse
import copy
import json
from pathlib import Path
import re
import shutil

import build_dual_0614 as b
import preserved_iso

c, d, layout = b.c, b.d, b.layout


def preflight(source, build, output, fself):
    c.require(c.ROOT / 'work' in output.parents, 'Output must be under work/')
    c.require(output.parent.is_dir(), 'Output parent must exist')
    c.require(c.digest(fself) == d.FSELF_SHA256, 'Wrapper tool changed')
    state = c.preflight(source, build, output, fself)
    manifest, replacements, inventory, primary = state
    c.require(re.fullmatch(r'\d+\.\d+\.\d+', manifest['version']), 'Unsafe version')
    c.require(manifest.get('platform') == 'ps3', 'Expected PS3 snapshot')
    c.require(c.digest(source) == b.ORIGINAL_SHA, 'Wrong original ISO SHA256')
    original = b.read_member(source, inventory[d.EBOOT])
    c.control_records(original)
    elf = (build / 'EBOOT.BIN').read_bytes()
    folded = layout.fold(elf)  # Rejects any incompatible input layout.
    print(json.dumps(layout.verify(elf, folded), indent=2), flush=True)
    print('Packaging override: ONE full unsplit ISO, no FAT32 parts or delta.')
    print('Fresh validated source build; NOT the frozen 0.6.14 translations.')
    return state, original, elf, folded


def package(source, build, output, fself, state, fresh=False):
    (manifest, replacements, inventory, primary), original, elf, folded = state
    manifest_hash = c.digest(build / 'build_manifest.json')
    output.mkdir()
    elfpath = output / 'EBOOT-two-load.elf'
    elfpath.write_bytes(folded)
    wrapped, self_report = d.wrap(elfpath, original, fself, output / 'wrapper-generated.bin')
    c.require(b.rpc_decode(wrapped) == folded, 'RPCS3 SELF extraction differs')
    stage = output / 'intermediate_disc'
    stage.mkdir()
    print('Extracting and verifying original disc...', flush=True)
    original_files = d.extract_original(source, stage, inventory)
    files = copy.deepcopy(original_files)
    snapshot = output / 'snapshot'
    snapshot.mkdir()
    for name, expected in manifest['files'].items():
        c.require(Path(name).name == name, 'Unsafe snapshot filename')
        src = build / name
        c.require(d.info(src) == expected, 'Snapshot changed: ' + name)
        shutil.copyfile(src, snapshot / name)
        c.require(d.info(snapshot / name) == expected, 'Snapshot copy failed: ' + name)
    (snapshot / 'EBOOT.BIN').write_bytes(wrapped)
    derived = copy.deepcopy(manifest)
    derived['files']['EBOOT.BIN'] = d.info(snapshot / 'EBOOT.BIN')
    derived['compatibility_candidate'] = 'hardware-test1; runtime unverified'
    derived['derived_from_manifest_sha256'] = manifest_hash
    derived['loader_layout_checks'] = layout.verify(elf, folded)
    for name, local in replacements.items():
        target = stage / c.safe_relative(name)
        shutil.copyfile(snapshot / local, target)
        files[name] = d.info(target)
        c.require(files[name] == derived['files'][local], 'Overlay mismatch: ' + name)
    c.require(set(d.changed(original_files, files)) <= set(replacements),
              'Unexpected changes outside the validated deployment list')
    version = manifest['version']
    image_name = 'SRW-Z3-English-%s-hardware-test1.iso' % version
    if fresh:
        image = d.write_image(output / image_name, stage, primary, files)
    else:
        staged = {name: stage / c.safe_relative(name) for name in replacements}
        image = preserved_iso.write(output / image_name, source, inventory, primary,
                                    staged, files)
    c.require(c.digest(build / 'build_manifest.json') == manifest_hash, 'Source manifest changed')
    (snapshot / 'build_manifest.json').write_text(json.dumps(derived, indent=2) + '\n', encoding='utf-8')
    shutil.copyfile(c.ROOT / 'docs/PS3_CURRENT_HARDWARE_TEST.md', output / 'README.md')
    (output / 'SHA256SUMS.txt').write_text(image['sha256'] + '  ' + image_name + '\n', encoding='ascii')
    report = dict(schema=1, candidate=version + '-hardware-test1', image=image,
                  original_iso_sha256=b.ORIGINAL_SHA, source_manifest_sha256=manifest_hash,
                  shared_content=manifest.get('shared_content'),
                  fself_sha256=d.FSELF_SHA256, raw_elf_sha256=b.sha(elf),
                  folded_elf=d.info(elfpath), executable=derived['files']['EBOOT.BIN'],
                  self_checks=self_report, layout_checks=layout.verify(elf, folded),
                  rpcs3_debug_self_extraction_verified=True,
                  files=files, replacements=len(replacements),
                  translation_complete=manifest.get('translation_complete', False),
                  untranslated_mission_variants=manifest.get('untranslated_mission_variants'),
                  hardware_tested=False, rpcs3_runtime_tested=False,
                  installed=False, release_or_upload_performed=False)
    (output / 'HARDWARE_TEST_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('COMPLETE: local hardware candidate; console boot/gameplay still untested.', flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=b.ORIGINAL)
    parser.add_argument('--build', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--fself', type=Path, default=b.FSELF)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--fresh-layout', action='store_true',
                        help='Rebuild both ISO trees (0.6.15 layout); patches become very large')
    args = parser.parse_args()
    source, build, output, fself = [p.resolve() for p in (args.source, args.build, args.out, args.fself)]
    state = preflight(source, build, output, fself)
    if args.write:
        package(source, build, output, fself, state, fresh=args.fresh_layout)
    else:
        print('DRY RUN PASSED; no output or installation changed.')


if __name__ == '__main__':
    main()
