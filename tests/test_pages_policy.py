"""Offline checks for MSC public Pages boundary. No participant data or network."""
from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pages_validator", ROOT / "scripts/validate_pages.py")
pages = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(pages)


class PagesPolicyTests(unittest.TestCase):
    def fixture(self, dest: Path) -> Path:
        shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns(
            ".git", ".venv", "__pycache__", "_site", "site"))
        return dest

    def test_baseline_passes(self):
        self.assertEqual([], pages.check_pages(ROOT))
        self.assertFalse((ROOT / "CONTRIBUTING.md").exists())
        self.assertEqual(["index.md"], json.loads(
            (ROOT / "config/pages-policy.json").read_text())["public_files"])

    def test_old_docs_source_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            config = root / "mkdocs.yml"
            config.write_text(config.read_text().replace("docs_dir: pages", "docs_dir: docs"))
            self.assertTrue(any("isolated docs_dir/pages" in s for s in pages.check_pages(root)))

    def test_unlisted_material_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/protocol.md").write_text("Internal protocol", encoding="utf-8")
            self.assertIn("PAGES NOT APPROVED: protocol.md", pages.check_pages(root))

    def test_direct_agent_instruction_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/index.md").write_text("Dla agenta: popraw stronę", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md", pages.check_pages(root))

    def test_editorial_note_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/index.md").write_text("Uwagi redakcyjne: dopisać badanie", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md", pages.check_pages(root))

    def test_unpublished_status_marker_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/index.md").write_text("Badanie NOT_COLLECTED", encoding="utf-8")
            self.assertIn("PAGES EDITORIAL OR AGENT CONTENT: index.md", pages.check_pages(root))

    def test_contributing_guide_cannot_be_allowlisted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            policy = root / "config/pages-policy.json"
            value = json.loads(policy.read_text())
            value["public_files"].append("CONTRIBUTING.md")
            policy.write_text(json.dumps(value))
            self.assertIn("PAGES POLICY: unsafe public file allowlist", pages.check_pages(root))

    def test_link_to_internal_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/index.md").write_text("[SAP](../research/analysis-plan.md)")
            self.assertIn("PAGES INTERNAL REFERENCE: index.md", pages.check_pages(root))

    def test_unreviewed_plugin_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            file = root / "mkdocs.yml"
            file.write_text(file.read_text() + "plugins: [search]\n")
            self.assertIn("PAGES CONFIG: unreviewed or duplicate config key",
                          pages.check_pages(root))

    def test_symlink_to_private_file_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            (root / "pages/secret.md").symlink_to(root / "research/ethics.md")
            self.assertIn("PAGES SYMLINK: secret.md", pages.check_pages(root))

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            policy = root / "config/pages-policy.json"
            obj = json.loads(policy.read_text())
            obj["public_files"].append("../docs/index.md")
            policy.write_text(json.dumps(obj))
            self.assertIn("PAGES POLICY: unsafe public file allowlist",
                          pages.check_pages(root))

    def test_unreviewed_nav_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(Path(tmp) / "msc")
            file = root / "mkdocs.yml"
            file.write_text(file.read_text() + "  - Metody: protocol.md\n")
            self.assertIn("PAGES CONFIG: navigation contains unapproved source",
                          pages.check_pages(root))


if __name__ == "__main__":
    unittest.main()
