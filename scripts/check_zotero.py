#!/usr/bin/env python3
"""Offline Zotero/Better BibTeX bibliographic contract (no Zotero API or login)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FIELDS = {
    "schema_version", "manager", "exporter", "bibliography",
    "auto_export_status", "keep_updated_required", "export_notes",
    "export_attachments", "export_annotations",
}
BIB_START = re.compile(r"(?im)^[ \t]*@([A-Za-z]+)\s*[{(]")
BIB_ENTRY = re.compile(r"(?im)^[ \t]*@([A-Za-z]+)\s*[{(]\s*([^,\s{}()]+)\s*,")
BIB_SPECIAL = {"string", "preamble", "comment"}
CITATION = re.compile(
    r"\\(?:cite(?:t|p|author|year|yearpar|alp|alt)?|autocite|parencite|"
    r"textcite|footcite|nocite)\*?\s*(?:\[[^\]]*\]\s*){0,2}\{([^{}]+)\}"
)
PRIVATE_FIELD = re.compile(
    r"(?im)^[ \t]*(?:file|files|attachment|attachments|annotation|annote|pdf)\s*="
)
KEY = re.compile(r"[A-Za-z0-9][A-Za-z0-9_:+./-]*\Z")


def without_tex_comments(value: str) -> str:
    lines = []
    for line in value.splitlines():
        for i, char in enumerate(line):
            if char != "%":
                continue
            backslashes = 0
            p = i - 1
            while p >= 0 and line[p] == "\\":
                backslashes += 1
                p -= 1
            if backslashes % 2 == 0:
                line = line[:i]
                break
        lines.append(line)
    return "\n".join(lines)


def used_keys(manuscript: Path) -> set[str]:
    cited = set()
    for file in sorted(manuscript.rglob("*")):
        if file.is_symlink() or not file.is_file() or file.suffix not in (".tex", ".qmd", ".md"):
            continue
        if file.stat().st_size > 1_000_000:
            continue
        content = file.read_text(encoding="utf-8")
        if file.suffix == ".tex":
            for cited_group in CITATION.findall(without_tex_comments(content)):
                cited.update(k.strip() for k in cited_group.split(",")
                             if k.strip() and k.strip() != "*")
        else:
            for bracket in re.findall(r"\[[^\]\n]*@[^\]\n]+\]", content):
                cited.update(re.findall(r"(?<![A-Za-z0-9])@([A-Za-z0-9_:+./-]+)", bracket))
    return cited


def bibliography_keys(content: str) -> tuple[set[str], list[str]]:
    found: set[str] = set()
    errors: list[str] = []
    parsed = 0
    for match in BIB_ENTRY.finditer(content):
        if match.group(1).lower() in BIB_SPECIAL:
            continue
        parsed += 1
        key = match.group(2)
        if not KEY.fullmatch(key):
            errors.append(f"Unsafe BibTeX citation key: {key}")
        if key in found:
            errors.append(f"Duplicate BibTeX citation key: {key}")
        found.add(key)
    expected = sum(m.group(1).lower() not in BIB_SPECIAL for m in BIB_START.finditer(content))
    if parsed < expected:
        errors.append("Unparseable BibTeX entry header")
    if PRIVATE_FIELD.search(content):
        errors.append("BibTeX contains attachment/annotation field; disable export")
    return found, errors


def validate_manuscript(manuscript: Path, require_setup: bool = False) -> list[str]:
    errors = []
    config_file = manuscript / "zotero.json"
    if config_file.is_symlink() or not config_file.is_file():
        return ["Missing Zotero descriptor: zotero.json"]
    try:
        if config_file.stat().st_size > 20_000:
            raise ValueError("Descriptor exceeds size limit")
        cfg = json.loads(config_file.read_text(encoding="utf-8"))
        if not isinstance(cfg, dict):
            raise ValueError("Expected JSON object")
    except (OSError, UnicodeError, ValueError):
        return ["Invalid Zotero descriptor"]
    if set(cfg) - FIELDS:
        errors.append("Unexpected Zotero settings; credentials and IDs are forbidden")
    if cfg.get("schema_version") != 1 or cfg.get("manager") != "zotero":
        errors.append("Invalid Zotero descriptor schema or manager")
    if cfg.get("exporter") != "Better BibTeX":
        errors.append("Use Better BibTeX translator for BibTeX/natbib")
    if cfg.get("auto_export_status") not in ("configured", "not_configured"):
        errors.append("Invalid Zotero auto-export status")
    for name, expected in (
        ("keep_updated_required", True),
        ("export_notes", False),
        ("export_attachments", False),
        ("export_annotations", False),
    ):
        if cfg.get(name) is not expected:
            errors.append(f"Unsafe Zotero export option: {name}")
    filename = cfg.get("bibliography")
    if (not isinstance(filename, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+\.bib", filename)
            or filename.startswith(".")):
        return sorted(set(errors + ["Unsafe Zotero bibliography filename"]))
    bib = manuscript / filename
    if bib.is_symlink() or not bib.is_file():
        return sorted(set(errors + [f"Missing Zotero bibliography: {filename}"]))
    if bib.stat().st_size > 8_000_000:
        return sorted(set(errors + ["Zotero bibliography exceeds review size limit"]))
    try:
        available, issues = bibliography_keys(bib.read_text(encoding="utf-8"))
        needed = used_keys(manuscript)
    except (OSError, UnicodeError):
        return sorted(set(errors + ["Unreadable bibliography/manuscript source"]))
    errors.extend(issues)
    errors.extend(f"Missing Zotero citation key: {key}" for key in sorted(needed - available))
    if require_setup:
        if cfg.get("auto_export_status") != "configured":
            errors.append("Zotero auto-export setup not confirmed by owner")
        if not available:
            errors.append("No bibliography entries exported from Zotero")
    return sorted(set(errors))


def validate_root(root: Path, require_setup: bool = False) -> tuple[list[str], int]:
    errors: list[str] = []
    found = 0
    manuscript_root = root / "manuscripts"
    if not manuscript_root.is_dir():
        return errors, found
    for path in sorted(manuscript_root.iterdir()):
        if path.is_symlink() or not path.is_dir() or not (path / "zotero.json").exists():
            continue
        found += 1
        errors.extend(f"{path.name}: {issue}" for issue in validate_manuscript(path, require_setup))
    return errors, found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--require-setup", action="store_true")
    args = parser.parse_args(argv)
    problems, count = validate_root(args.root, args.require_setup)
    for issue in problems:
        print("FAIL:", issue)
    print(f"zotero-contract: {'FAIL' if problems else 'PASS'};"
          f" configured_manuscripts={count}; Zotero live sync NOT_VERIFIED")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
