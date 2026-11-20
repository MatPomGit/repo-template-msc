"""Output HTML audit regression tests, without internet or MkDocs dependencies."""
from __future__ import annotations
import tempfile
import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from validate_site import check_site

class SiteTests(unittest.TestCase):
    def site(self,d):
        site=Path(d)/"_site"
        site.mkdir(parents=True)
        (site/"index.html").write_text("<h1>Projekt badawczy</h1>",encoding="utf-8")
        return site
    def test_html_site_passes(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual([],check_site(self.site(d)))
    def test_agent_prompt_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site=self.site(d)
            (site/"index.html").write_text("<h1>Agent: wykonaj teraz</h1>",encoding="utf-8")
            self.assertTrue(any("SITE UNSAFE HTML" in e for e in check_site(site)))
    def test_internal_reference_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site=self.site(d)
            (site/"index.html").write_text('<a href="../docs/secret.md">Tajne</a>',encoding="utf-8")
            self.assertTrue(any("SITE INTERNAL URL" in e for e in check_site(site)))
    def test_extra_private_directory_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site=self.site(d)
            (site/"private").mkdir()
            (site/"private/file.html").write_text("private",encoding="utf-8")
            self.assertTrue(any("SITE UNSAFE PATH" in e for e in check_site(site)))
    def test_remote_script_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"index.html").write_text(
                '<script src="https://cdn.example.org/unknown.js"></script>', encoding="utf-8")
            self.assertIn("SITE UNAPPROVED SCRIPT: index.html", check_site(site))

    def test_unapproved_inline_script_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"index.html").write_text("<script>alert(1)</script>", encoding="utf-8")
            self.assertIn("SITE UNAPPROVED INLINE SCRIPT: index.html", check_site(site))

    def test_active_event_handler_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"index.html").write_text('<img onerror="alert(1)">', encoding="utf-8")
            self.assertIn("SITE ACTIVE HANDLER: index.html", check_site(site))

    def test_strict_rejects_unknown_static_asset(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"js").mkdir()
            (site/"js/unreviewed.js").write_text("alert(1)", encoding="utf-8")
            self.assertIn("SITE UNAPPROVED FILE: js/unreviewed.js",
                          check_site(site, strict=True))

    def test_strict_rejects_modified_pinned_script(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"js").mkdir()
            (site/"js/base.js").write_text("// replaced", encoding="utf-8")
            self.assertIn("SITE THEME HASH MISMATCH: js/base.js",
                          check_site(site, strict=True))

    def test_known_mkdocs_inline_config_passes(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"index.html").write_text(
                '<script>var base_url = "/", shortcuts = '
                '{"help": 191, "next": 78, "previous": 80, "search": 83};'
                '</script>', encoding="utf-8")
            self.assertEqual([], check_site(site))

    def test_search_form_without_action_passes(self):
        with tempfile.TemporaryDirectory() as d:
            site = self.site(d)
            (site/"index.html").write_text(
                '<form><input id="mkdocs-search-query" type="search"></form>', encoding="utf-8")
            self.assertEqual([], check_site(site))

    def test_public_pdf_tamper_rejected(self):
        import hashlib
        import json
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "config").mkdir()
            original = json.loads((ROOT / "config/pages-policy.json").read_text(encoding="utf-8"))
            pdf = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF"
            original["public_files"].append("manuscript-p01.pdf")
            original["approved_pdf_sha256"]["manuscript-p01.pdf"] = hashlib.sha256(pdf).hexdigest()
            (folder / "config/pages-policy.json").write_text(json.dumps(original), encoding="utf-8")
            site = self.site(tmp)
            (site / "manuscript-p01.pdf").write_bytes(pdf + b"tampered")
            self.assertIn("SITE PDF HASH MISMATCH: manuscript-p01.pdf",
                          check_site(site, root=folder))

    def test_public_pdf_sha_validates_when_matching(self):
        import hashlib
        import json
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "config").mkdir()
            original = json.loads((ROOT / "config/pages-policy.json").read_text(encoding="utf-8"))
            pdf = b"%PDF-1.7\n1 0 obj\n<<>>\nendobj\n%%EOF"
            original["public_files"].append("manuscript-p01.pdf")
            original["approved_pdf_sha256"]["manuscript-p01.pdf"] = hashlib.sha256(pdf).hexdigest()
            (folder / "config/pages-policy.json").write_text(json.dumps(original), encoding="utf-8")
            site = self.site(tmp)
            (site / "manuscript-p01.pdf").write_bytes(pdf)
            self.assertEqual([], check_site(site, root=folder))

if __name__=="__main__":
    unittest.main()
