"""Exercise the exact name-join byte stores and all six reported pilot names."""
import json
from pathlib import Path
import struct
import sys
import unittest

from cpk import CPK
import digraph
import eboot
import rpw
import status_name_separator as separator

ROOT = Path('work/build_0.6.24_english_20260930')


def run_join(code, prefix):
    regs = [0x100000+i*0x1000 for i in range(32)]
    regs[3],regs[27],regs[29] = len(prefix),0x200000,0
    before = regs[:]
    memory = dict(enumerate(prefix+b'\0'*4,regs[27]))
    # Execute the exact eight instructions, including the unmodified pointer
    # load and address operations. No unrecognized instructions are skipped.
    for w, in struct.iter_unpack('>I',code):
        op,t,a,b = w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
        imm = (w&65535)- (65536 if w&32768 else 0)
        if op==14:
            regs[t]=(regs[a] if a else 0)+imm
        elif w==0x8082e618:
            regs[4]=0x7208b0
        elif w==0x7c63da14:
            regs[3]+=regs[27]
        elif w==0x78630020:
            regs[3]&=0xffffffff
        elif op==38:
            address=regs[a]+imm
            assert before[27]+len(prefix)<=address<=before[27]+len(prefix)+2
            memory[address]=regs[t]&255
        else:
            raise AssertionError(hex(w))
    assert all(regs[i]==before[i] for i in set(range(32))-{0,3,4,9})
    return bytes(memory[before[27]+i] for i in range(len(prefix)+3))


class StatusNameSeparatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping=json.loads((ROOT/'pairs.json').read_text())
        cls.before=(ROOT/'EBOOT.BIN').read_bytes()
        cls.after=separator.patch(cls.before,cls.mapping)
        cls.terms=json.loads(Path('analysis/glossary.json').read_text(encoding='utf8'))['terms']
        k=CPK('work/lib/RPW_DATA.CPK');cls.rpw=k.read(k.files[0])

    def test_three_western_names_exact_join(self):
        override,_=rpw.piece_overrides(self.rpw,self.terms)
        js=rpw.jstrings(self.rpw); slots=rpw.slots(self.rpw)
        names={225:'Heero Yui',251:'Heero Yui',234:'Zechs Marquise',257:'Zechs Marquise',
               356:'Otto Mitas',357:'Otto Mitas',414:'Otto Mitas'}
        code=separator.expected(self.mapping)
        for rec,full in names.items():
            with self.subTest(rec=rec):
                # Reported pilots use identical short/given strings in col0/2.
                self.assertEqual(js[slots['pilot-nw',rec,0]],js[slots['pilot-nw',rec,2]])
                first=digraph.encode_mixed(override['pilot-nw',rec,0],self.mapping)
                last=digraph.encode_mixed(override['pilot-nw',rec,1],self.mapping)
                self.assertEqual(run_join(separator.SOURCE,first),first+b'\x81\x45\0')
                self.assertEqual(run_join(code,first)[:-1]+last,
                                 digraph.encode_mixed(full,self.mapping))

    def test_three_surname_first_names_already_covered(self):
        override=rpw.surname_first_overrides(self.rpw,self.terms)
        for rec,full in {2:'Kakikouji Umemaro',15:'Kakikouji Umemaro',
                         3:'Atsui Tetsuo',17:'Atsui Tetsuo',
                         4:'Kinoshita Touhachirou',16:'Kinoshita Touhachirou'}.items():
            self.assertEqual(override['pilot-nw',rec,1]+override['pilot-nw',rec,2],full)
            self.assertNotIn(('pilot-nw',rec,0),override)

    def test_two_immediates_only_and_source_guards(self):
        segs=eboot._segments(self.before)
        allowed={eboot._off(segs,site)+i for site in separator.SITES for i in (2,3)}
        self.assertEqual(len(self.before),len(self.after))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.before,self.after))))
        for i in range(len(separator.SOURCE)):
            bad=bytearray(self.before);bad[eboot._off(segs,separator.START)+i]^=1
            with self.assertRaises(AssertionError):separator.patch(bad,self.mapping)

    def test_folded_hardware_layout(self):
        sys.path.insert(0,'platforms/ps3')
        import cfw_loader_layout
        import ppc_permissions
        folded=cfw_loader_layout.fold(self.after)
        separator.check(folded,self.mapping)
        pristine=Path('work/EBOOT_dec.elf').read_bytes()
        for blob in (self.after,folded):
            ppc_permissions.check_changed_branches(pristine,blob)


if __name__=='__main__':unittest.main()
