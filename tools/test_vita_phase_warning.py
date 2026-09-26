"""Exercise the original remaining-team formatter with its actual count input."""
import sys,unittest,gc,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
from inspect_vwf import load,segment
from self_decrypt import parse
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *
import phase_warning as warning


def native_lines(executable,counts):
    gc.collect()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
    text,base=segment(executable,parse(executable),0)
    u.mem_map(base,(len(text)+4095)//4096*4096);u.mem_write(base,text)
    u.mem_map(0x200000,0x10000)
    def string(ptr):
        raw=bytes(u.mem_read(ptr,256));return raw[:raw.index(b'\0')]
    def external(cpu,address,size,data):
        if address not in (0x8121DC20,0x8121DA10,0x8121DC80):return
        dst,src=cpu.reg_read(UC_ARM_REG_R0),cpu.reg_read(UC_ARM_REG_R1)
        if address==0x8121DC80:
            payload=bytes(cpu.mem_read(src,cpu.reg_read(UC_ARM_REG_R2)))
        else:
            if address==0x8121DA10:dst+=len(string(dst))
            payload=string(src)+b'\0'
        cpu.mem_write(dst,payload)
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE,external)
    rows=[]
    for count in counts:
        u.mem_write(0x208000,b'X'*0x400)
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        u.reg_write(UC_ARM_REG_SP,0x208000)
        u.reg_write(UC_ARM_REG_R0,count&0xffffffff)
        u.emu_start(0x8100A095,warning.END,count=2000)
        assert u.reg_read(UC_ARM_REG_PC)==warning.END
        rows.append((string(0x208014),string(0x208114)))
    return rows


def native_center(executable,key,mode):
    gc.collect()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
    info=parse(executable)
    for i in (0,1):
        data,base=segment(executable,info,i)
        u.mem_map(base,(len(data)+4095)//4096*4096);u.mem_write(base,data)
    u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
    u.reg_write(UC_ARM_REG_SP,0x208000);u.reg_write(UC_ARM_REG_LR,0x200001)
    u.reg_write(UC_ARM_REG_C1_C0_2,0xf<<20);u.reg_write(UC_ARM_REG_FPEXC,1<<30)
    state=0x8138AA58;u.mem_write(state,bytes(0x78))
    u.mem_write(state+0x14,struct.pack('<f',32));u.mem_write(state+0x1c,struct.pack('<f',31))
    u.mem_write(0x201000,key+b'\0');u.reg_write(UC_ARM_REG_R0,0x201000)
    u.reg_write(UC_ARM_REG_R1,mode);u.reg_write(UC_ARM_REG_R2,0)
    for reg,value in ((UC_ARM_REG_S0,640),(UC_ARM_REG_S1,200),(UC_ARM_REG_S2,0)):
        u.reg_write(reg,struct.unpack('<I',struct.pack('<f',value))[0])
    positions=[]
    def external(cpu,address,size,data):
        if address==0x8121DC30:cpu.reg_write(UC_ARM_REG_R0,len(key))
        elif address==0x8121DA90:cpu.reg_write(UC_ARM_REG_R0,len(key.decode('utf-8')))
        elif address==0x81006E10:
            positions.append(struct.unpack('<f',struct.pack('<I',cpu.reg_read(UC_ARM_REG_S0)))[0])
        else:return
        cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
    u.hook_add(UC_HOOK_CODE,external)
    u.emu_start(0x8100791F,0x200000,count=100000)
    assert u.reg_read(UC_ARM_REG_PC)==0x200000
    assert u.reg_read(UC_ARM_REG_SP)==0x208000
    return positions


class PhaseWarningTests(unittest.TestCase):
    def test_native_count_composition_and_plain_prompt(self):
        executable,_=load()
        counts=[-1,0]+list(range(1,101))+[106,199,999]
        for count,(first,second) in zip(counts,native_lines(executable,counts)):
            if count<=0:
                self.assertEqual(first,'フェイズを終了します。'.encode('cp932'))
                self.assertEqual(second,'よろしいですか？'.encode('cp932'))
            else:
                digits=str(count%100).translate(str.maketrans('0123456789',warning.DIGITS))
                self.assertEqual(first,(warning.PREFIX+digits+warning.SUFFIX).encode('cp932'))
                self.assertEqual(second,'フェイズを終了しますか？'.encode('cp932'))


if __name__=='__main__':unittest.main()
