"""Patch the UI string pool (AIDDATAPACK.CPK member 0) in place.

Invoked automatically by VWF build_project.py builds, which produce pairs.json -- the letter
mapping this shares, so UI text uses the same VWF cells as everything else. No
atlas change is needed: the 79 letter cells already cover ASCII.

Strings are written in place and never longer than the original, because how
the pool is referenced is still unknown -- no offset table was found for it.
That caps what can be translated. The scenario-select screen fits (6-14 cells
a string). The protagonist sheet (1-4 cells: 姓 is ONE cell) does not, and
cannot until the reference mechanism is decoded. The battle COMMAND list is
not in this member at all: it is a UTF-8 string table in the EBOOT
(eboot.command_labels, translation/ui_eboot.json).

    python tools/build_ui.py [--disc <USRDIR>] [--out work/out]
"""
import argparse
import io
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aiddata            # noqa: E402
import cpkpatch           # noqa: E402
import digraph as dg      # noqa: E402
from cpk import CPK       # noqa: E402

NAME = "AIDDATAPACK.CPK"
SUB = "DATA/AIDDATA"
MEMBER = 0


def load_mapping(out):
    p = os.path.join(out, "pairs.json")
    if not os.path.exists(p):
        raise SystemExit("%s missing -- run build_project.py first" % p)
    m = json.load(open(p, encoding="utf-8"))
    return {(k if len(k) == 1 else (k[0], k[1])): v for k, v in m.items()}


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--disc", default="E:/SRWZ3/PS3_GAME/USRDIR")
    ap.add_argument("--out", default="work/out")
    ap.add_argument("--trans", default="translation/ui_aiddata.json")
    ap.add_argument("--ttf",
                    default="E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF")
    a = ap.parse_args(argv[1:])

    # This builder runs in a separate process; it cannot inherit the parent
    # builder's glossary. Widget text may contain canonical $$term$$ tokens.
    import trdata
    trdata.use_glossary('analysis/glossary.json')

    # Read from the pristine cache, NOT the disc: deploy.py overwrites the
    # disc copy, so on the second run the Japanese source strings are already
    # English and every translation silently drops out. That happened once and
    # cost the scenario-select text.
    cache = os.path.join("work", "orig", NAME)
    src = cache if os.path.exists(cache) else os.path.join(a.disc, SUB, NAME)
    if not os.path.exists(src):
        raise SystemExit("%s not found" % src)
    if src != cache:
        os.makedirs(os.path.dirname(cache), exist_ok=True)
        import shutil
        shutil.copy2(src, cache)
        src = cache
        print("  [ui]   cached a pristine %s" % NAME)
    dg.use_letters(a.ttf, cap=22, dilate=0.5)
    mapping = load_mapping(a.out)
    doc = json.load(open(a.trans, encoding="utf-8"))

    k = CPK(src)
    blob = k.read(k.files[MEMBER])
    # expand each entry to every occurrence of that exact Japanese string
    byjp = {}
    for off, t, nb, _slack in aiddata.strings(blob):
        byjp.setdefault(t, []).append((off, nb))
    edits = []
    for row in doc["lines"]:
        for off, _nb in byjp.get(row["jp"], []):
            edits.append({"off": off, "en": row["en"]})
    # slots too small for one-letter-per-cell: encode with PAIR cells instead
    tightp = "translation/ui_tight.json"
    tight = []
    if os.path.exists(tightp):
        for row in json.load(open(tightp, encoding="utf-8"))["lines"]:
            for off, _nb in byjp.get(row["jp"], []):
                tight.append({"off": off, "en": row["en"], "pairs": True})
    missing = [r["jp"] for r in doc["lines"] if r["jp"] not in byjp]
    if missing:
        raise SystemExit("source strings not found (already patched source?): %s"
                         % ", ".join(missing))
    if not edits:
        raise SystemExit("no strings matched -- is the pool the expected one?")

    new, done = aiddata.apply(blob, edits, mapping)
    new, team_done = aiddata.team_label_fragments(new, mapping)
    done.extend(team_done)
    new, roster_team_done = aiddata.roster_team_overlay(new, mapping)
    done.extend(roster_team_done)
    new, resupply_done = aiddata.roster_resupply_headers(new, mapping)
    done.extend(resupply_done)
    probs = aiddata.verify(blob, new, done)
    for q in probs:
        print("  PROBLEM (in place) %s" % q)
    if probs:
        return 1
    staged = new
    # repointed strings: appended past the end, references rewritten, so the
    # English is not limited by the Japanese it replaces
    rp = "translation/ui_repoint.json"
    moved = []
    if os.path.exists(rp):
        red = []
        for row in json.load(open(rp, encoding="utf-8"))["lines"]:
            for off, _nb in byjp.get(row["jp"], []):
                red.append({"off": off, "en": row["en"]})
        new, moved, unref = aiddata.repoint(staged, red, mapping)
        if unref:
            raise SystemExit("no widget record references: %s"
                             % ", ".join(r["en"] for r in unref))
        probs = aiddata.verify_repoint(staged, new, moved, mapping)
        for q in probs:
            print("  PROBLEM (repoint) %s" % q)
        if probs:
            return 1
    if tight:
        new, done2 = aiddata.apply(new, tight, mapping, pairs=True)
        done = done + done2
    import search_layout
    new = search_layout.tabs(new, mapping)
    import command_layout
    new = command_layout.funds_colon(new)
    widths = {int(k): v for k,v in json.load(open(os.path.join(a.out, 'widths.json'))).items()}
    new = command_layout.split_labels(new, mapping, widths)
    import trader_ui
    trader_before = new
    new = trader_ui.apply(new, mapping, widths)
    trader_ui.verify(trader_before, new, mapping, widths)
    import battle_preview_layout
    new = battle_preview_layout.apply(new, mapping, widths)
    import roster_settings_layout
    new = roster_settings_layout.apply(new, mapping, widths)
    import intermission_layout
    new = intermission_layout.apply(new, mapping, widths)
    import pilot_swap_alignment
    new = pilot_swap_alignment.apply(new)
    import record_screen_labels
    new = record_screen_labels.apply(new,mapping,widths,blob)
    import naming_search_layout
    new = naming_search_layout.apply(new, mapping, widths)
    import name_entry_labels
    new = name_entry_labels.apply(new, mapping, widths)
    import team_order_labels
    new = team_order_labels.apply(new, mapping, widths)
    import team_roster_layout
    new = team_roster_layout.apply(new, mapping, widths)
    import map_popup_layout
    new = map_popup_layout.apply(new, mapping, widths)
    import support_popup_layout
    new = support_popup_layout.apply(new)
    support_popup_layout.verify(blob,new)
    import tag_reward_layout
    new = tag_reward_layout.apply(new, mapping, widths)
    import search_list_headers
    new = search_list_headers.apply(new,mapping,widths)
    import weapon_info_layout
    new = weapon_info_layout.apply(new,mapping,widths)
    import map_weapon_info
    map_weapon_info.check_source(Path('work/EBOOT_dec.elf').read_bytes(),blob)
    new = map_weapon_info.apply(new,mapping,widths,blob)
    import weapon_requirements
    new = weapon_requirements.apply(new,mapping,widths)
    import battle_screen_labels
    new = battle_screen_labels.apply(new,mapping,widths)
    import mech_info_layout
    new = mech_info_layout.apply(new,mapping,widths)
    import upgrade_list_labels
    new = upgrade_list_labels.apply(new,mapping,widths)
    import combat_record_links
    new = combat_record_links.apply(new,mapping,widths)
    import ui_followup_layout
    new = ui_followup_layout.apply(new, mapping, widths)
    import battle_reports
    new = battle_reports.apply(new, mapping, widths)
    import deployment_layout
    new = deployment_layout.apply(new, mapping, widths)
    import deployment_menu_text
    new = deployment_menu_text.apply(new,mapping,widths)
    import aboard_order_labels
    new = aboard_order_labels.apply(new,mapping,widths,blob)
    import song_deployment_labels
    new = song_deployment_labels.apply(new,mapping,widths,blob)
    import command_swap_labels
    new = command_swap_labels.apply(new,mapping,widths,blob)
    import trader_spirit_prompts
    new = trader_spirit_prompts.apply_ui(new,mapping,widths,blob)
    import pilot_spirit_layout
    new = pilot_spirit_layout.apply(new,mapping,widths,blob)
    import library_list_labels
    new = library_list_labels.apply(new,mapping,widths,blob)
    import save_prompt_layout
    new = save_prompt_layout.apply(new,mapping)
    import menu_followup
    new = menu_followup.apply(new,mapping,widths,blob)
    import training_help_layout
    new = training_help_layout.apply(new,mapping,widths,blob)
    import parts_menu_followup
    new = parts_menu_followup.apply(new,mapping,widths,blob)
    import unit_info_currency
    new = unit_info_currency.apply(new,mapping,widths,blob)
    import startup_menu_layout
    new = startup_menu_layout.apply_ui(new)
    tmp = os.path.join(a.out, "aiddata.member")
    open(tmp, "wb").write(new)
    dst = os.path.join(a.out, NAME)
    import attack_heading
    art_original = k.read(next(f for f in k.files if f['id'] == 1))
    art = attack_heading.apply(art_original, a.ttf)
    attack_heading.verify(art_original, art, a.ttf)
    import trader_art
    trader_art_before = art
    art = trader_art.apply(art, a.ttf)
    trader_art.verify(trader_art_before, art, a.ttf)
    art = startup_menu_layout.apply_art(art)
    art_tmp = os.path.join(a.out, 'aiddata.attack.member')
    open(art_tmp, 'wb').write(art)
    cnt, csz = cpkpatch.build(src, dst, {k.files[MEMBER]["id"]: tmp, 1: art_tmp})
    os.remove(art_tmp)
    os.remove(tmp)
    print("  [ui]   %s member %d: %d strings in %d places%s%s"
          % (NAME, MEMBER, len(doc["lines"]), len(edits),
             "" if not tight else " (+%d on pair cells)" % len(tight),
             "" if not moved else
             ", %d repointed, +%d B" % (len(moved), len(new) - len(blob))))
    print("  [ui]   %s  %d members, %d B" % (NAME, cnt, csz))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
