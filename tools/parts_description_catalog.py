"""Reviewed Z3 parts effects, adapted to the three-line in-game help panel.

Reference: https://akurasu.net/wiki/Super_Robot_Wars/Z3/Parts (2026-09-11).
Original wording, not a verbatim copy of the reference table. Names stay as-is.
The Japanese names identify RPW records; descriptions are NEVER written to RPW.
"""
import localization as _l10n

SOURCE = 'https://akurasu.net/wiki/Super_Robot_Wars/Z3/Parts'
# Keep the full effects, including range exceptions and non-stacking rules.
# The wiki corrects F Bomber's first activation to the second player turn.
DATA = _l10n.literal('parts_description_catalog.DATA/0')
CATALOG = dict(line.split('|', 1) for line in DATA.strip().splitlines())
