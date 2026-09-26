"""Exact composed headings from the pinned Vita title/episode metadata."""
import struct
import unicodedata
from inspect_vwf import segment
from category_port import require
import episode_heading_hooks as shared

TITLES=0x81328CA4
RECORDS=0x813291A4


def hooks(executable,info,catalog):
    text,tbase=segment(executable,info,0);data,dbase=segment(executable,info,1)
    translations={unicodedata.normalize('NFKC',r['Japanese']):r['English'] for r in shared.scenario_title.ROWS}
    translations.update({unicodedata.normalize('NFKC',jp):en for jp,en in shared.EXTRA.items()})
    titles=[]
    for i in range(159):
        p=struct.unpack_from('<I',data,TITLES-dbase+i*4)[0]-tbase
        require(0<=p<len(text),'Native title pointer outside text')
        jp=text[p:text.index(b'\0',p)].decode('cp932');key=unicodedata.normalize('NFKC',jp)
        require(key in translations,'Native title has no shared translation')
        titles.append((jp,translations[key]))
    records=set()
    for i in range(181):
        at=RECORDS-dbase+i*32
        number,index=struct.unpack_from('<hh',data,at+14)
        if 0<=index<159:records.add((number,index))
    require((1,0) in records and (10,16) in records and titles[16][0]=='魔王の誘い',
            'Unexpected native episode identities')
    out={};template=catalog.text('ui.episode_heading_hooks:numbered_heading')
    for number,index in sorted(records):
        jp,en=titles[index]
        if number>0:
            for digits in {str(number),str(number).zfill(2)}:
                wide=digits.translate(str.maketrans('0123456789','０１２３４５６７８９'))
                out['第'+wide+'話『'+jp+'』']=template.format(number=number,title=en)
        if number<0:out['『'+jp+'』']='『'+en+'』'
        for match,source,label in ((number==60,'最終話','final_label'),
                                   (number==61,'エピローグ','epilogue_label'),
                                   (100<=index<=121,'分岐シナリオ','route_label')):
            if match:out[source+'『'+jp+'』']=catalog.text('ui.episode_heading_hooks:'+label)+' 『'+en+'』'
    return out
