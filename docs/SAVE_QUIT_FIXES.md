# Save alignment and end-session translation

## What changed

The save-complete question renders each line independently. Its translation
already existed, but no line-specific centering compensation existed. Six
save/overwrite/return lines are now appended to `command_layout.SAVE_DIALOGS`.
Their pads occupy original blank cells 0x8468..0x846d and use the original
Japanese line count plus English ink width at live font pitch/quad size. Old
pad indices are unchanged. The VWF helper stays 264 bytes: only its bank-end
comparison changes.

`セーブが終了しました。` also occurs in a separate **left-aligned** AID widget
at 0xbfa54. `save_prompt_layout.py` gives this widget its own encoded English
string, preserving every style/position byte. It therefore cannot accidentally
match the new centered Japanese hook. The Yes/No selection/tab code is unchanged.

The end-session screenshot is **STG0700.CPK member 1, event t_060**, not the
battle-voice bank. Its seven speech records (563..569 in the member, event
ordinals 3..9) are now translated in `translation/suspend_scene.json`.
Seven of seven scene speech records were read in context. The entire member
contains 872 records, including 590 speech records: **other scenes have not
been translated by this change**. `suspend_scene.py` binds source hash, event,
ordinal, speaker ID and Japanese text fingerprint before replacing only these
seven long-string bodies. Source newline count, quote structure and runtime
placeholders are checked. Commands, voice cues, face states, waits and every
other byte remain unchanged. English uses glossary tokens for speaker names.

Trophy 022 is `Time to Rest`, with description `View an end-session message.`
`trophy_labels.py` changes only its name/description in TROP.SFM and TROP_00.SFM,
using outside-element whitespace to preserve archive entry sizes and offsets.
It preserves all other XML bytes, entry IDs, icons and conditions. The archive
SHA-1 is recomputed with the 20-byte hash field zeroed, matching
[RPCS3's loader](https://github.com/RPCS3/rpcs3/blob/master/rpcs3/Loader/TRP.cpp).
Native-console signature acceptance is not claimed. No user TROPUSR.DAT,
TROPCONF cache, saves or earned-progress data is opened or changed by the builder.

## Pipeline and verification

The shared build pools the scene's English in the global font mapping, creates
STG0700.SDAT using the established version-2 encryption, then decrypts it again
and compares the complete CPK. TROPHY.TRP is built alongside it. Deployment,
extraction and patch-application maps include both. Trophy data is a sibling
of USRDIR, under PS3_GAME/TROPDIR/NPWR05207_00; ISO lookup normalizes this path
and asserts it remains below PS3_GAME.

`python -W ignore::ResourceWarning tools/test_save_quit.py`: five tests pass.
Coverage includes emitted PPC centering, the separate left-aligned widget,
only seven changed dialogue bodies, rejection of source drift, trophy metadata
and checksum, and consistent disc/ISO paths. Original blank-cell checks passed
in both font layers. Existing deployment/map tests also pass.

Candidate `work/out_0.6.3` has been rebuilt and this batch's packed-file checks
passed: 11,520 emitted-PPC centering cases, 205 dialog hooks, 192 blank pad cells
in both built font layers, seven correctly encoded/fitting scene records,
SDAT decrypt round-trip and trophy checksum/metadata. All 83 map-caption
checks from the previous batch still pass. The full suite is 38/40 passing;
both failures and the full-build failure remain the independent STG0068
mission-source audit. Counter stays 0.6.2; the candidate has no successful
manifest and must not be deployed or published. No release or ISO is
performed here. In-game visual/audio confirmation is pending; installed trophy
metadata may remain cached, and this work does not delete that cache.
