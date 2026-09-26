"""Native Vita opening narration: fixed text slots, NOT stage Lua dialogue.

The native member is7 (PS3 uses6). Locate the shared Japanese identities in
the verified Vita record grid. Preserve headers, timings, record tails and
even unused bytes after the new terminator; never pad a whole record.
"""
import struct
from category_port import require,digest,encoded
from prepare_vwf import line_widths

ARCHIVE='DATA/STAGE/STG0001a.cpk'
MEMBER=7
SOURCE_SHA256='88c8525bfa287ca31c250c7e767f6259aa995381f831088f01929a5d86dfcc8d'
GROUP='narration_0001a'
BASE=20
STRIDE=84
COUNT=95
CAP=52


def source_records(data):
    require(digest(data)==SOURCE_SHA256,'Opening narration source changed')
    require(len(data)==BASE+STRIDE*COUNT and struct.unpack_from('<H',data)[0]==COUNT,
            'Unknown native narration record grid')
    rows={}
    for off in range(BASE,len(data),STRIDE):
        stop=data.find(b'\0',off,off+STRIDE)
        require(stop>=off,'Unterminated native narration record')
        if stop==off:continue
        raw=data[off:stop];jp=raw.decode('cp932')
        require(jp not in rows,'Duplicate opening narration identity')
        rows[jp]=off
    require(len(rows)==28 and max(len(jp.encode('cp932')) for jp in rows)==CAP,
            'Native narration inventory or measured capacity changed')
    return rows


def apply(data,port):
    native=source_records(data)
    definitions=port.catalog.document('localization/messages/'+GROUP+'.json')['messages']
    messages={}
    for mid,row in definitions.items():
        # Expanded legacy mirrors are not independent translation records.
        if row.get('context',{}).get('variant')=='expanded':continue
        jp=row.get('source')
        require(jp and jp not in messages,'Missing/duplicate shared narration source')
        messages[jp]=mid
    require(set(native)==set(messages),'Shared/native opening narration inventory differs')
    out=bytearray(data);allowed=set();audit=[]
    for jp,off in sorted(native.items(),key=lambda pair:pair[1]):
        mid=messages[jp];text=port.text(port.catalog.text(mid))
        require(text and '\n' not in text and '\r' not in text and '$' not in text,
                'Narration must remain one fully expanded timed row')
        payload=encoded(text,port.mapping)
        require(len(payload)<=CAP,'Narration exceeds measured 52-byte text capacity: '+mid)
        width=max(line_widths(text,port.widths))
        require(width<=26*32,'Narration exceeds native 26-cell width budget: '+mid)
        require(not any(data[off+len(jp.encode('cp932')):off+len(payload)+1]),
                'Narration translation would overwrite nonzero record fields')
        out[off:off+len(payload)+1]=payload+b'\0'
        allowed.update(range(off,off+len(payload)+1))
        audit.append(dict(message=mid,record=(off-BASE)//STRIDE,offset=off,
                          encoded_bytes=len(payload),width_texels=width))
    require(len(out)==len(data) and all(a==b or i in allowed for i,(a,b) in enumerate(zip(data,out))),
            'Narration changed non-text bytes')
    return bytes(out),dict(status='native_opening_narration_verified',archive=ARCHIVE,member=MEMBER,
        records=len(audit),source_sha256=SOURCE_SHA256,sha256=digest(out),rows=audit,
        text_capacity_bytes=CAP,timing_controls_and_record_tails_preserved=True,runtime_tested=False)


def prepare(port):
    cpk=port.cpk(ARCHIVE)
    original=cpk.read(next(e for e in cpk.files if e['id']==MEMBER))
    changed,audit=apply(original,port)
    port.emit(ARCHIVE,MEMBER,changed)
    return audit
