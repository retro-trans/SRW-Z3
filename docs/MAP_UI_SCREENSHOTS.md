# Map-menu screenshot follow-up

Implemented in native game assets, not edited screenshots.

## Text widgets (AIDDATAPACK member 0)

The screenshot's four-line Tag Command widget at 0x9cf94 was already translated
by `tag_reward_layout`: Multi Action, Bonus PP, Bonus Chips, Charge SP. Its
encoded strings, line spacing and fit are now covered by the packed tests.

New translations cover the complete adjacent selection-heading group:

| Record | English |
| --- | --- |
| 0xa9194 | Transform |
| 0xa91d4 | Spirit Commands |
| 0xa91f4 | Element Change |
| 0xa9214 | Power Parts |

Angle brackets are retained. English strings are appended and the exact
widget pointers relocated. Japanese count-based centering is replaced with
measured English ink positioning relative to the original half-pixel center.
Font size, vertical position, colors and other state fields remain unchanged.
Adjacent Search Settings at 0xa9234 is already translated and verified by
`naming_search_layout`; do not apply two patches to that same record.

## Battle status artwork (member 1, texture 2)

The screenshot's 装甲値▼ is assembled from three image pieces, independently
of the already translated text-hook effect descriptions. `trader_art` now
renders Armor in (56,256)-(112,288), Sight in (56,224)-(112,256), and clears
the shared 値 suffix at (56,352)-(88,384). English does not require that suffix.
The original down-arrow tile remains intact. Existing Mobility uses its
earlier Mobi/lity split and remains unchanged. Color is supplied by the game.

The extracted, assembled Armor/Sight/Mobility popup preview was visually
reviewed. Every byte outside the explicitly declared atlas cells is verified
unchanged after composing with the existing ALL Attack patch. No UV, layout,
animation or tint commands are altered.

## Spirit clear-marks confirmation

The candidate EBOOT already contains both runtime translations:

- All marked Spirits will be cleared.
- Are you sure?

The constructor copies fixed UTF-8 byte counts before conversion to CP932.
The original UTF-8 literals and pointers must remain untouched; replacement
occurs in the existing runtime lookup after conversion. The new tests verify
the actual packed EBOOT lookup entries and source-copy bytes. No EBOOT or
font modification was needed in this batch.

## Verification and delivery

`python tools/build_ui.py --out work/out_0.6.3` rebuilt the candidate AID archive.
`python -m unittest discover -s tools -p test_map_ui_screenshots.py` passes all
three tests. Candidate-only checks do not approve a release or establish live
runtime behavior. No source game, emulator, cache, save, ISO or release was
modified. The separate STG0068 full-build audit blocker remains; counter 0.6.2
is unchanged. Screenshots showing Japanese despite existing translations
need a verified complete deployment and live retest, not blind source edits.
