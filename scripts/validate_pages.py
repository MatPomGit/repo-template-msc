"""Static, fail-closed source allowlist for public GitHub Pages (stdlib only).

Does not publish content, inspect remote Pages settings or certify privacy.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EXT = {".md", ".html", ".css", ".js", ".svg", ".png", ".jpg",
               ".jpeg", ".webp", ".avif", ".ico"}
TEXT_EXT = {".md", ".html", ".css", ".js", ".svg"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".avif", ".ico"}
UNSAFE_SEGMENTS = {"docs", "research", "manuscripts", "software",
                   "data", "results", "equipment", "secrets", "credentials",
                   "private", "raw", "students", "participants",
                   "agents.md", "contributing.md", "internal"}
BANNED = (
    re.compile(r"\b(?:AGENTS\.md|AGENT_WORKFLOW|CONTRIBUTING(?:\.md)?)\b", re.I),
    re.compile(r"\b(?:TODO|FIXME|REPLACE(?:_[A-Z0-9_]+)?|PLACEHOLDER|TBD|"
               r"NOT_RUN|NOT_VERIFIED|NOT_CONFIGURED|NOT_ASSESSED|NOT_COLLECTED)\b", re.I),
    re.compile(r"(?:instrukcj\w*\s+dla\s+agent\w*|poleceni\w*\s+dla\s+agent\w*|"
               r"dla\s+agenta\s*:|agent\s*:\s*(?:wykonaj|zmień|dodaj|popraw|sprawdź)|"
               r"agent instructions|system prompt|developer instructions)", re.I),
    re.compile(r"(?:uwagi?\s+redakcyjne|notatk\w*\s+(?:dla\s+)?(?:autora|redaktora)|"
               r"editorial notes?|notes? to (?:author|editor)|"
               r"przed publikacją|do uzupełnienia|wstaw tutaj)", re.I),
    re.compile(r"(?:jak\s+(?:pomóc|wspierać)\s+(?:projekt|repozytorium)|"
               r"how to contribute|contributing guidelines|"
               r"contribute to (?:this|the) (?:project|repository)|"
               r"send (?:a )?pull request)", re.I),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?<![A-Za-z0-9])gh[pousr]_[A-Za-z0-9_]{36,}(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9])AKIA[0-9A-Z]{16}(?![0-9A-Z])"),
    re.compile(r"\b(?:asystenc\w*\s+AI|ChatGPT|Copilot|AI\s+agent|AI\s+assistant)\b"
               r"\s*[,;:-]?\s*(?:wykonaj|zmień|popraw|zaktualizuj|usuń|dodaj|napisz|"
               r"create|update|ignore|rewrite|remove|edit|write)\b", re.I),
    re.compile(r"<\s*/?\s*(?:script|iframe|object|embed|form|meta|base)\b|"
               r"\bon[a-z]+\s*=|\b(?:javascript|vbscript)\s*:", re.I),
)


def safe_relative(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        return False
    if value.startswith(("/", "./")) or "//" in value:
        return False
    parts = PurePosixPath(value).parts
    return bool(parts) and all(
        item not in {".", "..", ""} and not item.startswith(".")
        and item.lower() not in UNSAFE_SEGMENTS for item in parts
    ) and PurePosixPath(value).suffix.lower() in ALLOWED_EXT


# Validate link destinations in addition to the source-file allowlist. This is a
# conservative static check; final rendered HTML still requires a human review.
PRIVATE_LINK_SEGMENTS = UNSAFE_SEGMENTS | {
    ".github", "config", "scripts", "tests", "project_state.yaml",
    "architecture.md", "security.md", "research.md", "reproducibility.md",
    "template_setup.md", "governance.md", "agent_workflow.md",
}
MD_INLINE_TARGET = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)\n]+))"
)
MD_REFERENCE_TARGET = re.compile(
    r"(?m)^\s{0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]+)>|(\S+))"
)
CSS_TARGET = re.compile(
    r"\burl\(\s*(?:[\"']([^\"']+)[\"']|([^\"'\s)]+))\s*\)", re.I
)
CSS_IMPORT = re.compile(r"@import\s+[\"']([^\"']+)[\"']", re.I)


class _HtmlLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value is None:
                continue
            if key in {"href", "src", "poster", "action", "formaction"}:
                self.targets.append(value)
            elif key == "srcset":
                self.targets.extend(item.strip().split()[0] for item in value.split(",")
                                    if item.strip())


def extract_targets(content: str) -> list[str]:
    targets: list[str] = []
    for pattern in (MD_INLINE_TARGET, MD_REFERENCE_TARGET, CSS_TARGET, CSS_IMPORT):
        targets.extend(next((v for v in match.groups() if v is not None), "")
                       for match in pattern.finditer(content))
    parser = _HtmlLinks()
    parser.feed(content)
    targets.extend(parser.targets)
    return targets


def unsafe_public_reference(target: str, source: str, allowed: set[str]) -> bool:
    """Reject non-allowlisted local destinations and GitHub source-file links."""
    url = unquote(html.unescape(target.strip().strip("<>")))
    if not url or url.startswith("#"):
        return False
    if "\\" in url or "\0" in url:
        return True
    try:
        parsed = urlsplit(url)
    except ValueError:
        return True
    if parsed.scheme in {"mailto", "tel"}:
        return False
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return True
    if parsed.scheme in {"http", "https"} and not parsed.netloc:
        return True
    if parsed.netloc:
        host = (parsed.hostname or "").lower()
        segments = [unquote(part).lower() for part in parsed.path.split("/") if part]
        if host == "github.com" and len(segments) >= 4 and segments[2] in {"blob", "raw", "tree"}:
            repo_path = segments[3:]
        elif host == "raw.githubusercontent.com" and len(segments) >= 4:
            repo_path = segments[2:]
        elif host == "api.github.com" and len(segments) >= 5 and segments[:1] == ["repos"] and "contents" in segments:
            repo_path = segments[segments.index("contents") + 1:]
        else:
            return False
        return any(part in PRIVATE_LINK_SEGMENTS for part in repo_path)
    path = unquote(parsed.path)
    if not path or path == "/":
        return False
    if "\\" in path or "\0" in path or any(item == ".." for item in path.split("/")):
        return True
    if path.startswith("/"):
        relative = posixpath.normpath(path.lstrip("/"))
    else:
        relative = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
    parts = relative.lower().split("/")
    return (relative.startswith("../") or relative in {"..", "."}
            or any(part in PRIVATE_LINK_SEGMENTS for part in parts)
            or relative not in allowed)


def parse_mkdocs(text: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Only a transparent, offline MkDocs configuration is supported."""
    keys: dict[str, str] = {}
    navigation: list[str] = []
    errors: list[str] = []
    mode = ""
    theme: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        if top:
            key, value = top.groups()
            if key not in {"site_name", "docs_dir", "site_dir", "nav", "theme"} or key in keys:
                errors.append("PAGES CONFIG: unreviewed or duplicate config key")
            else:
                keys[key] = value.strip("\"'")
            mode = key if key in {"nav", "theme"} else ""
            continue
        if mode == "nav":
            item = re.fullmatch(r"  - [^:]+:\s*([A-Za-z0-9_./-]+\.md)\s*", line)
            if item:
                navigation.append(item.group(1))
                continue
        if mode == "theme":
            field = re.fullmatch(r"  (name|highlightjs):\s*([a-z]+)\s*", line)
            if field and field.group(1) not in theme:
                theme[field.group(1)] = field.group(2)
                continue
        errors.append("PAGES CONFIG: unreviewed YAML content")
    if keys.get("docs_dir") != "pages" or keys.get("site_dir") != "_site":
        errors.append("PAGES CONFIG: isolated docs_dir/pages and site_dir/_site required")
    if not keys.get("site_name") or "nav" not in keys or not navigation:
        errors.append("PAGES CONFIG: site name or navigation missing")
    if keys.get("theme") != "" or theme != {"name": "mkdocs", "highlightjs": "false"}:
        errors.append("PAGES CONFIG: approved offline theme required")
    return keys, navigation, errors



