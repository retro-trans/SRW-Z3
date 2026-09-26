# -*- coding: utf-8 -*-
"""Vietnamese build. Needs --kanji (852 pairs vs a 634-cell safe pool) and
--metrics 11,25 so stacked tone marks have room."""

STAGES = [
 {"cpk": "work/stage_dec/STG0001A.cpk", "sdat": "STG0001A.SDAT",
  "members": [
    {"id": 4, "lua": "work/luaA/STG0001A_00004.lua",
     "trans": "translation/vi/stage0001a.json"},
  ]},
 {"cpk": "work/stage_dec/STG0001B.cpk", "sdat": "STG0001B.SDAT",
  "members": [
    {"id": 3, "lua": "work/luaB/STG0001B_00003.lua",
     "trans": "translation/vi/stage0001b_03.json"},
    {"id": 4, "lua": "work/luaB/STG0001B_00004.lua",
     "trans": "translation/vi/stage0001b_04.json"},
  ]},
]

# English library so the shared atlas stays consistent with the deployed zukan
LIBRARIES = [
 {"cpk": "work/lib/MTZKN_KW.CPK", "trans": "translation/library_kw.py"},
 {"cpk": "work/lib/MTZKN_PT.CPK", "trans": "translation/library_pt.py"},
 {"cpk": "work/lib/MTZKN_RT.CPK", "trans": "translation/library_rt.py"},
]
