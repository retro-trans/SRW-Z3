# Title-screen Library submenu

The screenshot's five labels are baked into EFFPS3.CPK member 296, texture 5
(720 x 512 linear ARGB32). They are separate from the in-game Library widgets.
The GTF starts at 0x1fe290. The pristine member SHA-256 is
`dec8e258f43dc5ba892a2ceab84e0a6777a387e5bc7b57c48ed8fb98da4c9e7e`.

| Japanese | English | Sample rectangle (x,y,w,h) | References |
| --- | --- | --- | --- |
| ロボット大図鑑 | Robot Encyclopedia | 3,269,269,60 | 468 |
| キャラクター事典 | Character Encyclopedia | 1,204,307,55 | 463 |
| 用語事典 | Glossary | 1,137,167,57 | 459 |
| サウンドセレクト | Sound Select | 1,74,301,53 | 455 |
| シナリオチャート | Scenario Chart | 3,8,297,58 | 447 |

`tools/title_library_buttons.py` paints these five rectangles only, using
Times New Roman Bold (`C:/Windows/Fonts/timesbd.ttf`), white ink with a soft
gray glow matching the existing title labels. Text is centered, with narrow
horizontal fitting for the longer encyclopedia names. The before/after atlas
preview was visually reviewed. This is a game asset patch, not a screenshot edit.

All 2,292 normal/highlight animation sample records, geometry, timing, texture
headers, other artwork and existing English buttons are byte-identical.
The patch first applies the existing version footer when a version is supplied.
Its verifier restores only the five label rectangles before running the strict
footer verifier, so neither patch can silently modify unrelated bytes.

`location_caption.build` integrates this with the existing EFF composition;
`check_issue_fixes.py` uses the combined verifier for both numbered and debug builds.
Five tests in `tools/test_title_library_buttons.py` cover the full animation
family, rectangle isolation, footer composition, unrelated-change rejection
and source-drift rejection. Local original assets/fonts are required.

Verification passed against the rebuilt, packed candidate EFF: all five labels,
the footer, all 83 map captions, scenario-title companions and all untouched
member payloads. Five new tests and seven existing footer tests pass.

No live emulator, source game folder, save, ISO or release is changed. Candidate
`work/out_0.6.3` remains unstamped because of the independent STG0068 full-build
audit blocker documented in HANDOFF.md. The successful counter remains 0.6.2.