def check_pages(root: Path = ROOT) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []
    try:
        data = json.loads((root / "config/pages-policy.json").read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return ["PAGES POLICY: missing or malformed JSON"]
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        return ["PAGES POLICY: unsupported schema_version"]
    if (data.get("source_dir"), data.get("output_dir"),
            data.get("mkdocs_config")) != ("pages", "_site", "mkdocs.yml"):
        errors.append("PAGES POLICY: source, output and MkDocs paths must remain isolated")
    allowed = data.get("public_files")
    if not isinstance(allowed, list) or not allowed or any(not safe_relative(x) for x in allowed):
        return sorted(set(errors + ["PAGES POLICY: unsafe public file allowlist"]))
    if len(allowed) != len(set(allowed)) or "index.md" not in allowed:
        errors.append("PAGES POLICY: duplicate or missing index")
    approved_theme = data.get("approved_theme_assets")
    approved_images = data.get("approved_image_sha256")
    if (not isinstance(approved_theme, dict) or not approved_theme or
            not isinstance(approved_images, dict) or
            any(not isinstance(k, str) or not isinstance(v, str) or
                not re.fullmatch(r"[0-9a-f]{64}", v)
                for k, v in approved_theme.items()) or
            any(not isinstance(k, str) or k not in allowed or
                PurePosixPath(k).suffix.lower() not in IMAGE_EXT or
                not isinstance(v, str) or not re.fullmatch(r"[0-9a-f]{64}", v)
                for k, v in approved_images.items())):
        return sorted(set(errors + ["PAGES POLICY: invalid approved asset hashes"]))
    try:
        config = (root / "mkdocs.yml").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return sorted(set(errors + ["PAGES CONFIG: missing or unreadable mkdocs.yml"]))
    _, nav, config_errors = parse_mkdocs(config)
    errors.extend(config_errors)
    if not nav or "index.md" not in nav or any(x not in allowed for x in nav):
        errors.append("PAGES CONFIG: navigation contains unapproved source")

    folder = root / "pages"
    if not folder.is_dir() or folder.is_symlink():
        return sorted(set(errors + ["PAGES SOURCE: missing or unsafe directory"]))
    for file in sorted(folder.rglob("*")):
        rel = file.relative_to(folder).as_posix()
        if file.is_symlink():
            errors.append("PAGES SYMLINK: " + rel)
            continue
        if file.is_dir():
            continue
        if not file.is_file():
            errors.append("PAGES UNSUPPORTED: " + rel)
            continue
        if not safe_relative(rel) or rel not in allowed:
            errors.append("PAGES NOT APPROVED: " + rel)
            continue
        try:
            if not file.resolve(strict=True).is_relative_to(folder):
                errors.append("PAGES OUTSIDE SOURCE: " + rel)
                continue
            if file.stat().st_size > 2_000_000:
                errors.append("PAGES TOO LARGE: " + rel)
                continue
            if file.suffix.lower() in IMAGE_EXT:
                body = file.read_bytes()
                if hashlib.sha256(body).hexdigest() != approved_images.get(rel):
                    errors.append("PAGES IMAGE HASH UNAPPROVED: " + rel)
                # Conservative metadata indicator screen; never a full media audit.
                if (file.suffix.lower() != ".ico" and
                        any(marker in body for marker in
                            (b"Exif\x00\x00", b"eXIf", b"XMP_", b"<x:xmpmeta",
                             b"http://ns.adobe.com/xap/1.0/", b"tEXt", b"iTXt", b"zTXt"))):
                    errors.append("PAGES IMAGE METADATA: " + rel)
            if file.suffix.lower() in TEXT_EXT:
                content = file.read_text(encoding="utf-8")
                if any(regex.search(content) for regex in BANNED):
                    errors.append("PAGES EDITORIAL OR AGENT CONTENT: " + rel)
                if any(unsafe_public_reference(target, rel, set(allowed))
                       for target in extract_targets(content)):
                    errors.append("PAGES INTERNAL REFERENCE: " + rel)
        except (OSError, UnicodeError):
            errors.append("PAGES UNREADABLE: " + rel)
    for rel in allowed:
        file = folder / rel
        if not file.is_file() or file.is_symlink():
            errors.append("PAGES MISSING APPROVED FILE: " + rel)
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check_pages(args.root)
    for error in errors:
        print("FAIL:", error)
    print("msc-pages:", "FAIL" if errors else "PASS")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
