"""Unicode documentation budgets for MSC; manuscript sources are not character-limited."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("msc_docs_validator", ROOT / "scripts/validate_documentation.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class DocumentationTests(unittest.TestCase):
    def fixture(self, dest: Path) -> Path:
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "_site", "site"))
        return dest

    def test_scaffold_budgets_pass(self):
        self.assertEqual([], validator.check_documentation(ROOT))

    def test_utf8_characters_not_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            objpath = root / "config/documentation-policy.json"
            cfg = json.loads(objpath.read_text())
            cfg["exact_limits"]["SUPPORT.md"] = 100
            objpath.write_text(json.dumps(cfg), encoding="utf-8")
            (root / "SUPPORT.md").write_text("ą" * 100, encoding="utf-8")
            self.assertEqual([], validator.check_documentation(root))

    def test_too_long_architecture_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "ARCHITECTURE.md").write_text("x" * 12001, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: ARCHITECTURE.md" in e
                                for e in validator.check_documentation(root)))

    def test_new_adr_has_specific_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "docs/adr/0002-extra.md").write_text("x" * 6501, encoding="utf-8")
            self.assertTrue(any("DOC LENGTH EXCEEDED: docs/adr/0002-extra.md" in e
                                for e in validator.check_documentation(root)))

    def test_missing_security_doc_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "SECURITY.md").unlink()
            self.assertIn("DOC MISSING: SECURITY.md", validator.check_documentation(root))

    def test_boolean_schema_version_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            p = root / "config/documentation-policy.json"
            cfg = json.loads(p.read_text())
            cfg["schema_version"] = True
            p.write_text(json.dumps(cfg))
            self.assertIn("DOC POLICY: unsupported schema_version",
                          validator.check_documentation(root))

    def test_symlink_to_external_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            external = Path(tmp) / "external.md"
            external.write_text("not for public", encoding="utf-8")
            (root / "SUPPORT.md").unlink()
            (root / "SUPPORT.md").symlink_to(external)
            self.assertIn("DOC SYMLINK: SUPPORT.md", validator.check_documentation(root))

    def test_invalid_policy_path_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            p = root / "config/documentation-policy.json"
            data = json.loads(p.read_text())
            data["exact_limits"]["../private.md"] = 500
            p.write_text(json.dumps(data))
            self.assertIn("DOC POLICY: invalid limit or path ../private.md",
                          validator.check_documentation(root))


if __name__ == "__main__":
    unittest.main()
