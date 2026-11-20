"""Offline Unicode character budgets for msc research documentation.

Configuration: config/documentation-policy.json. Does not alter source files.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
POLICY = "config/documentation-policy.json"


def _valid_rel_path(value: str, allow_glob: bool = False) -> bool:
    """Reject paths outside the repository, including platform separators."""
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return False
    return allow_glob or not any(ch in value for ch in "*?[]")


def _valid_limit(value: object) -> bool:
    return type(value) is int and 100 <= value <= 100000



# Scientific documents may be migrated to explicitly mapped PROJECT_STATE paths.
# Apply the same budgets to those actual paths rather than enforcing placeholders.
SCIENTIFIC_DOCUMENT_PATHS = {
    "research/protocol.md": "protocol_path",
    "research/analysis-plan.md": "analysis_plan_path",
    "research/ethics.md": "ethics_path",
    "research/data-management.md": "data_management_path",
    "research/preregistration.md": "preregistration_path",
    "research/decisions.md": "decisions_path",
}


def scientific_document_mappings(root: Path, errors: list[str]) -> dict[str, str]:
    path = root / "PROJECT_STATE.yaml"
    try:
        value = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        errors.append("DOC POLICY: PROJECT_STATE.yaml unreadable")
        return {}
    result: dict[str, str] = {}
    for standard, field in SCIENTIFIC_DOCUMENT_PATHS.items():
        match = re.search(r"(?m)^" + re.escape(field) + r":\s*([^\r\n#]*)", value)
        mapped = (match.group(1).strip().strip("'\\\"") if match else "") or standard
        if not _valid_rel_path(mapped) or not mapped.endswith(".md"):
            errors.append("DOC POLICY: unsafe scientific document mapping " + field)
            continue
        result[standard] = mapped
    return result

def check_documentation(root: Path = ROOT) -> list[str]:
    """Return deterministic validation errors; unknown/invalid policies fail closed."""
    root = Path(root).resolve()
    try:
        policy = json.loads((root / POLICY).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError):
        return ["DOC POLICY: missing or malformed " + POLICY]
    if not isinstance(policy, dict) or type(policy.get("schema_version")) is not int or policy["schema_version"] != 1:
        return ["DOC POLICY: unsupported schema_version"]
    if policy.get("count_method") != "unicode_codepoints":
        return ["DOC POLICY: expected unicode_codepoints"]
    exact = policy.get("exact_limits")
    glob = policy.get("glob_limits")
    if not isinstance(exact, dict) or not isinstance(glob, dict) or not exact or not glob:
        return ["DOC POLICY: exact_limits and glob_limits required"]

    errors: list[str] = []
    for rules, is_glob in ((exact, False), (glob, True)):
        for path, limit in rules.items():
            if not _valid_rel_path(path, allow_glob=is_glob) or not _valid_limit(limit):
                errors.append("DOC POLICY: invalid limit or path " + str(path))
    if errors:
        return sorted(set(errors))

    mapped = scientific_document_mappings(root, errors)
    if errors:
        return sorted(set(errors))
    selected: dict[str, int] = {}
    for path, limit in exact.items():
        final = mapped.get(path, path)
        selected[final] = min(limit, selected.get(final, limit))
    for pattern, limit in glob.items():
        try:
            matched = list(root.glob(pattern))
        except (ValueError, OSError):
            errors.append("DOC POLICY: invalid glob " + pattern)
            continue
        for file in matched:
            rel = file.relative_to(root).as_posix()
            if rel not in selected:
                selected[rel] = min(limit, selected.get(rel, limit))
            elif rel not in mapped.values():
                selected[rel] = min(limit, selected[rel])

    for rel, limit in sorted(selected.items()):
        file = root / rel
        if file.is_symlink():
            errors.append("DOC SYMLINK: " + rel)
            continue
        if not file.is_file():
            if rel in exact:
                errors.append("DOC MISSING: " + rel)
            continue
        try:
            if not file.resolve(strict=True).is_relative_to(root):
                errors.append("DOC OUTSIDE REPO: " + rel)
                continue
            count = len(file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError):
            errors.append("DOC UNREADABLE: " + rel)
            continue
        if count > limit:
            errors.append(f"DOC LENGTH EXCEEDED: {rel} ({count}/{limit} chars)")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = check_documentation(args.root)
    for error in errors:
        print("ERROR:", error)
    print("FAIL: documentation" if errors else "PASS: documentation")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
