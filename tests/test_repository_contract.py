"""Offline structural tests. They do not validate scientific methods."""

import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("msc_validator", ROOT / "scripts" / "validate_repository.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(validator)


class RepositoryContractTests(unittest.TestCase):
    def test_scaffold_passes(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_publish_remains_blocked_before_owner_configuration(self):
        self.assertTrue(validator.validate(ROOT, "publish"))

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            (dest / "research" / "protocol.md").unlink()
            self.assertTrue(any("research/protocol.md" in s for s in validator.validate(dest)))

    def test_missing_manuscript_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            (dest / "manuscripts" / "P01" / "main.qmd").unlink()
            self.assertTrue(any("main.qmd" in s for s in validator.validate(dest)))


if __name__ == "__main__":
    unittest.main()
