"""Read-only audit of MSC rendered MkDocs and its approved static assets.

A successful check is not permission to deploy or evidence of scientific validity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

from validate_pages import BANNED

ROOT = Path(__file__).resolve().parents[1]
INTERNAL = re.compile(
    r"(?:\.\./docs/|/\.github/|/AGENTS\.md|/CONTRIBUTING\.md|/research/|file://)", re.I
)
SENSITIVE = {"docs", "portfolio", "research", "equipment", "private", "raw", "secrets"}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")
GENERATED = {"sitemap.xml", "sitemap.xml.gz", "search/search_index.json"}
INLINE_MKDOCS = re.compile(
    r'^\s*var\s+base_url\s*=\s*"(?:/|\.{1,2}(?:/\.\.)*)"\s*,\s*'
    r'shortcuts\s*=\s*\{\s*"help":\s*191,\s*"next":\s*78,\s*'
    r'"previous":\s*80,\s*"search":\s*83\s*\}\s*;\s*$'
)


class PageParser(HTMLParser):
    def __init__(self, page: str, scripts: set[str]):
        super().__init__(convert_charrefs=True)
        self.page = page
        self.scripts = scripts
        self.parts: list[str] = []
        self.references: list[str] = []
        self.issues: list[str] = []
        self.ignored = 0
        self.inline_script = False
        self.inline_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        attributes = {k.lower(): v or "" for k, v in attrs}
        if tag in {"script", "style"}:
            self.ignored += 1
        if tag in {"iframe", "object", "embed", "base"} or (tag == "form" and attributes):
            self.issues.append("SITE ACTIVE TAG: " + self.page)
        if any(key.startswith("on") for key in attributes):
            self.issues.append("SITE ACTIVE HANDLER: " + self.page)
        if any(re.search(r"(?i)\b(?:javascript|vbscript)\s*:|data\s*:\s*text/html", value)
               for value in attributes.values()):
            self.issues.append("SITE ACTIVE URL: " + self.page)
        if tag == "meta" and attributes.get("http-equiv", "").lower() == "refresh":
            self.issues.append("SITE META REFRESH: " + self.page)
        for key, value in attributes.items():
            if key in {"href", "src", "action"} and value:
                self.references.append(value)
        if tag == "script":
            source = attributes.get("src")
            if source is None:
                self.inline_script = True
                self.inline_parts = []
            else:
                if source.startswith("/") and not source.startswith("//"):
                    relative = source.lstrip("/")
                elif re.match(r"^[A-Za-z][\w+.-]*:|^//", source):
                    relative = ""
                else:
                    relative = posixpath.normpath(posixpath.join(
                        posixpath.dirname(self.page), source
                    ))
                if relative not in self.scripts:
                    self.issues.append("SITE UNAPPROVED SCRIPT: " + self.page)
        if tag in {"link", "img", "source"}:
            address = attributes.get("href", attributes.get("src", ""))
            if re.match(r"(?i)^https?://|^//", address):
                self.issues.append("SITE EXTERNAL RESOURCE: " + self.page)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self.inline_script:
            self.inline_script = False
            if not INLINE_MKDOCS.fullmatch("".join(self.inline_parts)):
                self.issues.append("SITE UNAPPROVED INLINE SCRIPT: " + self.page)
        if tag.lower() in {"script", "style"} and self.ignored:
            self.ignored -= 1

    def handle_data(self, data):
        if self.inline_script:
            self.inline_parts.append(data)
        if not self.ignored:
            self.parts.append(data)


def expected_html(approved: list[str]) -> set[str]:
    found = {"404.html"}
    for name in approved:
        path = PurePosixPath(name)
        if path.suffix == ".md":
            target = path.with_suffix("")
            found.add(str(target.parent / "index.html") if target.name == "index"
                      else str(target / "index.html"))
        elif path.suffix == ".html":
            found.add(name)
    return found


def read_policy(root: Path) -> tuple[dict, list[str]]:
    try:
        data = json.loads((root / "config/pages-policy.json").read_text(encoding="utf-8"))
        if ((data.get("source_dir"), data.get("output_dir"), data.get("mkdocs_config")) !=
                ("pages", "_site", "mkdocs.yml")):
            return {}, ["SITE POLICY: source and build directories must be isolated"]
        theme = data["approved_theme_assets"]
        images = data["approved_image_sha256"]
        files = data["public_files"]
        if (type(data.get("schema_version")) is not int or data["schema_version"] != 1
                or not isinstance(theme, dict) or not theme
                or not isinstance(images, dict) or not isinstance(files, list)
                or any(not isinstance(k, str) or not isinstance(v, str) or
                       not HASH_RE.fullmatch(v) for k, v in [*theme.items(), *images.items()])
                or any(name not in files for name in images)):
            return {}, ["SITE POLICY: invalid approved assets"]
        return data, []
    except (OSError, ValueError, TypeError, KeyError, UnicodeError, AttributeError):
        return {}, ["SITE POLICY: missing or malformed"]


def check_site(site: Path, *, strict: bool = False, root: Path = ROOT) -> list[str]:
    site = Path(site).resolve()
    if not site.is_dir() or site.is_symlink():
        return ["SITE MISSING: generated site is required"]
    policy, errors = read_policy(Path(root).resolve())
    if errors:
        return errors
    approved = policy["public_files"]
    theme = policy["approved_theme_assets"]
    images = policy["approved_image_sha256"]
    approved_html = expected_html(approved)
    approved_sources = {x for x in approved if PurePosixPath(x).suffix != ".md"}
    scripts = {x for x in theme if x.endswith(".js")} | {
        x for x in approved if x.endswith(".js")
    }
    allowed = approved_html | approved_sources | set(theme) | GENERATED
    issues: list[str] = []
    found: set[str] = set()
    count = 0
    for file in sorted(site.rglob("*")):
        name = file.relative_to(site).as_posix()
        if file.is_symlink():
            issues.append("SITE SYMLINK: " + name)
            continue
        if file.is_dir():
            continue
        if not file.is_file() or any(
                part.startswith(".") or part.lower() in SENSITIVE
                for part in file.relative_to(site).parts):
            issues.append("SITE UNSAFE PATH: " + name)
            continue
        if strict and name not in allowed:
            issues.append("SITE UNAPPROVED FILE: " + name)
            continue
        found.add(name)
        if name in theme and hashlib.sha256(file.read_bytes()).hexdigest() != theme[name]:
            issues.append("SITE THEME HASH MISMATCH: " + name)
        if name in images and hashlib.sha256(file.read_bytes()).hexdigest() != images[name]:
            issues.append("SITE IMAGE HASH MISMATCH: " + name)
        if file.suffix.lower() == ".html":
            count += 1
            try:
                html = file.read_text(encoding="utf-8")
                parser = PageParser(name, scripts)
                parser.feed(html)
                parser.close()
                issues.extend(parser.issues)
                visible = " ".join(parser.parts)
                if any(p.search(visible) for p in BANNED):
                    issues.append("SITE UNSAFE HTML TEXT: " + name)
                if any(INTERNAL.search(ref) for ref in parser.references) or INTERNAL.search(html):
                    issues.append("SITE INTERNAL URL: " + name)
            except (OSError, UnicodeError, ValueError):
                issues.append("SITE UNREADABLE HTML: " + name)
        elif name == "search/search_index.json":
            try:
                raw = file.read_text(encoding="utf-8")
                if any(p.search(raw) for p in BANNED) or INTERNAL.search(raw):
                    issues.append("SITE UNSAFE SEARCH INDEX")
            except (OSError, UnicodeError):
                issues.append("SITE UNREADABLE SEARCH INDEX")
    if count == 0:
        issues.append("SITE EMPTY: no rendered HTML")
    if "index.html" not in found:
        issues.append("SITE MISSING APPROVED PAGES")
    if strict:
        for name in sorted(approved_html | approved_sources | set(theme)):
            if name not in found:
                issues.append("SITE MISSING APPROVED ASSET: " + name)
    return sorted(set(issues))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=ROOT / "_site")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    errors = check_site(args.site, strict=args.strict)
    for error in errors:
        print("FAIL:", error)
    print("msc-rendered-site:", "FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
