"""Read-only: the numbered-condition indent is blanked and every continuation is hooked."""
import json
from pathlib import Path
import unittest
import eboot
import trdata
import mission_conditions as m
import operation_indent as o


class OperationIndentTests(unittest.TestCase):
    def test_only_the_indent_bytes_change(self):
        elf = Path('work/EBOOT_dec.elf').read_bytes()
        new = o.apply(elf)
        changed = [i for i, (a, b) in enumerate(zip(elf, new)) if a != b]
        self.assertEqual(changed, list(range(0x6ea2a8, 0x6ea2ac)))
        o.check(new)

    def test_refuses_unexpected_layout(self):
        elf = bytearray(Path('work/EBOOT_dec.elf').read_bytes())
        elf[0x6ea2a8] = 0
        with self.assertRaises(AssertionError):
            o.apply(elf)

    def test_every_continuation_line_is_hooked(self):
        trdata.use_glossary('analysis/glossary.json')
        hooks = eboot.load_ui_hook()
        # both sources, as displayed; expand() already applied the display
        # variants, and applying them twice would mangle ソ (trail byte 0x5c)
        rows = m.expand(m.additional_lines())
        rows += m.expand(json.loads(Path('translation/mission_conditions_hook.json')
                                    .read_text(encoding='utf-8'))['lines'])
        for row in rows:
            for line in row['jp'].split('\n')[1:]:
                value = line.strip('　 ')
                if value:
                    self.assertIn(value, hooks, value)


if __name__ == '__main__':
    unittest.main()
