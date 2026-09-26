"""Only the 28 descriptive lines used by the two System Settings pages."""
import json
from pathlib import Path

def rows():
    data = json.loads(Path('translation/ui_utf8.json').read_text(encoding='utf-8'))['lines']
    first = next(i for i,r in enumerate(data) if r['jp']=='音声ボリュームを設定します。')
    last = next(i for i,r in enumerate(data) if r['jp']=='戦闘アニメ終了時にＢＧＭをマップ曲に戻します。')
    result = data[first:last+1]
    assert len(result)==28
    return result

LABELS = tuple(r['en'] for r in rows())
