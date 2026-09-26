"""Portable paths, public resources and GUI workflow using synthetic saves only."""
from pathlib import Path
import tempfile
import time
import tkinter as tk
import unittest
from unittest.mock import patch

import convert_z3_saves as core
import save_converter_gui as gui
from test_save_conversion import inputs


class PortableTests(unittest.TestCase):
    def test_frozen_home_is_executable_not_extraction_or_cwd(self):
        with patch.object(gui.sys, 'frozen', True, create=True), \
                patch.object(gui.sys, 'executable', str(Path('portable/app.exe').resolve())):
            self.assertEqual(gui.app_home(), Path('portable').resolve())

    def test_public_guide_available(self):
        guide = gui.guide_path().read_text(encoding='utf-8')
        self.assertIn('NPJB00520', guide)
        self.assertIn('PCSG00264', guide)
        self.assertNotIn('Users/Binh', guide)

    def test_output_collision_is_not_reused(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            with patch.object(gui, 'datetime') as clock:
                clock.now.return_value.strftime.return_value = 'fixed'
                first = gui.next_output(home)
                first.mkdir(parents=True)
                self.assertEqual(gui.next_output(home), first.with_name(first.name + '-1'))

    def test_changed_sources_rejected_before_output_creation(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            ps3, vita = inputs(home)
            output = home / 'work/result'
            with patch.object(core, 'ROOT', home):
                report = core.build(ps3, vita, output)
                (ps3 / 'NPJB00520-SYS/ICON0.PNG').write_bytes(b'changed fixture icon')
                with self.assertRaisesRegex(ValueError, 'changed since checking'):
                    core.build(ps3, vita, output, write=True, guide_path=gui.guide_path(),
                               expected_sources=report['source_files'])
                self.assertFalse(output.exists())

    def test_public_guide_override_and_live_output_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            home = Path(folder)
            ps3, vita = inputs(home / 'work/fixtures')
            with patch.object(core, 'ROOT', home):
                for unsafe in (ps3 / 'out', vita / 'out', home / 'outside'):
                    with self.assertRaises(ValueError):
                        core.build(ps3, vita, unsafe, write=True, guide_path=gui.guide_path())
                    self.assertFalse(unsafe.exists())
                output = home / 'work/result'
                core.build(ps3, vita, output, write=True, guide_path=gui.guide_path())
            self.assertEqual((output / 'README-FIRST.md').read_bytes(), gui.guide_path().read_bytes())


class WindowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='srw-converter-test-')
        self.home = Path(self.temp.name)
        self.original_root = core.ROOT
        self.home_patch = patch.object(gui, 'app_home', return_value=self.home)
        self.guide_patch = patch.object(gui, 'guide_path', return_value=gui.guide_path())
        self.home_patch.start()
        self.guide_patch.start()
        self.window = tk.Tk()
        self.window.withdraw()
        self.app = gui.ConverterApp(self.window)
        self.window.update()

    def tearDown(self):
        self.app.close()
        self.home_patch.stop()
        self.guide_patch.stop()
        core.ROOT = self.original_root
        self.temp.cleanup()

    def wait_done(self):
        deadline = time.monotonic() + 30
        while self.app.busy and time.monotonic() < deadline:
            self.window.update()
            time.sleep(0.01)
        self.assertFalse(self.app.busy, 'Worker did not finish')

    def select_fixtures(self):
        ps3, vita = inputs(self.home / 'fixtures')
        self.app.ps3.set(str(ps3))
        self.app.vita.set(str(vita))
        self.app.closed.set(True)
        return ps3, vita

    def test_conversion_gated_on_inputs_and_check(self):
        self.assertEqual(str(self.app.convert_button['state']), 'disabled')
        self.app.start(True)
        self.assertFalse(self.app.busy)
        self.select_fixtures()
        self.app.start(True)
        self.assertIsNone(self.app.finished)
        self.assertFalse(self.app.output.exists())

    def test_browse_updates_selected_folder(self):
        with patch.object(gui.filedialog, 'askdirectory', return_value=str(self.home)):
            self.app.browse(self.app.ps3)
        self.assertEqual(self.app.ps3.get(), str(self.home))

    def test_check_convert_and_originals_unchanged(self):
        ps3, vita = self.select_fixtures()
        before = core.source_blobs(core.load_ps3(ps3), core.load_vita(vita))
        self.app.start(False)
        self.wait_done()
        self.assertIsNotNone(self.app.checked, self.app.status.get())
        self.assertFalse(self.app.output.exists())
        self.app.start(True)
        self.wait_done()
        self.assertIsNotNone(self.app.finished, self.app.status.get())
        self.assertTrue((self.app.finished / 'CONVERSION_AUDIT.json').is_file())
        self.assertTrue((self.app.finished / 'rpcs3-to-vita3k.zip').is_file())
        self.assertTrue((self.app.finished / 'vita3k-to-rpcs3.zip').is_file())
        self.assertEqual(core.source_blobs(core.load_ps3(ps3), core.load_vita(vita)), before)
        self.assertIsNone(self.app.checked)
        self.assertEqual(str(self.app.convert_button['state']), 'disabled')

    def test_input_change_invalidates_check(self):
        self.select_fixtures()
        self.app.start(False)
        self.wait_done()
        self.assertIsNotNone(self.app.checked)
        self.app.closed.set(False)
        self.assertIsNone(self.app.checked)
        self.assertEqual(str(self.app.convert_button['state']), 'disabled')

    def test_invalid_folder_is_readable_error_no_output(self):
        self.app.ps3.set(str(self.home / 'missing'))
        self.app.vita.set(str(self.home / core.VITA_ID))
        self.app.closed.set(True)
        self.app.start(False)
        self.wait_done()
        self.assertTrue(self.app.status.get().startswith('Stopped:'))
        self.assertFalse(self.app.output.exists())


if __name__ == '__main__':
    unittest.main()
