"""Static, dependency-free contract validator for an msc research repository."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path, PurePosixPath

REQUIRED = (
    "README.md", "AGENTS.md", "ARCHITECTURE.md", "RESEARCH.md",
    "REPRODUCIBILITY.md", "PROJECT_STATE.yaml", "CITATION.cff",
    "LICENSE", "SECURITY.md", ".gitignore", ".gitattributes",
    "mkdocs.yml", "docs/index.md", "docs/outputs.md",
    "data/README.md", "results/README.md", "equipment/README.md",
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


# Every scientific obligation stays mandatory, even if a migrated project
# uses different physical paths. These are only mapping defaults.
DOCUMENTS = {
    "protocol_path": "research/protocol.md",
    "analysis_plan_path": "research/analysis-plan.md",
    "ethics_path": "research/ethics.md",
    "data_management_path": "research/data-management.md",
    "preregistration_path": "research/preregistration.md",
    "decisions_path": "research/decisions.md",
    "evidence_register_path": "research/evidence-register.csv",
    "software_manifest_path": "software/dependencies.yaml",
}


def state_scalar(text: str, key: str) -> str | None:
    match = re.search(r"(?m)^" + re.escape(key) + r":\s*([^\r\n#]*)", text)
    if not match:
        return None
    return match.group(1).strip().strip("'\\\"")


def relative_file(root: Path, candidate: str | None) -> Path | None:
    if not isinstance(candidate, str) or not candidate or chr(92) in candidate:
        return None
    path = PurePosixPath(candidate)
    if path.is_absolute() or any(piece in (".", "..") for piece in candidate.split("/")):
        return None
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", candidate):
        return None
    target = root.joinpath(*path.parts)
    try:
        if target.resolve().is_relative_to(root.resolve()) and not target.is_symlink():
            return target
    except (OSError, ValueError):
        pass
    return None


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

    state_path = root / "PROJECT_STATE.yaml"
    state = state_path.read_text(encoding="utf-8") if state_path.is_file() else ""
    for key, default in DOCUMENTS.items():
        relative = state_scalar(state, key) or default
        target = relative_file(root, relative)
        if target is None or not target.is_file() or target.stat().st_size == 0:
            issues.append(f"Missing or unsafe required {key}: {relative}")

    manuscript_root = state_scalar(state, "manuscript_root") or "manuscripts"
    tracks = relative_file(root, manuscript_root)
    if tracks is None or not tracks.is_dir():
        issues.append(f"Missing or unsafe manuscript_root: {manuscript_root}")
    else:
        explicit_source = state_scalar(state, "manuscript_source")
        if explicit_source:
            source_file = relative_file(root, explicit_source)
            if (source_file is None or not source_file.is_file()
                    or source_file.suffix not in (".qmd", ".tex", ".md")
                    or not source_file.relative_to(root).as_posix().startswith(manuscript_root + "/")):
                issues.append(f"Missing or unsafe manuscript_source: {explicit_source}")
            bibliography = state_scalar(state, "bibliography_path") or (manuscript_root + "/references.bib")
            bib = relative_file(root, bibliography)
            if bib is None or not bib.is_file():
                issues.append(f"Missing bibliography: {bibliography}")
        else:
            manuscripts = sorted(p for p in tracks.iterdir() if p.is_dir() and not p.is_symlink())
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
    ev = relative_file(root, state_scalar(state, "evidence_register_path") or DOCUMENTS["evidence_register_path"])
    if ev is not None and ev.is_file():
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
