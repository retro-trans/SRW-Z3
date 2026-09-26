# Title-screen build footer

The press-any-button screen displays two right-aligned lines:

- `v<successful build number>`
- `github.com/retro-trans`

`tools/title_footer.py` renders them from the build's PS3 bold Latin font,
at 18 px on the native 1280x720 canvas. The right and bottom insets are
28 and 24 px. A dark outline keeps the light text readable over the stars.

## Exact resource and scope

The original `COMMONDATA/KURODATA/LUACPK.CPK` member 1 defines
`ScAnime_Z3TITLE = 295`. `ANIME/EFFPS3.CPK` has a shared member 0, so the
title animation is **member 296**, not 295. Its GTF begins at `0x1fe290`;
texture 0 is the stationary 1280x720 Earth/galaxy title background. All
seven textures use linear ARGB32. Textures 1/2 hold the logo and prompt;
3/4 are the subsequent menu backgrounds, 5 the menu text, and 6 effects.

Only texture 0's rectangle `(912,640)-(1252,696)` is changed. The member
size, texture headers, animation commands, logo, prompt, other six textures,
and other archive members are preserved. This is build-time native font
rendering, not an edited screenshot or a hard-coded release bitmap.

The relevant background quads sample `(0,0,1280,720)` at fixed coordinates.
The title view uses `(-480,-270)-(480,270)`; a larger backdrop also samples
the same texture at `(-640,-360)-(640,360)`. No quad positions or timing
are patched. Other title-menu backgrounds intentionally have no footer.

## Version consistency and verification

`build_project.py` reads the next prospective number at build start and
passes it into the existing `location_caption.build` EFF rebuild, alongside
the school-caption and episode-card patches. The full regression gate reads
the actual output member and verifies its exact pixels for that version.

At successful numbering, `build_version.stamp` checks the expected number
under its exclusive lock. If another build claimed it in the meantime,
numbering fails without advancing the counter; rebuild with the new number.
The visible footer, `title_footer_version`, and manifest `version` must agree.
Partial/debug builds are not numbered and do not receive this footer.

Tests: `test_title_footer.py` checks alignment, spacing, overflow rejection,
repeatability, source identity, version changes, and byte preservation.
`test_build_version.py` covers sequential numbering, mismatches, and a
concurrent-build conflict. `check_issue_fixes.py --out <build> --version <n>`
validates a not-yet-numbered build; after numbering it reads the manifest.

The build's `title_footer_background.png` is an extracted asset preview,
not an RPCS3 screenshot. Live emulator placement remains a separate check.
