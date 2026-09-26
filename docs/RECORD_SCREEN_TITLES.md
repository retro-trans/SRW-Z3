# Record screen title and category follow-up

September 13, 2026. Source changes only; installed version stays 0.6.12.

The screenshot titles are not single strings. Original AIDDATAPACK member 0
contains these FSSA groups in visual order:

| Caption | Records | Original pieces |
| --- | --- | --- |
| Pilot TOP 5 | a03f4, a03d4, a0374, a0394, a03b4, a0414 | ～ / パイ / ロット / ＴＯ / Ｐ５ / ～ |
| Ace Pilot variant 1 | a07f4, a0814, a0834, a0854 | エースパイ / ロット / ＢＥ / ＳＴ５ |
| Ace Pilot variant 2 | a0874, a0894, a08b4, a08d4 | same |
| Trade List variant 1 | a25f4, a2614, a2634, a2654 | ：ト / レ / ード / リスト |
| Trade List variant 2 | a2a54, a2a74, a2a94, a2ab4 | same |

The separate UTF-8 `トレードリスト` at EBOOT file offset 0x6d9170 belongs to
the Key Help caption table. Translating it is not proof that the displayed
header is translated. Likewise the complete Pilot title prototype at aed14
does not replace the six-fragment header. Remove the guessed whole-title
hooks now that the source fragments are identified.

`record_screen_labels` places one complete English caption in the leftmost
fragment and points the remaining siblings at empty strings. It measures the
English advances against the original group's left/right bounds and changes
only the first X coordinate. Font sizes, baselines, colors, styles and
animation records are unchanged. The related Ace Pilot variants retain Ace
in the English title.

Trade List category headings a2674/a2694 and a2ad4/a2af4 have approximately
150 native pixels before the first item icon in the reported layout. At
25px, Upgrade Systems consumed 214.84 pixels and Power Parts 147.66 pixels.
Use Systems (94.16px) and Power Parts (135.84px), both at 23px, to retain
clear separation. Keep the wider Buy-screen a26f4 Upgrade Systems unchanged.
No item positions, locked entries, unlock conditions or selection logic change.

Validation: eight record-category tests cover original fragment inventory,
exact patch isolation, text fit/centering, sibling suppression, source and
position guards, category spacing, existing target/lore coverage, and the
actual production UI pass order executed in memory before its output stage.
Four menu and three Combat Record regressions also pass. Packed validation
checks the translated fragments, title coordinates/styles and category sizes.
In-game confirmation remains pending the user's explicit build instruction.
