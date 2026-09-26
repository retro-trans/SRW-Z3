"""Portable, offline Windows interface for the decrypted emulator save converter.

Legacy standalone 0.6.14 reference. The maintained converter is now in
../retro-trans-tools/retro_trans/z3_saves.py and Retro Trans's Z3 saves tab.
Keep this historical implementation for existing packagers/native checks;
make future converter changes in Retro Trans. No new standalone release implied.
"""
from contextlib import redirect_stdout
from datetime import datetime
import io
import json
import os
from pathlib import Path
import queue
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import convert_z3_saves as core

VERSION = '0.6.14'


def app_home():
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def guide_path():
    if getattr(sys, 'frozen', False):
        return Path(__file__).resolve().with_name('SAVE_CONVERTER_RELEASE.md')
    return app_home() / 'docs/SAVE_CONVERTER_RELEASE.md'


def next_output(home):
    base = home / 'work' / ('converted-' + datetime.now().strftime('%Y%m%d-%H%M%S'))
    result, suffix = base, 1
    while result.exists():
        result = base.with_name(base.name + '-' + str(suffix))
        suffix += 1
    return result


class QueueWriter:
    def __init__(self, events):
        self.events = events

    def write(self, text):
        if text:
            self.events.put(('log', text))
        return len(text)

    def flush(self):
        pass


