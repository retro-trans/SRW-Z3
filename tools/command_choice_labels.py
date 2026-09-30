"""Canonical Tactical/Tag choices across FSSA, CP932 and live UTF-8 tables."""
import struct
import localization

TACTICS=('attack','defense','assault')
TAGS=('multi','pp','chips','sp')
UTF8=(('attack_help',0x6ea3b0,0x780578),('defense_help',0x6ea3e0,0x78057c),
      ('assault_help',0x6ea408,0x780580),('multi',0x6ea448,0x780584),
      ('pp',0x6ea468,0x780588),('chips',0x6ea480,0x78058c),('sp',0x6ea4a0,0x780590))

def wording(key):
    cat=localization.english();mid='ui.tag_reward_layout:'+key
    return cat.definition(mid)['source'],cat.text(mid)

def choices(keys,bullet=True,source=False):
    return '\n'.join(('・' if bullet else '')+wording(k)[0 if source else 1] for k in keys)

def hooks():
    return dict(wording(k) for k in TACTICS+TAGS)

def utf8_labels():
    return {('・' if key in TAGS else '')+wording(key)[0]:
            ('・' if key in TAGS else '')+wording(key)[1] for key,_,_ in UTF8}

def check_source(blob):
    import eboot
    segs=eboot._segments(blob);labels=utf8_labels()
    low=segs[1]['off'];high=low+segs[1]['filesz']
    for (key,va,ref),jp in zip(UTF8,labels):
        assert eboot._cstr(blob,eboot._off(segs,va))==jp.encode('utf8'),key
        actual=[p for p in range(low,high-3,4) if struct.unpack_from('>I',blob,p)[0]==va]
        assert actual==[ref],(key,actual)

def check_built(blob,mapping,widths):
    import eboot
    from intermission_layout import ink
    segs=eboot._segments(blob)
    for (key,_,ref),en in zip(UTF8,utf8_labels().values()):
        expected=''.join(chr(eboot.VWF_CP_BASE+ord(c)) if 32<=ord(c)<127 else c for c in en).encode('utf8')
        va=struct.unpack_from('>I',blob,ref)[0]
        assert eboot._cstr(blob,eboot._off(segs,va))==expected,key
        assert ink(en,mapping,widths,31)<(280 if key in TAGS else 880),(key,en)
