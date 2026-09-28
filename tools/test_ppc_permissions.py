"""Synthetic direct-branch permission failures, independent of game files."""
import struct
import unittest
import ppc_permissions as P


def fixture():
    blob = bytearray(0x500)
    blob[:6] = b'\x7fELF\x02\x02'
    struct.pack_into('>Q', blob, 32, 64)
    struct.pack_into('>Q', blob, 40, 0x100)
    struct.pack_into('>HHHH', blob, 54, 56, 2, 64, 1)
    struct.pack_into('>IIQQQQQQ', blob, 64, 1, 5, 0x200, 0x1000, 0x1000, 0x200, 0x200, 4)
    struct.pack_into('>IIQQQQQQ', blob, 120, 1, 6, 0x400, 0x2000, 0x2000, 0x100, 0x200, 4)
    struct.pack_into('>IIQQQQIIQQ', blob, 0x100, 0, 1, 6, 0x1000, 0x200, 0x10, 0, 0, 4, 0)
    struct.pack_into('>4I', blob, 0x200, *([0x60000000] * 4))
    return blob


def jump(blob, pc, target, link=False):
    offset = 0x200 + pc - 0x1000
    struct.pack_into('>I', blob, offset, 0x48000000 | ((target - pc) & 0x3fffffc) | int(link))


class PermissionTests(unittest.TestCase):
    def test_branch_encodings(self):
        self.assertEqual(P.branch_target(0x4bfffffd, 0x1004), 0x1000)
        self.assertEqual(P.branch_target(0x4082fffc, 0x1004), 0x1000)
        self.assertEqual(P.branch_target(0x48001002, 0x1100), 0x1000)
        self.assertIsNone(P.branch_target(0x60000000, 0x1000))

    def test_call_continuation_and_conditional_paths_are_checked(self):
        old = fixture()
        new = bytearray(old)
        jump(new, 0x1000, 0x1100, True)
        jump(new, 0x1100, 0x1004, True)
        struct.pack_into('>I', new, 0x304, 0x4082000c)  # bne 0x1110
        struct.pack_into('>I', new, 0x308, 0x4e800020)
        struct.pack_into('>I', new, 0x310, 0x4e800020)
        self.assertEqual(P.check_changed_branches(old, new)['injected_instructions'], 4)
        jump(new, 0x1110, 0x2000)
        with self.assertRaisesRegex(ValueError, '0x2000'):
            P.check_changed_branches(old, new)

    def test_unmapped_data_bss_and_rwx_targets_rejected(self):
        old = fixture()
        for target in (0x2000, 0x2100, 0x3000):
            new = bytearray(old)
            jump(new, 0x1000, target)
            with self.subTest(target=hex(target)), self.assertRaises(ValueError):
                P.check_changed_branches(old, new)
        new = bytearray(old)
        struct.pack_into('>I', new, 68, 7)
        with self.assertRaisesRegex(ValueError, 'read-only executable'):
            P.check_changed_branches(old, new)

    def test_data_words_are_not_interpreted_as_code(self):
        old = fixture()
        new = bytearray(old)
        struct.pack_into('>I', new, 0x400, 0x4800ffff)
        self.assertEqual(P.check_changed_branches(old, new)['direct_branch_edges'], 0)

    def test_executable_boundary_and_padding_rejected(self):
        old = fixture()
        new = bytearray(old)
        jump(new, 0x1000, 0x11fc)
        struct.pack_into('>I', new, 0x3fc, 0x60000000)
        with self.assertRaisesRegex(ValueError, 'file-backed executable'):
            P.check_changed_branches(old, new)
        jump(new, 0x1000, 0x1100)
        with self.assertRaisesRegex(ValueError, 'zero padding'):
            P.check_changed_branches(old, new)


if __name__ == '__main__':
    unittest.main()
