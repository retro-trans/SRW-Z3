import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
import eboot
import key_help_labels as K
import training_help_layout as T
from intermission_layout import ink


class TrainingHelp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.12_approved_subtitle')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c=CPK('work/orig/AIDDATAPACK.CPK'); cls.source=c.read(c.files[0])
        cls.elf=Path('work/EBOOT_dec.elf').read_bytes()

    def test_ui_isolation_and_reference_tab(self):
        b=self.source;out=T.apply(b,self.mapping,self.widths,b)
        allowed={i for r in T.ROWS for i in range(r,r+4)}
        allowed.update(i for r in T.LEARN for i in range(r+4,r+8))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,out))))
        for r in (0xb5bf4,0xb5c14,0xb5c74,0xb5c94,0xb5ed4,0xb5ef4,0xb5e94):
            self.assertEqual(out[r:r+32],b[r:r+32])
        # Supplied capture's relative tab inset, within screenshot rounding.
        self.assertLess(abs((2006.5-1412)+T.LEARN_SHIFT*(2434/1280)-533.75),1)

    def test_complete_family_and_widths(self):
        labels=K.source_inventory(self.elf)
        loaded=eboot.load_commands(eboot.UI_UTF8_FILE)
        self.assertEqual(len(K.LABELS),91)
        for jp in labels[1:]:
            self.assertIn(jp,loaded)
            self.assertLess(ink(loaded[jp],self.mapping,self.widths,28),490)
        self.assertNotIn(labels[0],K.LABELS)
        self.assertEqual(loaded[K.SLOT_HELP_JP],K.SLOT_HELP_EN)

    def test_utf8_pointer_roundtrip_in_memory(self):
        # No package build or installed-file writes. Exercise the real UTF-8
        # patcher and verify each original Key Help pointer now reads English.
        source=self.elf; b=bytearray(source)
        eboot.add_segment(b);segs=eboot._segments(b)
        loaded=eboot.load_commands(eboot.UI_UTF8_FILE)
        labels={jp:loaded[jp] for jp in (*K.LABELS,*K.EXTRA)}
        expected=lambda s: ''.join(chr(eboot.VWF_CP_BASE+ord(c)) if 32<=ord(c)<127 else c for c in s).encode('utf8')+b'\0'
        result=eboot.command_labels(b,segs,labels,eboot._off(segs,eboot.NAME_STR),
                                   self.mapping,self.widths,window=False)
        self.assertFalse(result[2],result[2])
        start=source.index(K.START)+len(K.START);end=source.index(K.END,start)
        data=segs[1]
        for jp,en in labels.items():
            off=source.find(b'\0'+jp.encode('utf8')+b'\0',start,end)+1 if jp in K.LABELS else source.index(jp.encode('utf8'))
            self.assertGreaterEqual(off,0)
            raw=expected(en)
            va=eboot._va(segs,off);refs=[]
            for p in range(data['off'],data['off']+data['filesz'],4):
                if source[p:p+4]==struct.pack('>I',va):refs.append(p)
            self.assertTrue(refs,jp)
            for p in refs:
                target=eboot._off(segs,struct.unpack_from('>I',b,p)[0])
                self.assertEqual(b[target:target+len(raw)],raw,jp)
        dashes=source.index('－－－－－－－'.encode('utf8'),start,end)
        self.assertEqual(b[dashes:dashes+22],source[dashes:dashes+22])


if __name__=='__main__': unittest.main()