class ConverterApp:
    def __init__(self, window):
        self.window = window
        self.home = app_home()
        core.ROOT = self.home
        self.events = queue.Queue()
        self.busy = False
        self.checked = None
        self.finished = None
        self.ps3 = tk.StringVar(window)
        self.vita = tk.StringVar(window)
        self.closed = tk.BooleanVar(window, False)
        self.output = next_output(self.home)
        self.status = tk.StringVar(window, 'Select both save folders, then check them.')
        self.output_text = tk.StringVar(window, str(self.output))
        window.title('SRW Z3 Save Converter ' + VERSION)
        window.geometry('860x680')
        window.minsize(720, 620)
        window.protocol('WM_DELETE_WINDOW', self.close)
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill='both', expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(10, weight=1)
        ttk.Label(frame, text='SRW Z3 Save Converter', font=('Segoe UI', 20, 'bold')).grid(
            row=0, column=0, columnspan=3, sticky='w')
        ttk.Label(frame, text='RPCS3  ↔  Vita3K  ·  Jigoku-hen  ·  Offline',
                  font=('Segoe UI', 11)).grid(row=1, column=0, columnspan=3, sticky='w', pady=(4, 16))
        ttk.Label(frame, text='Create system data and at least one manual save in EACH emulator first.\n'
                  'This converts whole profiles in both directions; it does not merge progress.',
                  wraplength=700).grid(row=2, column=0, columnspan=3, sticky='w', pady=(0, 14))
        self.controls = []
        for row, label, variable, help_text in (
                (3, 'RPCS3 saves', self.ps3, 'Select savedata containing NPJB00520-SYS and NPJB00520-STG-*.'),
                (5, 'Vita3K saves', self.vita, 'Select PCSG00264 under ux0/user/00/savedata (not the game folder).')):
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky='w', padx=(0, 12))
            entry = ttk.Entry(frame, textvariable=variable)
            entry.grid(row=row, column=1, sticky='ew')
            button = ttk.Button(frame, text='Browse…', command=lambda v=variable: self.browse(v))
            button.grid(row=row, column=2, padx=(8, 0))
            self.controls.extend((entry, button))
            ttk.Label(frame, text=help_text, wraplength=680).grid(
                row=row + 1, column=1, columnspan=2, sticky='w', pady=(4, 14))
        checkbox = ttk.Checkbutton(frame, text='Both emulators are closed. I have kept my original saves.',
                                   variable=self.closed)
        checkbox.grid(row=7, column=0, columnspan=3, sticky='w', pady=(2, 12))
        self.controls.append(checkbox)
        actions = ttk.Frame(frame)
        actions.grid(row=8, column=0, columnspan=3, sticky='w', pady=(0, 12))
        self.check_button = ttk.Button(actions, text='1. Check saves', command=lambda: self.start(False))
        self.check_button.pack(side='left')
        self.convert_button = ttk.Button(actions, text='2. Convert both directions', command=lambda: self.start(True))
        self.convert_button.pack(side='left', padx=8)
        self.open_button = ttk.Button(actions, text='Open output folder', command=self.open_output)
        self.open_button.pack(side='left')
        ttk.Button(actions, text='Instructions', command=self.instructions).pack(side='left', padx=8)
        ttk.Label(frame, textvariable=self.status, wraplength=730).grid(
            row=9, column=0, columnspan=3, sticky='w', pady=(0, 8))
        self.log = scrolledtext.ScrolledText(frame, height=10, wrap='word', font=('Consolas', 10), state='disabled')
        self.log.grid(row=10, column=0, columnspan=3, sticky='nsew')
        ttk.Label(frame, text='New output folder (originals are never modified):').grid(
            row=11, column=0, columnspan=3, sticky='w', pady=(12, 3))
        ttk.Label(frame, textvariable=self.output_text, wraplength=730).grid(
            row=12, column=0, columnspan=3, sticky='w')
        ttk.Label(frame, text='Decrypted emulator saves only. No direct physical-console installation.',
                  wraplength=730).grid(row=13, column=0, columnspan=3, sticky='w', pady=(10, 0))
        for variable in (self.ps3, self.vita, self.closed):
            variable.trace_add('write', self.invalidate)
        self.refresh()
        self.timer = window.after(75, self.poll)

    def invalidate(self, *args):
        self.checked = None
        if not self.busy:
            self.status.set('Inputs changed. Check saves before converting.')
        self.refresh()

    def refresh(self):
        for control in self.controls:
            control.configure(state='disabled' if self.busy else 'normal')
        ready = bool(self.ps3.get().strip() and self.vita.get().strip() and self.closed.get())
        self.check_button.configure(state='normal' if ready and not self.busy else 'disabled')
        self.convert_button.configure(state='normal' if ready and self.checked and not self.busy else 'disabled')
        self.open_button.configure(state='normal' if self.finished and not self.busy else 'disabled')

    def browse(self, variable):
        selected = filedialog.askdirectory(parent=self.window, title='Choose save folder', mustexist=True)
        if selected:
            variable.set(selected)

    def append_log(self, text):
        self.log.configure(state='normal')
        self.log.insert('end', text)
        self.log.see('end')
        self.log.configure(state='disabled')

    def start(self, write):
        if self.busy:
            return
        if not self.closed.get() or not self.ps3.get().strip() or not self.vita.get().strip():
            self.status.set('Select both folders and confirm the emulators are closed.')
            return
        if write and not self.checked:
            self.status.set('Check saves first.')
            return
        if not write:
            self.checked = None
            self.output = next_output(self.home)
            self.output_text.set(str(self.output))
        ps3, vita = Path(self.ps3.get().strip()), Path(self.vita.get().strip())
        expected = self.checked['source_files'] if write else None
        self.busy = True
        self.status.set('Converting and verifying…' if write else 'Checking formats, checksums and slot mappings…')
        self.append_log('\n' + self.status.get() + '\n')
        self.refresh()
        threading.Thread(target=self.worker, args=(ps3, vita, self.output, write, expected), daemon=True).start()

    def worker(self, ps3, vita, output, write, expected):
        try:
            with redirect_stdout(QueueWriter(self.events)):
                report = core.build(ps3, vita, output, write=write,
                                    guide_path=guide_path(), expected_sources=expected)
            self.events.put(('done', (write, output, report)))
        except Exception as error:
            self.events.put(('error', (output, str(error))))

    def poll(self):
        while True:
            try:
                kind, payload = self.events.get_nowait()
            except queue.Empty:
                break
            if kind == 'log':
                self.append_log(payload)
            elif kind == 'done':
                write, output, report = payload
                self.busy = False
                self.checked = None if write else report
                if write:
                    self.finished = output
                    self.status.set('Conversion verified. Open the output folder and follow README-FIRST.md to import.')
                else:
                    self.status.set('Checks passed. Review the slot mappings below, then convert.')
                self.refresh()
            elif kind == 'error':
                output, error = payload
                self.busy, self.checked = False, None
                self.status.set('Stopped: ' + error)
                self.append_log('ERROR: ' + error + '\n')
                if output.exists():
                    self.append_log('Do NOT import this incomplete output: ' + str(output) + '\n')
                self.refresh()
        self.timer = self.window.after(75, self.poll)

    def open_output(self):
        if self.finished:
            try:
                os.startfile(str(self.finished))
            except OSError as error:
                messagebox.showerror('Cannot open folder', str(error), parent=self.window)

    def instructions(self):
        dialog = tk.Toplevel(self.window)
        dialog.title('Save conversion instructions')
        dialog.geometry('800x620')
        text = scrolledtext.ScrolledText(dialog, wrap='word', font=('Segoe UI', 11), padx=16, pady=16)
        text.pack(fill='both', expand=True)
        try:
            text.insert('end', guide_path().read_text(encoding='utf-8'))
        except OSError as error:
            text.insert('end', 'Cannot read instructions: ' + str(error))
        text.configure(state='disabled')

    def close(self):
        if self.busy:
            messagebox.showinfo('Please wait', 'Wait for the check or conversion to finish before closing.', parent=self.window)
            return
        self.window.after_cancel(self.timer)
        self.window.destroy()


def self_test(report_path):
    """Developer diagnostic: synthetic saves only, never discovers user saves."""
    import unittest
    import test_save_conversion
    import test_save_converter_gui
    report_path = Path(report_path)
    core.require(not report_path.exists(), 'Diagnostic report already exists')
    stream = io.StringIO()
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(module)
                               for module in (test_save_conversion, test_save_converter_gui))
    with redirect_stdout(stream):
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report = dict(success=result.wasSuccessful(), tests=result.testsRun,
                  frozen=bool(getattr(sys, 'frozen', False)), python=sys.version,
                  log=stream.getvalue())
    with report_path.open('x', encoding='utf-8') as output:
        json.dump(report, output, ensure_ascii=False, indent=2)
    return 0 if result.wasSuccessful() else 1


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--self-test':
        return self_test(sys.argv[2])
    window = tk.Tk()
    ttk.Style(window).theme_use('vista' if 'vista' in ttk.Style(window).theme_names() else 'clam')
    ConverterApp(window)
    window.mainloop()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
