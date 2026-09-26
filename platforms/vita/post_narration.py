"""Source-bound post-prologue narration keys; leave timed records untouched."""
import struct
from category_port import require,digest
from narration_layout import KEYS

ARCHIVE='DATA/STAGE/STG0001b.cpk'
MEMBER=7
SOURCE_SHA='0d769d4248c68e072fcef0b0bdfb3a5eddfafc6c25a8d578696b3818df34b399'
BASE=20
STRIDE=88
COUNT=80


def source_records(data):
    require(digest(data)==SOURCE_SHA,'Post-prologue narration source changed')
    require(len(data)==BASE+STRIDE*COUNT and struct.unpack_from('<H',data)[0]==COUNT,
            'Post-prologue native record grid changed')
    rows={}
    for off in range(BASE,len(data),STRIDE):
        stop=data.find(b'\0',off,off+STRIDE)
        require(stop>=off,'Unterminated narration')
        if stop==off:continue
        jp=data[off:stop].decode('cp932')
        require(jp not in rows,'Duplicate narration source')
        rows[jp]=off
    require(set(rows)==set(KEYS),'Post-prologue narration inventory differs')
    return rows


def sources(port):
    archive=port.cpk(ARCHIVE)
    data=archive.read(next(e for e in archive.files if e['id']==MEMBER))
    rows=source_records(data)
    definitions=port.catalog.document('localization/messages/issue_hook.json')['messages']
    for jp in rows:
        mids=[mid for mid,row in definitions.items() if row.get('source')==jp]
        require(len(mids)==1,'Missing/duplicate shared narration translation')
        text=port.text(port.catalog.text(mids[0]))
        require(text and '\n' not in text and '\r' not in text and '$' not in text,
                'Narration must preserve timed row count')
        require(sum(port.widths[ch] for ch in text)<=900,'Narration exceeds screen margin')
    return rows
