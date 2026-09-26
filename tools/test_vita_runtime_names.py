"""Run the native name constructor and the relocated default-name adapter."""
import sys,struct,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
from category_port import Port,encoded
from inspect_vwf import load
import ui_text,vwf,runtime_names_vita
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *


class NameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port=Port();cls.names=runtime_names_vita.rows(cls.port)
        cls.original,cls.old=load()
        cls.candidate,cls.audit=ui_text.patch(cls.original,cls.port.width_bank,
            {'修理'.encode('cp932'):encoded('Repair',cls.port.mapping)},name_rows=cls.names)

    def machine(self,text_shift=0,data_shift=0):
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);info=vwf.parse(self.candidate)
        for i,shift in ((0,text_shift),(1,data_shift)):
            p=info['phdrs'][i];off,size=info['infos'][i][:2]
            u.mem_map(p[2]+shift,((size+4095)//4096)*4096)
            u.mem_write(p[2]+shift,self.candidate[off:off+size])
        # Apply all newly appended relocations with independent segment bases.
        off,size=info['infos'][3][:2];old_size=self.old['infos'][3][1]
        for at in range(off+old_size,off+size,12):
            tag,addend,patch=struct.unpack_from('<III',self.candidate,at)
            self.assertEqual(tag,0x310)
            address=info['phdrs'][0][2]+text_shift+patch
            target=info['phdrs'][1][2]+data_shift+addend
            u.mem_write(address,struct.pack('<I',(target-address)&0xffffffff))
        u.mem_map(0x200000,0x10000)
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        u.reg_write(UC_ARM_REG_SP,0x208000)
        u.reg_write(UC_ARM_REG_C1_C0_2,0xf<<20);u.reg_write(UC_ARM_REG_FPEXC,1<<30)
        def external(cpu,address,size,data):
            if address not in (0x8121DC20+text_shift,0x8121DA10+text_shift):return
            dst,src=cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)
            if address==0x8121DA10+text_shift:dst+=len(self.string(cpu,dst))
            cpu.mem_write(dst,self.string(cpu,src)+b'\0')
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        u.hook_add(UC_HOOK_CODE,external)
        return u

    def string(self,u,p):
        out=bytearray()
        while True:
            b=bytes(u.mem_read(p+len(out),1))
            if b==b'\0':return bytes(out)
            out+=b
            self.assertLess(len(out),256)

    def test_exact_names_custom_names_and_independent_relocation(self):
        for ts,ds in ((0,0),(0x1000000,0x2000000),(0x2000000,0x1000000)):
            u=self.machine(ts,ds)
            for text in list(self.names)+[s.encode('cp932') for s in ('修理','ヒビキ改','アキラ','カミシロＡ','')]:
                u.mem_write(0x201000,text+b'\0');u.mem_write(0x202000,b'X'*48)
                u.reg_write(UC_ARM_REG_R0,0x202000);u.reg_write(UC_ARM_REG_R1,0x201000)
                u.reg_write(UC_ARM_REG_R7,123);u.reg_write(UC_ARM_REG_LR,0x200001)
                u.reg_write(UC_ARM_REG_S0,0x42aa0000)
                u.emu_start((int(self.audit['runtime_names']['wrapper_address'],16)+ts)|1,0x200000,count=20000)
                expected=self.names.get(text,text)
                self.assertEqual(self.string(u,0x202000),expected)
                self.assertEqual(bytes(u.mem_read(0x202000+len(expected)+1,47-len(expected))),b'X'*(47-len(expected)))
                self.assertEqual(self.string(u,0x201000),text)
                self.assertEqual(u.reg_read(UC_ARM_REG_R7),123)
                self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
                self.assertEqual(u.reg_read(UC_ARM_REG_S0),0x42aa0000)

    def test_native_constructor_both_orders_and_untouched_saved_names(self):
        for order in (0,1):
            u=self.machine()
            for ptr,name in ((0x815FEB02,'ヒビキ'),(0x815FEB17,'カミシロ'),(0x815FEB2E,'ヒビキ')):
                u.mem_write(ptr,name.encode('cp932')+b'\0')
            u.mem_write(0x815FEB01,bytes([order]))
            before=bytes(u.mem_read(0x815FE9C0,0x200))
            u.mem_write(0x203000,b'X'*0x300);u.reg_write(UC_ARM_REG_R0,0x203000)
            u.reg_write(UC_ARM_REG_LR,0x200001)
            u.emu_start(0x810CBE19,0x810CBF4A,count=50000)
            for off,en in ((0x2d,'Hibiki'),(0x7f,'Hibiki'),(0xd1,'Kamishiro'),
                           (0x1c7,'Kamishiro Hibiki' if order else 'Hibiki Kamishiro')):
                self.assertEqual(self.string(u,0x203000+off),encoded(en,self.port.mapping))
                self.assertEqual(bytes(u.mem_read(0x203000+off+40,1)),b'X')
            self.assertEqual(bytes(u.mem_read(0x815FE9C0,0x200)),before)


if __name__=='__main__':unittest.main()
