"""Exact stage GIFT report messages, including explicitly paired draw lines.

Do not edit stage logic or repack presets. Proper nouns use glossary markers;
part names come from the existing part-name database. The original line
boundaries are retained because Report draws and centers one line at a time.
"""
import localization as _l10n
import argparse,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
HOOK=ROOT/'translation/gift_report_hook.json'
CONVERSIONS={'ラウンドムーバー':_l10n.literal('gift_reports.CONVERSIONS/0'),
             '軽量仕様':_l10n.literal('gift_reports.CONVERSIONS/1'),'強襲仕様':_l10n.literal('gift_reports.CONVERSIONS/2')}


def messages():
    out={}
    for jp,en in CONVERSIONS.items():
        out['スコープドッグ用　換装パーツ\n「'+jp+'」を入手しました。']=(
            '$$スコープドッグ$$ conversion equipment:\nReceived '+en+'.')
    parts=json.loads((ROOT/'translation/parts.json').read_text(encoding='utf-8'))
    for jp in ('補助ＧＮドライヴ','スーパーリペアキット','超合金Ｚ'):
        out['強化パーツ「'+jp+'」を入手しました。']='Received Power Part: '+parts[jp]+'.'
    out.update({
        '資金５００００を入手しました。':'Received 50,000 funds.',
        'インターミッションの『サブオーダー』が解禁になりました。':
            'Sub Orders are now available at Intermission.',
        'インターミッションの『Ｄトレーダー』が解禁になりました。':
            'D-Trader is now available at Intermission.',
        'ヤクト・ドーガ（ギュネイ）、ヤクト・ドーガ（クェス）に使用した改造費用は\n払い戻されました':
            'Upgrade costs for $$ヤクト・ドーガ$$ ($$ギュネイ$$/$$クェス$$)\nhave been refunded.',
        'ヤクト・ドーガ（ギュネイ）、ヤクト・ドーガ（クェス）、\nクシャトリヤに使用した改造費用は払い戻されました':
            'Upgrade costs for $$ヤクト・ドーガ$$ ($$ギュネイ$$/$$クェス$$) and\n$$クシャトリヤ$$ have been refunded.',
        'スペースキングキタンに使用した改造費用は\n払い戻されました':
            'Upgrade costs for $$スペースキングキタン$$\nhave been refunded.',
    })
    for lead,amounts in [('　',(50,100,150,200,1000)),('',(50,100,200,300,1000))]:
        for amount in amounts:
            wide=str(amount).translate(str.maketrans('0123456789','０１２３４５６７８９'))
            jp=lead+'ＡＧからのボーナス\n「Ｚチップ　'+wide+'Ｚ」を入手しました'
            out[jp]='Bonus from $$ＡＧ$$\nReceived {:,} Z Chips.'.format(amount)
    return out


def hooks():
    out=messages()
    for jp,en in list(out.items()):
        jlines,elines=jp.split('\n'),en.split('\n')
        assert len(jlines)==len(elines)
        if len(jlines)>1:
            for j,e in zip(jlines,elines):
                assert j not in out or out[j]==e
                out[j]=e
    return out


def centered_lines():
    # These existing lines already carry command_layout's live-pitch pads.
    # Never measure them again in the centered-drawer wrapper.
    padded={'　ＡＧからのボーナス','ＡＧからのボーナス'}
    padded.update('「Ｚチップ　'+n+'Ｚ」を入手しました' for n in ('１００','２００','１０００'))
    return tuple(jp for jp in hooks() if '\n' not in jp and jp not in padded)


def inventory(root=ROOT/'work'):
    found={}
    for path in sorted(root.glob('lua*/*preset.lua')):
        source=path.read_text(encoding='cp932')
        # Only actual MESSAGE strings inside GIFT tables, not Lua comments.
        source=re.sub(r'--[^\r\n]*','',source)
        for block in re.finditer(r'\bGIFT_\w+\s*=\s*\{(.*?)\}',source,re.S):
            for m in re.finditer(r'"((?:[^"\\]|\\.)*)"',block[1]):
                jp=m[1].replace('\\n','\n')
                if jp:found.setdefault(jp,[]).append(path.name)
    return found


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    found=inventory();catalog=messages()
    assert set(found)==set(catalog),(set(found)-set(catalog),set(catalog)-set(found))
    import trdata
    from intermission_layout import ink
    trdata.use_glossary(str(ROOT/'analysis/glossary.json'))
    out=ROOT/'work/out_0.6.3'
    mapping=json.loads((out/'pairs.json').read_text())
    widths={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}
    for jp,en in catalog.items():
        en=trdata._ex(en,str(HOOK))
        assert all(ink(line,mapping,widths,28)<=1000 for line in en.splitlines())
        print(en.replace('\n',' / '))
    rows=hooks()
    print('%d distinct reports / %d source occurrences / %d exact whole-and-line hooks.'%
          (len(found),sum(map(len,found.values())),len(rows)))
    if args.write:
        HOOK.write_text(json.dumps({'line_pairs':False,'lines':[
            {'jp':jp,'en':en} for jp,en in rows.items()]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
