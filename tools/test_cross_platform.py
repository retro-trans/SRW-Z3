"""Synthetic port guards plus read-only checks of the existing PS3 manifest."""
import importlib.util
import json
from pathlib import Path
import runpy
import tempfile
import unittest

import luarec
import shared_content
import check_names
import register_stage
import stage_status

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("vita_prepare", ROOT / "platforms/vita/prepare_translation.py")
vita = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vita)


def record(n=0, jp="example", en="English"):
    return {"event": "t_000", "n": n, "pid": "pid_TEST", "jp": jp,
            "sha": luarec.digest(jp), "en": en}


class CrossPlatformTests(unittest.TestCase):
    def test_registration_targets_real_platform_manifest(self):
        self.assertEqual(register_stage.MANIFEST, "platforms/ps3/manifest.py")
        self.assertIn(register_stage.MANIFEST_MARKER,
                      (ROOT / register_stage.MANIFEST).read_text(encoding="utf-8"))

    def test_status_and_name_checks_still_find_all_members(self):
        manifest = runpy.run_path(str(ROOT / "platforms/ps3/manifest.py"))
        expected = {stage["sdat"][:-5]: [(str(m["id"]), m["trans"]) for m in stage["members"]]
                    for stage in manifest["STAGES"]}
        self.assertEqual(stage_status.registered(), expected)
        for stage in manifest["STAGES"]:
            for member in stage["members"]:
                self.assertEqual(check_names.member_lua(member["trans"]), member["lua"])

    def test_legacy_manifest_compatibility(self):
        old = runpy.run_path(str(ROOT / "translation/manifest.py"))
        new = runpy.run_path(str(ROOT / "platforms/ps3/manifest.py"))
        for key in ("STAGES", "LIBRARIES"):
            self.assertEqual(old[key], new[key])
            self.assertTrue(new[key])

    def test_matches_identity_not_order(self):
        first, second = record(), record(1, "second")
        self.assertEqual(vita.match_records([first, second], [second, first]), [second, first])

    def test_duplicate_text_is_safe_with_distinct_identity(self):
        first, second = record(), record(1)
        self.assertEqual(len(vita.match_records([first, second], [second, first])), 2)

    def test_rejects_duplicate_identity(self):
        with self.assertRaisesRegex(ValueError, "Ambiguous"):
            vita.match_records([record(), record()], [record(), record()])

    def test_rejects_changed_text_speaker_or_ordinal(self):
        for changed in (record(jp="different"), dict(record(), pid="pid_OTHER"), record(2)):
            with self.assertRaisesRegex(ValueError, "differs"):
                vita.match_records([record()], [changed])

    def test_rejects_stale_fingerprint(self):
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            vita.match_records([record()], [dict(record(), jp="changed")])

    def test_rejects_missing_extra_empty_or_unstamped(self):
        for source in ([], [record(), record(1)], [{"en": "bare"}]):
            with self.assertRaises(ValueError):
                vita.match_records([record()], source)

    def test_newline_normalization(self):
        self.assertEqual(len(vita.match_records([record(jp="a\nb")],
                                               [record(jp="a\r\nb")])), 1)

    def test_shared_revision_tracks_content_not_build_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "translation").mkdir()
            (root / "shared/catalog.json").write_text(json.dumps({
                "content_globs": ["translation/**/*.json"], "exclude": []}))
            text = root / "translation/example.json"
            text.write_text('{"en":"one"}')
            original = shared_content.revision(root)
            (root / "generated.json").write_text("output")
            self.assertEqual(original, shared_content.revision(root))
            text.write_text('{"en":"two"}')
            self.assertNotEqual(original, shared_content.revision(root))

    def test_pilot_uses_shared_content_and_remains_unverified(self):
        result = vita.prepare()
        self.assertFalse(result["playable"])
        self.assertEqual(result["status"], "prepared_unverified")
        self.assertEqual(result["shared_content"], shared_content.revision())
        self.assertEqual(len(result["members"]), 3)
        for member in result["members"]:
            self.assertTrue(member["translation"].startswith("translation/"))
            self.assertTrue(member["records"])
            self.assertTrue(all("$$" not in r["en"] for r in member["lines"]))


if __name__ == "__main__":
    unittest.main()
