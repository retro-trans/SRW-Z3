# English patch 0.6.1

For the Japanese retail PS3 release of Super Robot Taisen Z3: Jigoku-hen
(BLJS10256). Requires your own game dump; no complete game files are included.

## Changes since 0.6.0

- Story translation extended through **stage 30**, plus 26 intermission/route
  archives. Glossary references keep names consistent across the translated story.
- Mission conditions audited across all included stages: victory objectives,
  defeat events and SR requirements retain their different meanings, numbers
  and timing. Numbered, multiline and displayed-name variants are covered.
- All 78 terrain names across 64 maps are translated; map parameters and tile
  grids are unchanged.
- Weapon effects, battle effect labels, Tag Commands, Maximum Break artwork,
  repair/reward reports and D-Trader unlock notices receive translation fixes.
- Alignment and overflow fixes for team lists, status popups, library/network
  menus, search/settings, weapon headings and result messages.
- Builds now advance **0.6.1, 0.6.2, 0.6.3**, one number per successful complete
  build. Failed builds do not consume a number.

## Downloads

- **Original Japanese ISO:** `SRW-Z3-English-0.6.1.iso.xdelta` (136.6 MB).
- **Update an existing 0.6.0 ISO:** `SRW-Z3-English-0.6.0-to-0.6.1.iso.xdelta` (7.1 MB).
- **Pristine folder dump:** `SRW-Z3-English-0.6.1.zip` (45 MB), containing 133 per-file
  patches, the application helper, file hashes and installation instructions.

Original ISO: 4,431,872,000 bytes, MD5
`2cfedd95e5bdde49550cffa21c3c29a3`.
The update patch requires the 0.6.0 ISO with MD5
`9338e39087e3ac1e9f92eba167cb18e2`.

Both ISO patches produce the same 0.6.1 image: **4,935,067,648 bytes**, MD5
`2e8e5dbe6fa92c3f5abdb286da3cd80c`.

```text
xdelta3 -d -s "original.iso" SRW-Z3-English-0.6.1.iso.xdelta "SRW-Z3-English-0.6.1.iso"
```

For an update, substitute the 0.6.0 image and the 0.6.0-to-0.6.1 patch.
See [installation instructions](https://github.com/retro-trans/SRW-Z3/blob/master/docs/INSTALL.md).

## Scope and limitations

Dialogue after stage 30 remains Japanese. Some artwork and voice-actor names
also remain untranslated. Existing battle-line translations cover all 211
sets, including lines retained from the earlier length-limited translation.
Automated coverage/layout/binary checks are not a substitute for an in-game
playthrough; the combined 0.6.1 build still needs runtime visual confirmation.
This release does not change saves or gameplay conditions.

## Verification

Both ISO patches were decoded and compared to the release image. Every
per-file patch was decode-verified; the ZIP passed CRC and entry-hash checks.
The complete build passed binary/layout checks, 504 message-coverage checks,
10,740 centering cases, and 17 release/context unit tests.

SHA-256 downloads:

```text
a2c774b8e81ec68ef2fbb6d35e50980dee8e7e3168528132498c638fa5f4b517  SRW-Z3-English-0.6.1.iso.xdelta
56c3f88cbaae2a26942a6b6caf305ee06b32e5a3e0f8cf1772a25545fc9c492c  SRW-Z3-English-0.6.0-to-0.6.1.iso.xdelta
77f9a57285a4513dadf8a6d559995270cc6fc41ef9d7041a2f8c0fde654f4845  SRW-Z3-English-0.6.1.zip
```
