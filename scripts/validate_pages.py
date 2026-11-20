"""Static, fail-closed source allowlist for public GitHub Pages (stdlib only).

Does not publish content, inspect remote Pages settings or certify privacy.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EXT = {".md", ".html", ".css", ".js", ".svg", ".png", ".jpg",
               ".jpeg", ".webp", ".avif", ".ico"}
TEXT_EXT = {".md", ".html", ".css", ".js", ".svg"}
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


def parse_mkdocs(text: str) -> tuple[dict[str, str], list[str], list[str]]:
    """Allow only a small, transparent subset of MkDocs YAML; reject plugins/hooks."""
    keys: dict[str, str] = {}
    navigation: list[str] = []
    errors: list[str] = []
    in_nav = False
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.fullmatch(r"([a-z_]+):\s*(.*?)\s*", line)
        if top:
            key, val = top.groups()
            if key not in {"site_name", "docs_dir", "site_dir", "nav"} or key in keys:
                errors.append("PAGES CONFIG: unreviewed or duplicate config key")
            else:
                keys[key] = val.strip("\"'")
            in_nav = key == "nav"
            continue
        item = re.fullmatch(r"  - [^:]+:\s*([A-Za-z0-9_./-]+\.md)\s*", line)
        if in_nav and item:
            navigation.append(item.group(1))
            continue
        errors.append("PAGES CONFIG: unreviewed YAML content")
    if keys.get("docs_dir") != "pages" or keys.get("site_dir") != "_site":
        errors.append("PAGES CONFIG: isolated docs_dir/pages and site_dir/_site required")
    if not keys.get("site_name") or "nav" not in keys or not navigation:
        errors.append("PAGES CONFIG: site name or navigation missing")
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
            if file.suffix.lower() in TEXT_EXT:
                content = file.read_text(encoding="utf-8")
                if any(regex.search(content) for regex in BANNED):
                    errors.append("PAGES EDITORIAL OR AGENT CONTENT: " + rel)
                if re.search(r"\.\./|file://|https?://\S*(?:/AGENTS\.md|/\.github/|/research/|/docs/)",
                             content, re.I):
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
