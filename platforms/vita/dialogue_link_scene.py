"""Normal dialogue lacks the explicit scene context used by the backlog."""
import vwf
from category_port import require

SITE=0x810D8D86
CAVE=0x810D6A64  # 18 unused bytes after the existing comparison helper


def stub():
    raw=vwf.assemble('''
        push {r1,lr}
        ldr r0,[r0,#4]
        cbnz r0,done
        bl 0x810d6dc8
        ldr r0,[r0,#12]
    done:
        pop {r1,pc}
    ''',CAVE)
    require(CAVE+len(raw)<=0x810d6a76,'Scene helper overlaps secondary return')
    return raw


def apply(text,base):
    require(text[0x810d5158-base:0x810d5158-base+4]==vwf.assemble('ldr r0,[r0,#4]; bx lr',0x810d5158),'Context getter differs')
    raw=stub(); edits=[]
    for at,old,new in ((SITE,vwf.assemble('bl 0x810d5158',SITE),vwf.assemble('bl %d'%CAVE,SITE)),
                       (CAVE,vwf.assemble('nop',0)*(len(raw)//2),raw)):
        require(text[at-base:at-base+len(old)]==old,'Dialogue scene guard '+hex(at))
        edits.append((at,old)); text[at-base:at-base+len(new)]=new
    return edits
