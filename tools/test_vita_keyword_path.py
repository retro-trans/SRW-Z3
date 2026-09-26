"""Execute native linked-piece path through copy and drawing dispatch."""
import struct
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import vwf
from inspect_vwf import load
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *


def run_keyword(candidate, text, column=0, row=0):
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x81000000,0x6A0000)
    info=vwf.parse(candidate)
    for i in (0,1):
        off,n=info['infos'][i][:2];u.mem_write(info['phdrs'][i][2],candidate[off:off+n])
    u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
    u.reg_write(UC_ARM_REG_SP,0x208000);u.reg_write(UC_ARM_REG_LR,0x200001)
    u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20);u.reg_write(UC_ARM_REG_FPEXC,1<<30)
    def put(p,*words):u.mem_write(p,struct.pack('<'+'I'*len(words),*words))
    u.mem_write(0x201000,text+b'\0');put(0x202000,0x201000,len(text))
    put(0x203004,0x204000);u.mem_write(0x20409c,struct.pack('<hh',20,30))
    u.mem_write(0x2040aa,bytes((24,24)))
    u.mem_write(0x205000,'《'.encode('cp932')+b'\0');u.mem_write(0x205010,'》'.encode('cp932')+b'\0')
    put(0x8132c03c,0x205000,0x205010);put(0x208000,row)
    for reg,val in ((UC_ARM_REG_R0,0x203000),(UC_ARM_REG_R1,0),
                    (UC_ARM_REG_R2,0x202000),(UC_ARM_REG_R3,column)):u.reg_write(reg,val)
    def cstr(p):
        out=bytearray()
        while bytes(u.mem_read(p+len(out),1))!=b'\0':out+=u.mem_read(p+len(out),1)
        return bytes(out)
    draws=[]
    def external(cpu,address,size,data):
        if address==0x8121dc30:cpu.reg_write(UC_ARM_REG_R0,len(cstr(cpu.reg_read(UC_ARM_REG_R0))))
        elif address==0x8121dc80:
            cpu.mem_write(cpu.reg_read(UC_ARM_REG_R0),bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R1),cpu.reg_read(UC_ARM_REG_R2))))
        elif address==0x810d9f92:
            draws.append((cstr(cpu.reg_read(UC_ARM_REG_R0)),cpu.reg_read(UC_ARM_REG_R2),
                          cpu.reg_read(UC_ARM_REG_R3)))
        elif address not in (0x810d8b1e,0x810d8cd8):return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE,external);u.emu_start(0x810da18b,0x200000,count=20000)
    return draws,u.reg_read(UC_ARM_REG_R0)


class KeywordPathTests(unittest.TestCase):
    def test_linked_native_piece_reaches_draw(self):
        original,_=load();candidate,_=vwf.patch(original,bytes([16]*192))
        body=bytes.fromhex('874187428743');text='《'.encode('cp932')+body+'》'.encode('cp932')
        for row in range(4):
            self.assertEqual(run_keyword(original,text,2,row),([(body,68,30+24*row)],len(body)))
            self.assertEqual(run_keyword(candidate,text,1280,row),([(body,30,30+24*row)],len(body)))


if __name__=='__main__':unittest.main()
