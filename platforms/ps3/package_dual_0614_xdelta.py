"""Package the existing dual-test1 ISO, without rebuilding/installing anything."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

import build_dual_0614 as b

TARGET = b.ROOT / 'work/ps3_dual_0614_test1' / b.NAME
TARGET_SHA = 'e2be81330cc2e45d8317271c8e290f7cde768749b4ea681114efd95b498c63c7'
NAME = 'SRW-Z3-English-0.6.14-dual-test1-from-original.iso.xdelta'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    output = b.layout.x.output_path(args.out)
    b.c.require(shutil.disk_usage(output.parent).free > 8 * 2**30, 'Need 8 GiB free')
    print('Checking original and exact RPCS3-user-confirmed target ISO...', flush=True)
    original_info, target_info = b.d.info(b.ORIGINAL), b.d.info(TARGET)
    b.c.require(original_info['sha256'] == b.ORIGINAL_SHA, 'Original ISO hash mismatch')
    b.c.require(target_info['sha256'] == TARGET_SHA, 'Target ISO hash mismatch')
    b.c.require(b.XDELTA.is_file(), 'Missing xdelta3')
    print('Source: original Japanese BLJS10256 ISO')
    print('Target: existing 0.6.14-dual-test1, no rebuild or game changes')
    print('Output:', output / NAME, flush=True)
    if not args.write:
        print('DRY RUN PASSED. No output written.')
        return
    output.mkdir()
    patch = output / NAME
    print('Encoding from-original xdelta...', flush=True)
    subprocess.run([str(b.XDELTA), '-e', '-s', str(b.ORIGINAL), str(TARGET), str(patch)],
                   check=True)
    decoded = output / 'verification-only.iso'
    print('Decoding patch for independent verification...', flush=True)
    subprocess.run([str(b.XDELTA), '-d', '-s', str(b.ORIGINAL), str(patch), str(decoded)],
                   check=True)
    b.c.require(b.c.digest(decoded) == TARGET_SHA and
                decoded.stat().st_size == TARGET.stat().st_size, 'Decoded ISO mismatch')
    decoded.unlink()  # Only our verified temporary duplicate; never a user input.
    audit = dict(schema=1, patch=b.d.info(patch), original=original_info,
                 target=target_info, decoded_verified=True,
                 rpcs3_user_report='Works; reported 2026-09-18; test scope unspecified',
                 physical_ps3_confirmed=False, uploaded=False)
    (output / 'PATCH_AUDIT.json').write_text(json.dumps(audit, indent=2) + '\n')
    (output / 'SHA256SUMS.txt').write_text(audit['patch']['sha256'] + '  ' + NAME + '\n')
    shutil.copyfile(b.ROOT / 'docs/PS3_DUAL_TEST_0.6.14.md', output / 'README.md')
    print('COMPLETE: patch decodes to the exact tested target.', flush=True)
    print(json.dumps(audit, indent=2), flush=True)


if __name__ == '__main__':
    main()
