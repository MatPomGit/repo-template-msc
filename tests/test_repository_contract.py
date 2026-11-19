"""Offline structural tests. They do not validate scientific methods."""

import importlib.util
import shutil
import json
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

    def test_explicit_manuscript_and_protocol_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            state = dest / "PROJECT_STATE.yaml"
            text = state.read_text(encoding="utf-8")
            text = text.replace("manuscript_root: manuscripts", (
                "manuscript_root: legacy/thesis\\n"
                "manuscript_source: legacy/thesis/praca.qmd\\n"
                "bibliography_path: legacy/thesis/bibliografia.bib"
            ).replace("\\n", "\n"))
            text = text.replace("protocol_path: research/protocol.md",
                                "protocol_path: legacy/protokol.md")
            text = text.replace("manuscript_format: latex", "manuscript_format: quarto")
            state.write_text(text, encoding="utf-8")
            (dest / "legacy/thesis").mkdir(parents=True)
            (dest / "legacy/thesis/praca.qmd").write_text("# Manuscript", encoding="utf-8")
            (dest / "legacy/thesis/bibliografia.bib").write_text(
                "@misc{example, title={Example}}", encoding="utf-8")
            (dest / "legacy/protokol.md").write_text("Protocol", encoding="utf-8")
            # Remove the original defaults; this would fail if metadata paths
            # were silently ignored by a broken parser.
            (dest / "research/protocol.md").unlink()
            shutil.rmtree(dest / "manuscripts")
            self.assertEqual(validator.validate(dest), [])

    def test_missing_mapped_protocol_must_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            state = dest / "PROJECT_STATE.yaml"
            state.write_text(state.read_text().replace(
                "protocol_path: research/protocol.md", "protocol_path: other/missing.md"
            ), encoding="utf-8")
            self.assertTrue(any("Missing or unsafe required protocol_path" in x
                                for x in validator.validate(dest)))

    def test_path_traversal_in_scientific_manifest_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            state = dest / "PROJECT_STATE.yaml"
            state.write_text(state.read_text().replace(
                "protocol_path: research/protocol.md", "protocol_path: ../outside.md"
            ), encoding="utf-8")
            self.assertTrue(any("Missing or unsafe required protocol_path" in x
                                for x in validator.validate(dest)))

    def test_default_source_is_latex(self):
        content = (ROOT / "PROJECT_STATE.yaml").read_text(encoding="utf-8")
        self.assertIn("manuscript_format: latex", content)
        self.assertIn("manuscript_source: manuscripts/P01/main.tex", content)
        self.assertTrue((ROOT / "manuscripts/P01/main.tex").is_file())
        self.assertFalse((ROOT / "manuscripts/P01/main.qmd").exists())

    def test_quarto_remains_supported_on_explicit_opt_in(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            source = dest / "manuscripts/P01/main.tex"
            source.unlink()
            (dest / "manuscripts/P01/main.qmd").write_text("# Draft", encoding="utf-8")
            state = dest / "PROJECT_STATE.yaml"
            data = state.read_text(encoding="utf-8")
            data = data.replace("manuscript_format: latex", "manuscript_format: quarto")
            data = data.replace("manuscript_source: manuscripts/P01/main.tex",
                                "manuscript_source: manuscripts/P01/main.qmd")
            state.write_text(data, encoding="utf-8")
            self.assertEqual(validator.validate(dest), [])

    def test_tikz_is_an_external_figure(self):
        main = (ROOT / "manuscripts/P01/main.tex").read_text(encoding="utf-8")
        figure = ROOT / "manuscripts/P01/figures/study-workflow.tex"
        self.assertIn(r"\\input{figures/study-workflow.tex}", main)
        self.assertNotIn(r"\\begin{tikzpicture}", main)
        self.assertTrue(figure.is_file())
        self.assertIn(r"\\begin{tikzpicture}", figure.read_text(encoding="utf-8"))

    def test_inline_tikz_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            main = dest / "manuscripts/P01/main.tex"
            main.write_text(main.read_text(encoding="utf-8") +
                            "\\n" + r"\\begin{tikzpicture}\\end{tikzpicture}",
                            encoding="utf-8")
            self.assertTrue(any("Inline TikZ drawing" in issue
                                for issue in validator.validate(dest)))

    def test_missing_external_tikz_figure_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            (dest / "manuscripts/P01/figures/study-workflow.tex").unlink()
            self.assertTrue(any("Missing or unsafe external figure" in issue
                                for issue in validator.validate(dest)))

    def test_external_figure_cannot_be_a_standalone_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            fig = dest / "manuscripts/P01/figures/study-workflow.tex"
            fig.write_text(r"\\documentclass{standalone}" + "\\n" + fig.read_text(),
                           encoding="utf-8")
            self.assertTrue(any("input fragment" in issue
                                for issue in validator.validate(dest)))

    def test_source_format_mismatch_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            state = dest / "PROJECT_STATE.yaml"
            state.write_text(state.read_text().replace(
                "manuscript_format: latex", "manuscript_format: quarto"
            ), encoding="utf-8")
            self.assertTrue(any("manuscript_format conflicts" in x
                                for x in validator.validate(dest)))

    def test_missing_manuscript_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "msc-test"
            shutil.copytree(ROOT, dest, ignore=shutil.ignore_patterns("__pycache__"))
            (dest / "manuscripts" / "P01" / "main.tex").unlink()
            self.assertTrue(any("main.tex" in s for s in validator.validate(dest)))


if __name__ == "__main__":
    unittest.main()
