# Library voice actor credits

`translation/library_voice_actors.json` romanizes the original game's ACTR credits,
not English dub actors. Given name precedes family name; ASCII spellings omit
macrons. Established stage spellings such as Show Hayami, Nobutoshi Canna,
Yukana and Cho are retained. The source placeholder remains `---`.

The source Library is the authority for which actor is credited to each entry.
All 153 distinct named credits are covered, not only playable pilots. Names
are romanizations; not every spelling is claimed to be an official English
credit. Targeted reading/spelling checks included:

- Haruna Ikezawa / 池澤春菜: [Asahi author profile](https://book.asahi.com/writer/11001912)
  supplies the reading; [English biographical spelling](https://en.wikipedia.org/wiki/Haruna_Ikezawa).
- Go Shinomiya / 四宮豪: [Ken Production agency profile](https://www.kenproduction.co.jp/talent/42)
  gives Shinomiya Go and the kana reading.
- Nobutoshi Canna / 神奈延年: [Aoni agency profile](https://www.aoni.co.jp/search/canna-nobutoshi.html).
- Tokio Shoji / 正司トキオ: [cast database](https://www.animecharactersdatabase.com/va.php?va_id=10416)
  gives Tokio Shouji; Shoji is the same long-vowel reading without `ou`.
- Ryu Murakami / 村上龍: the original Library credits Hibiki with this name;
  [Hibiki character reference](https://www.namu.moe/w/%ED%9E%88%EB%B9%84%ED%82%A4%20%EC%B9%B4%EB%AF%B8%EC%8B%9C%EB%A1%9C)
  identifies the actor as Murakami Ryu. Do not substitute the novelist's biography.
- Kazumi Togashi / 冨樫かずみ: [Baobab agency profile](https://pro-baobab.jp/actor/%E5%86%A8%E6%A8%AB-%E3%81%8B%E3%81%9A%E3%81%BF/).
- Shunsuke Sakuya / 咲野俊介: [Osawa agency profile](https://osawa-inc.co.jp/men/sakuyashunsuke/).
- Kiyohito Yoshikai / 吉開清人: [voice actor reference](https://hibikiforum.net/index.php?title=Yoshikai_Kiyohito).

## Build and validation

The normal Library builder and its text collector share the same ACTR mapping.
Unknown credits stop the build for review. Legacy Japanese ACTR glyphs stay
reserved to avoid changing unrelated font allocations in existing builds.

For the existing local VWF candidate only:

```
python tools/patch_library_cv_candidate.py
python tools/patch_library_cv_candidate.py --write
python -m unittest discover -s tools -p test_library_cv.py -v
```

The dry run rebuilds and validates a temporary archive. Write mode backs up
`work/out_0.6.3/MTZKN_PT.CPK` to `work/library_cv.before.CPK` and changes ACTR
fields only, preserving character names, descriptions, VOIC and LOOK payloads.
The original source determines entry-to-actor identity. All member IDs, field
order and non-ACTR bytes are checked after rebuilding. Existing font mappings
are reused; names must fit a conservative 400px header budget at 32px type.
`work/library_cv_audit.json` records coverage, widths and archive hashes.

This does not install into RPCS3, rebuild a release or stamp a version.
In-game visual confirmation is still needed.

Validated 2026-09-12: 408 entries, 193 named credits / 153 distinct actors,
215 placeholders. Widest name is Tomomichi Nishimura, 340px at 32px type;
Haruna Ikezawa is 248px. Source CP932 aliases such as 日髙のり子 are matched
by decoded identity, not a potentially different re-encoded byte sequence.
