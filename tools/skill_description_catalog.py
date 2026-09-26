"""Pilot-skill prose from the JP effects, reviewed against Akurasu Z3.

Reference: https://akurasu.net/wiki/Super_Robot_Wars/Z3/Pilot_Abilities
Reviewed 2026-09-11. Descriptions only; names, PP prices and mechanics untouched.
Wiki-only additions/corrections are documented in PILOT_SKILL_DESCRIPTIONS.md.
"""
import localization as _l10n
SOURCE = 'https://akurasu.net/wiki/Super_Robot_Wars/Z3/Pilot_Abilities'
DATA = _l10n.literal('skill_description_catalog.DATA/0')
CATALOG = dict(line.split('|',1) for line in DATA.strip().splitlines())
