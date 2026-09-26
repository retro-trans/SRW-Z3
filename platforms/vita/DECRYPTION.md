# Offline Vita PFS decryption — 2026-09-14

Completed using the user's existing PCSG00264 version 01.00 PKG and work.bin.
The original files were read only. No license, key or game data was uploaded.
Downloading public tooling source was the only network activity.

## Result and limits

- Encrypted extraction: `work/vita/app/PCSG00264`.
- PFS-decrypted data: `work/vita/decrypted_PCSG00264`.
- Audit: `work/vita/decryption_audit.json` (589 file hashes, no license values).
- Native parser passed mount metadata/signature checks, file decryption and
  keystone checks. Independent inspection matched all file names and sizes
  excluding PFS/package metadata, read 176 CPK tables / 35,861 member bounds,
  checked 189 GXT signatures and decompressed three opening-stage candidates.
- Candidate IDs: STG0001a ID 4, STG0001b IDs 3 and 4. Successful reads do not
  establish exact shared translation-record or control-metadata compatibility.
- EBOOT is still an SCE SELF container; inner executable decryption is unverified.
  No translated Vita game build, repack, install or runtime test was performed.
  PS3 outputs, shared English and version counter are unchanged.

## Public source provenance

All dependencies and generated binaries are ignored under `work/vita`.

| Source | Revision |
| --- | --- |
| https://github.com/mmozeiko/pkg2zip | 9222c4e00235dfe7914e9db0cc352da07e63d9f9 |
| https://github.com/Vita3K/psvpfsparser | d14381f871a69009bd18b2aaec2213a6738bebba |
| https://github.com/openssl/openssl (openssl-3.0.12 headers) | c3cc0f1386b0544383a61244a4beeb762b67498f |

Used GCC/G++ from `C:/mingw64/bin`, Python at `C:/Python/python.exe`, and Git's
existing `mingw64/bin/libcrypto-3-x64.dll` and `usr/bin/perl.exe`.
No OpenSSL installation or crypto system setting was changed.

Git's minimal Perl required local public CPAN modules: Locale-Maketext-Simple
0.21, ExtUtils-MakeMaker 7.70, Pod-Usage 2.03, podlators 6.1.1, Pod-Simple 3.48,
and Pod-Escapes 1.07. These reside in version-named work/vita folders. OpenSSL
`Configure mingw64 no-tests` generated configdata.pm; the Makefile phase initially
failed due missing Perl modules. After supplying them, the build helper used
official util/dofile.pl to generate public headers from that configdata.pm.
The helper requires these already prepared sources/configdata; it downloads nothing.

## Commands and safety

Compile pkg2zip's `pkg2zip*.c`, `miniz_tdef.c` and `puff.c` with GCC flags
`-O2 -std=c99 -DNDEBUG -D_GNU_SOURCE -maes -mssse3 -mpclmul -msse4`.
Inspect `pkg2zip -l` first, then run `pkg2zip -x` on the original package with
working directory `work/vita`. No zRIF or raw key argument was used.

From repository root, with Git's mingw64/bin and C:/mingw64/bin on PATH:

```powershell
python platforms/vita/build_offline_reader.py
./work/vita/offline_pfs.exe 'E:/Projects/SRW Z3/work/vita/app/PCSG00264' 'E:/Projects/SRW Z3/work/vita/decrypted_PCSG00264' 'E:/SRWZ3/iso/work.bin'
# Inspect dry-run, then repeat with --write, ONLY for a new destination.
python platforms/vita/verify_decryption.py --source work/vita/app/PCSG00264 --decrypted work/vita/decrypted_PCSG00264
# After inspecting, --report work/vita/decryption_audit.json saves a new audit.
python -m unittest discover -s tools -p 'test_vita*.py'
```

Outputs already exist; do not rerun write commands against them. The reader
and audit writer refuse overwrite. A failed file-decryption run may leave a
partial destination, which must not be treated as verified or silently reused.
Run the verifier with normal Python (not -O; assertions are part of its checks).

The adapter passes the locally read license key directly in memory, selects
F00DNativeKeyEncryptor explicitly, excludes upstream CLI/zRIF/factory/cache
sources, and discards upstream stdout/stderr/diagnostics without buffering.
Only fixed status text and numeric progress are emitted. No unknown exception
strings or key caches are printed. Seven tests pass: five synthetic license
checks plus wrong-key rejection before output creation and existing-output
preservation. Integration tests never read the user's real license.

Built SHA-256 values:

- pkg2zip.exe: `938b2abc4cf574822303e2a925bcd921c25b27128326a69aceb0a6d21c2ccbf1`
- offline_pfs.exe: `aae962c53de1691aa3a15bb3b61aa3b44f0fdae20a0ca47d12703014d62aa61a`

Next: parse and strictly match the decrypted opening scripts to canonical
`translation/` records; do not create a second editable English translation set.
