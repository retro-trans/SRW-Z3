"""Preview/apply the reviewed Focus terminology migration; no general-dialogue sweep."""
import argparse,json,re
from pathlib import Path
import eboot,trdata

FILES=('tools/parts_description_catalog.py','tools/skill_description_catalog.py',
       'tools/weapon_requirements.py','translation/ability_hook.json',
       'translation/message_class_hook.json','translation/skills.json',
       'translation/spirit_hook.json','translation/ui_hook.json',
       'translation/voice_121.json')
BASE=Path('work/focus_hooks_before.json')
SOURCES=Path('work/focus_sources_before.json')


def renamed(path,text):
    # Voice 121 contains two instructional references to the actual stat.
    # Ordinary morale in character dialogue is deliberately not changed.
    if path.endswith('skills.json'):
        return text.replace('Morale+','Foc+').replace('MoraleBonus','Foc Bonus')
    return re.sub(r'\bMorale\b','Focus',text)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--snapshot',action='store_true')
    ap.add_argument('--write',action='store_true')
    a=ap.parse_args()
    if a.snapshot:
        assert not a.write and not BASE.exists() and not SOURCES.exists()
        trdata.use_glossary('analysis/glossary.json')
        BASE.write_text(json.dumps(eboot.load_ui_hook(),ensure_ascii=False),encoding='utf-8')
        SOURCES.write_text(json.dumps({p:Path(p).read_text(encoding='utf-8') for p in FILES},ensure_ascii=False),encoding='utf-8')
        print('Saved pre-Focus hook and source baselines.')
        return
    originals=json.loads(SOURCES.read_text(encoding='utf-8'))
    for p,text in originals.items():
        new=renamed(p,text)
        assert Path(p).read_text(encoding='utf-8')==text,'Already changed: '+p
        print(p,':',text.count('Morale'),'occurrences')
        if a.write:Path(p).write_text(new,encoding='utf-8')


if __name__=='__main__':main()
