# English title logo

The local 0.6.3 candidate uses an official-style English wordmark inspired by
the user's SRW X cover reference, not an exact pixel copy of that cover.
Text: `3rd SUPER ROBOT WARS`, subtitle `TIME PRISON / CHAPTER`.
The original Z frame and fiery fill stay native, including their animation.

## Approved subtitle revision (2026-09-13)

The user approved the September 12 combined preview, then explicitly asked
to install it on September 13. That preview had never entered the build:
0.6.11 still contained the old equal-weight subtitle. The new subtitle makes
TIME PRISON dominant and CHAPTER smaller, with contour-following purple edges.
Main wordmark and native Z stay unchanged.

The user explicitly authorized scripted background removal and resizing to
preserve the approved lettering, rather than regeneration. Source copies:
`work/title_logo_draft/subtitle-approved-v2.png` and
`work/title_logo_draft/combined-approved-v2.png`. The subtitle source is RGB
with a baked-in checkerboard, not true alpha. `prepare_approved_subtitle.py`
hash-checks the approved source, removes neutral background including enclosed
letter holes, gives the violet glow soft alpha, and resizes without distorting
the lettering. Run with `--write` to save `work/title_logo_final/subtitle-v2.png`
and its dark/light alpha preview. The 339x117 native tile retains x=8, y=5;
visible bounds are (8,5)-(324,79). Old subtitle.png remains for rollback.
`title_logo.py` pins the new tile's SHA256. The existing exact native-Z,
animation, Library and footer preservation tests still apply.

## Provenance and local assets

Built-in imagegen produced two RGB drafts. The user subsequently authorized
scripted cleanup of the baked checkerboard. No external API/CLI generation.
Prompt and saved drafts: `work/title_logo_draft/PROMPT.md`, `english-logo-v2.png`.
`tools/clean_title_logo.py` previews dimensions by default; `--write` generates:

- `work/title_logo_final/wordmark.png` — RGBA706x296.
- `work/title_logo_final/subtitle.png` — RGBA339x117.
- `work/title_logo_final/alpha-preview.png` — dark/light alpha inspection.

Retain these local assets: they are ignored game-art derivatives, not source
control content. Rebuilding from a fresh checkout needs the saved draft/tiles
as well as the normal original game inputs. No silent Japanese fallback.
`title_logo.py` guards the exact reviewed PNG hashes.

## Native layout and preservation

EFFPS3 member296, GTF offset0x1fe290, texture1, linear ARGB32, 1024x720.
The wordmark samples (0,0,706,296), 1706 references; subtitle samples
(0,603,339,117), 1657 references. Artwork uses the native padding and pivots.
No UV/geometry/blend/animation records change.

Every byte of the Z sampling rectangles is preserved, including transparent
RGBA bytes: frame (24,304)-(473,601), fills (664,268)-(1024,550) and
(666,268)-(1024,564). Textures0 and2-6, prompt, menu, footer and all unrelated
member bytes are unchanged by this layer. The library/footer build runs first.

## Historical 0.6.3 candidate, checks and rollback

`python tools/patch_title_logo_candidate.py` is a dry-run.
With `--write`, it backs up the current member, packs a sibling archive,
audits all other 333 compressed payload hashes, and replaces the candidate
only after verification. It refuses a concurrently modified candidate.
Backup: `work/title_logo.before.member`; audit: `work/title_logo_patch_audit.json`.
Packed atlas: `work/out_0.6.3/title_logo_atlas.png`.
Rollback only member296 using that backup and cpkpatch against a sibling
archive, preserving other candidate work. Do not replace the entire archive
with the pristine Japanese archive.

All 18 `test_title*.py` tests passed. Checks cover native sample counts,
alpha, exact preservation, idempotence, unexpected modifications, and full
Library/footer composition. In-game visual/animation confirmation remains
pending; no deployment, ISO, release or stamping was performed.
