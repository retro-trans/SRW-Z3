"""Native title source and texture isolation; no package/install writes."""
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
from cpk import CPK
import title_art as T


class VitaTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=T.ROOT/'work/vita/decrypted_PCSG00264'/T.ARCHIVE
        if not source.exists():raise unittest.SkipTest('Native Vita title unavailable')
        cls.archive=CPK(str(source))
        cls.original=cls.archive.read(next(e for e in cls.archive.files if e['id']==T.MEMBER))
        cls.changed=T.apply(cls.original)

    def test_layout_palette_and_animation_preserved(self):
        T.verify(self.original,self.changed)
        title=T.Title(self.original)
        self.assertEqual(self.changed[:T.GXT],self.original[:T.GXT])
        self.assertEqual(self.changed[title.palettes:],self.original[title.palettes:])
        for texture in (0,2,3,4,6):
            at,w,h=title.textures[texture]
            self.assertEqual(self.changed[at:at+w*h],self.original[at:at+w*h])

    def test_each_of_seven_regions_changes(self):
        old,new=T.Title(self.original),T.Title(self.changed)
        for texture,rect in [(1,r[:4]) for r in T.logo.ROWS]+[(5,r[:4]) for r in T.buttons.ROWS]:
            x,y,w,h=rect;box=(x,y,x+w,y+h)
            self.assertNotEqual(old.image(texture).crop(box).tobytes(),new.image(texture).crop(box).tobytes())

    def test_wrong_source_and_unrelated_changes_rejected(self):
        wrong=bytearray(self.original);wrong[0]^=1
        with self.assertRaises(ValueError):T.apply(bytes(wrong))
        wrong=bytearray(self.changed);wrong[T.GXT]^=1
        with self.assertRaises(ValueError):T.verify(self.original,bytes(wrong))

    def test_builder_sink_and_report(self):
        port=mock.Mock();port.cpk.return_value=self.archive
        with mock.patch.object(T,'apply',return_value=self.changed):
            report=T.prepare(port)
        port.cpk.assert_called_once_with(T.ARCHIVE)
        port.emit.assert_called_once_with(T.ARCHIVE,T.MEMBER,self.changed)
        self.assertEqual(report['animation_samples_preserved'],5655)
        self.assertEqual(report['library_labels'],5)
        self.assertFalse(report['runtime_tested'])

    def test_native_palette_identity(self):
        palette=T.Title(self.original).palette(1)
        match=T.nearest_palette(palette)
        for rgba in palette:
            result=palette[match(rgba)]
            self.assertEqual(result[3],rgba[3])
            if rgba[3]:self.assertEqual(result,rgba)


if __name__=='__main__':unittest.main()
