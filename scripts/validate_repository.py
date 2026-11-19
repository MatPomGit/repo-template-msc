"""Static, dependency-free contract validator for an msc research repository."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

REQUIRED = (
    "README.md", "AGENTS.md", "ARCHITECTURE.md", "RESEARCH.md",
    "REPRODUCIBILITY.md", "PROJECT_STATE.yaml", "CITATION.cff",
    "LICENSE", "SECURITY.md", ".gitignore", ".gitattributes",
    "mkdocs.yml", "docs/index.md", "docs/outputs.md",
    "research/protocol.md", "research/analysis-plan.md",
    "research/ethics.md", "research/data-management.md",
    "research/preregistration.md", "research/decisions.md",
    "research/evidence-register.csv", "data/README.md",
    "results/README.md", "equipment/README.md",
    "software/dependencies.yaml", "manuscripts/P01/README.md",
    "manuscripts/P01/references.bib",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/research-task.md",
)

PROHIBITED_SEGMENTS = {"raw", "private", "processed-private"}
REQUIRED_STATE_KEYS = (
    "schema_version", "project_id", "repository_type", "programme",
    "research_phase", "ethics_status", "preregistration_status",
    "participant_data_status", "manuscript_root", "publication_tracks",
)
EVIDENCE_COLUMNS = (
    "evidence_id", "claim_id", "kind", "source_repository",
    "source_commit_sha", "dataset_reference", "dataset_sha256", "procedure",
    "environment", "observed_at_utc", "verification_status", "notes",
)


def validate(root: Path, phase: str = "scaffold") -> list[str]:
    """Check required structure and conservative readiness boundaries."""
    issues: list[str] = []
    if not root.is_dir():
        return [f"Missing repository directory: {root}"]

    for relative in REQUIRED:
        p = root / relative
        if not p.is_file() or p.is_symlink():
            issues.append(f"Missing required regular file: {relative}")
            continue
        if not p.read_bytes().strip():
            issues.append(f"Empty required file: {relative}")

    tracks = root / "manuscripts"
    manuscripts = sorted(p for p in tracks.iterdir() if p.is_dir()) if tracks.is_dir() else []
    if not manuscripts:
        issues.append("Missing manuscripts/P01 or another manuscript directory")
    for manuscript in manuscripts:
        if not (manuscript / "README.md").is_file():
            issues.append(f"Missing manuscript README: {manuscript.name}")
        if not any((manuscript / ("main" + ext)).is_file() for ext in (".qmd", ".tex", ".md")):
            issues.append(f"Missing main.qmd/main.tex/main.md: {manuscript.name}")
        if not (manuscript / "references.bib").is_file():
            issues.append(f"Missing references.bib: {manuscript.name}")

    state_path = root / "PROJECT_STATE.yaml"
    if state_path.is_file():
        state = state_path.read_text(encoding="utf-8")
        for key in REQUIRED_STATE_KEYS:
            if not re.search(r"(?m)^" + re.escape(key) + r":\s*", state):
                issues.append(f"Missing PROJECT_STATE.yaml key: {key}")
        if not re.search(r"(?m)^repository_type:\s*manuscript\s*$", state):
            issues.append("repository_type must be manuscript")
        if phase == "publish":
            if re.search(r"(?m)^(project_id|scientific_owner):\s*REPLACE", state):
                issues.append("Unresolved project identity/owner")
            if re.search(r"(?m)^programme:\s*unassigned", state):
                issues.append("Missing primary ARC programme")
    ev = root / "research/evidence-register.csv"
    if ev.is_file():
        with ev.open(encoding="utf-8", newline="") as handle:
            try:
                hdr = next(csv.reader(handle))
            except StopIteration:
                hdr = []
        if tuple(hdr) != EVIDENCE_COLUMNS:
            issues.append("Invalid evidence-register.csv header")

    if phase == "publish":
        for f in ("README.md", "CITATION.cff", "docs/index.md", "mkdocs.yml"):
            file = root / f
            if file.is_file() and ("REPLACE" in file.read_text(encoding="utf-8") or "[Tytuł" in file.read_text(encoding="utf-8")):
                issues.append(f"Unresolved template placeholder in {f}")
        if (root / "LICENSE").is_file() and "[WŁAŚCICIEL PRAW]" in (root / "LICENSE").read_text(encoding="utf-8"):
            issues.append("Unresolved copyright holder in LICENSE")
        for f in ("README.md", "docs/index.md", "docs/outputs.md"):
            file = root / f
            if file.is_file() and ("NOT_CONFIGURED" in file.read_text(encoding="utf-8") or "REPLACE" in file.read_text(encoding="utf-8")):
                issues.append(f"Publication metadata requires review: {f}")

    for p in root.rglob("*"):
        if not p.is_file() or p.is_symlink():
            continue
        rel = p.relative_to(root)
        if any(s in PROHIBITED_SEGMENTS for s in rel.parts):
            issues.append(f"Prohibited path in repository tree: {rel}")
    return sorted(set(issues))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--phase", choices=("scaffold", "publish"), default="scaffold")
    args = parser.parse_args(argv)
    problems = validate(args.root, args.phase)
    for issue in problems:
        print("FAIL:", issue)
    print(f"msc-contract: {'FAIL' if problems else 'PASS'}; phase={args.phase}; findings={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
