"""No-network test suite for Zotero and Better BibTeX manuscript support."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("zotero_check", ROOT / "scripts/check_zotero.py")
checker = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(checker)


class ZoteroContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.paper = Path(self.temp.name) / "manuscripts/P01"
        shutil.copytree(ROOT / "manuscripts/P01", self.paper)

    def test_scaffold_passes(self):
        self.assertEqual([], checker.validate_manuscript(self.paper))

    def test_missing_citation_fails(self):
        m = self.paper / "main.tex"
        m.write_text(m.read_text() + r"\citep{absent2026}", encoding="utf-8")
        self.assertIn("Missing Zotero citation key: absent2026",
                      checker.validate_manuscript(self.paper))

    def test_matching_bibtex_passes(self):
        (self.paper / "references.bib").write_text(
            "@article{valid2024, title={A bibliographic record}}\n", encoding="utf-8")
        m = self.paper / "main.tex"
        m.write_text(m.read_text() + r"\citep{valid2024}", encoding="utf-8")
        self.assertEqual([], checker.validate_manuscript(self.paper))

    def test_duplicate_keys_fail(self):
        (self.paper / "references.bib").write_text(
            "@article{k2024, title={One}}\n@book{k2024, title={Two}}\n", encoding="utf-8")
        self.assertIn("Duplicate BibTeX citation key: k2024",
                      checker.validate_manuscript(self.paper))

    def test_private_attachment_fields_fail(self):
        (self.paper / "references.bib").write_text(
            "@article{k1, title={One},\nfile={C:/private/file.pdf}}\n", encoding="utf-8")
        self.assertTrue(any("attachment/annotation" in item
                            for item in checker.validate_manuscript(self.paper)))

    def test_export_of_attachments_not_allowed(self):
        cfg = self.paper / "zotero.json"
        data = json.loads(cfg.read_text())
        data["export_attachments"] = True
        cfg.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("export_attachments" in item
                            for item in checker.validate_manuscript(self.paper)))

    def test_credentials_in_configuration_rejected(self):
        cfg = self.paper / "zotero.json"
        data = json.loads(cfg.read_text())
        data["api_key"] = "unsafe"
        cfg.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("credentials" in item
                            for item in checker.validate_manuscript(self.paper)))

    def test_scaffold_ok_but_submission_requires_actual_setup(self):
        self.assertEqual([], checker.validate_manuscript(self.paper))
        self.assertIn("Zotero auto-export setup not confirmed by owner",
                      checker.validate_manuscript(self.paper, True))

    def test_escaped_percent_stays_literal(self):
        value = checker.without_tex_comments(
            r"20\% in \cite{year2024} % \cite{ignored}")
        self.assertIn(r"\cite{year2024}", value)
        self.assertNotIn("ignored", value)

    def test_commented_cite_does_not_count(self):
        m = self.paper / "main.tex"
        m.write_text(m.read_text() + "\n% " + r"\cite{phantom}", encoding="utf-8")
        self.assertEqual([], checker.validate_manuscript(self.paper))

    def test_figure_citations_count(self):
        f = self.paper / "figures/study-workflow.tex"
        f.write_text(f.read_text() + "\n" + r"\cite{figMissing}", encoding="utf-8")
        self.assertTrue(any("figMissing" in x for x in checker.validate_manuscript(self.paper)))

    def test_multiple_quarto_cites_count(self):
        (self.paper / "older.qmd").write_text(
            "Quarto sources [@found; @notfound, p. 2].", encoding="utf-8")
        (self.paper / "references.bib").write_text(
            "@article{found, title={Found}}\n", encoding="utf-8")
        self.assertTrue(any("notfound" in x for x in checker.validate_manuscript(self.paper)))

    def test_malformed_bib_entry_fails(self):
        (self.paper / "references.bib").write_text(
            "@article{broken title={No comma}}\n", encoding="utf-8")
        self.assertTrue(any("Unparseable" in x for x in checker.validate_manuscript(self.paper)))

    def test_unsafe_bibliography_path_fails(self):
        cfg = self.paper / "zotero.json"
        data = json.loads(cfg.read_text())
        data["bibliography"] = "../private/references.bib"
        cfg.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("Unsafe Zotero bibliography filename",
                      checker.validate_manuscript(self.paper))

    def test_discovery_of_opted_in_manuscripts(self):
        errors, count = checker.validate_root(Path(self.temp.name))
        self.assertEqual(([], 1), (errors, count))


if __name__ == "__main__":
    unittest.main()
