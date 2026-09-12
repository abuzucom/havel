#!/usr/bin/env python3
"""Verify the reference graph between AUDIT.md, docs/checks, and docs/regimes.

Structural defects exit 1. A stale review date warns and exits 0, matching the
advisory convention check_us_spelling.py sets. A finding and an infrastructure
failure are different events and carry different codes.
"""
import argparse
import datetime
import pathlib
import re
import sys

REFERENCE_PATTERN = re.compile(r"\[(2\.\d+)@([a-z0-9-]+)\]")
ANCHOR_PATTERN = re.compile(r"^### \[(2\.\d+)@([a-z0-9-]+)\]\s*$", re.MULTILINE)
REVIEWED_PATTERN = re.compile(r"^Last reviewed:[^\S\n]*(\S+)[^\S\n]*$", re.MULTILINE)
SOURCES_PATTERN = re.compile(r"^Sources:[^\S\n]*(\S[^\n]*)$", re.MULTILINE)
TABLE_ROW_PATTERN = re.compile(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
SLUG_IN_CELL_PATTERN = re.compile(r"`([a-z0-9-]+)`")

STALENESS_THRESHOLD_DAYS = 183
DISCLAIMER = "Not legal advice."
EVERY_SLUG_PHRASE = "every known slug"
NONE_PHRASE = "none"
RESERVED_SCOPES = frozenset({"undeclared"})
CHECK_FILE_PATTERN = re.compile(r"^2\.(\d+)\.md$")
PROFILES_FILENAME = "scope-profiles.md"
MATRIX_FILENAME = "README.md"
NON_REGIME_FILES = frozenset({PROFILES_FILENAME, MATRIX_FILENAME})


class ScopeError(ValueError):
    """A declared scope names something the profile table does not define."""


def _read(path: pathlib.Path) -> str:
    """Return the text of one file, or fail with a recovery action."""
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise SystemExit(
            f"{path}: cannot read ({error}). Restore the file or correct the path.")


def _split_sections(text: str, heading: str) -> str:
    """Return the body under one level-two heading, or an empty string."""
    marker = f"## {heading}"
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    return body.split("\n## ", 1)[0]


def load_profiles(root: pathlib.Path) -> dict:
    """Return the profile expansion and the slug set from the profile table."""
    text = _read(root / "docs" / "regimes" / PROFILES_FILENAME)
    slugs = [match[0] for match in TABLE_ROW_PATTERN.findall(
        _split_sections(text, "Slugs"))]
    known = set(slugs)
    profiles = {}
    for name, cell in TABLE_ROW_PATTERN.findall(_split_sections(text, "Profiles")):
        if EVERY_SLUG_PHRASE in cell:
            profiles[name] = set(known)
        elif cell.strip() == NONE_PHRASE:
            profiles[name] = set()
        else:
            profiles[name] = set(SLUG_IN_CELL_PATTERN.findall(cell))
    return {"profiles": profiles, "slugs": known}


def expand_scope(declared, profiles: dict) -> set:
    """Return the slug set a declared scope expands to.

    Accepts a comma-separated string or an iterable. Profile names, bare
    slugs, and the reserved word undeclared all resolve. An unknown name
    raises rather than resolving to nothing.
    """
    if isinstance(declared, str):
        names = [part.strip() for part in declared.split(",")]
    else:
        names = [str(part).strip() for part in declared]
    resolved = set()
    for name in names:
        if not name or name in RESERVED_SCOPES:
            continue
        if name in profiles["profiles"]:
            resolved |= profiles["profiles"][name]
        elif name in profiles["slugs"]:
            resolved.add(name)
        else:
            raise ScopeError(
                f"scope '{name}' matches no profile and no slug. "
                f"Add it to docs/regimes/{PROFILES_FILENAME} or correct the spelling.")
    return resolved


def _regime_files(root: pathlib.Path) -> list:
    """Return every regime file, excluding the profile table and the matrix."""
    directory = root / "docs" / "regimes"
    return sorted(
        path for path in directory.glob("*.md") if path.name not in NON_REGIME_FILES)


def _check_files(root: pathlib.Path) -> list:
    """Return every class check file in class order."""
    directory = root / "docs" / "checks"
    if not directory.is_dir():
        return []
    return sorted(
        (path for path in directory.glob("*.md") if CHECK_FILE_PATTERN.match(path.name)),
        key=lambda path: int(CHECK_FILE_PATTERN.match(path.name).group(1)))


def _known_classes(root: pathlib.Path) -> set:
    """Return the class numbers the check files define."""
    return {path.stem for path in _check_files(root)}


def collect_references(root: pathlib.Path) -> dict:
    """Return every reference token mapped to the files citing it."""
    references = {}
    sources = [root / "AUDIT.md"] + _check_files(root)
    for path in sources:
        if not path.is_file():
            continue
        for class_number, slug in REFERENCE_PATTERN.findall(_read(path)):
            references.setdefault((class_number, slug), []).append(path.name)
    return references


def collect_anchors(root: pathlib.Path) -> dict:
    """Return every anchor token mapped to its defining file."""
    anchors = {}
    for path in _regime_files(root):
        for class_number, slug in ANCHOR_PATTERN.findall(_read(path)):
            anchors.setdefault((class_number, slug), []).append(path.name)
    return anchors


def check_graph(root: pathlib.Path, profiles: dict) -> list:
    """Return every reference-graph failure as a message."""
    failures = []
    known_classes = _known_classes(root)
    references = collect_references(root)
    anchors = collect_anchors(root)

    for path in _check_files(root):
        for class_number, slug in ANCHOR_PATTERN.findall(_read(path)):
            failures.append(
                f"{path.name}: defines anchor [{class_number}@{slug}]. "
                f"A definition site belongs in docs/regimes/{slug}.md. "
                "Move the subsection or change the anchor to a reference.")

    for (class_number, slug), citing in sorted(references.items()):
        where = ", ".join(sorted(set(citing)))
        if known_classes and class_number not in known_classes:
            failures.append(
                f"{where}: references unknown class {class_number}. "
                f"Add docs/checks/{class_number}.md or correct the token.")
        if slug not in profiles["slugs"]:
            failures.append(
                f"{where}: references unknown slug '{slug}'. "
                f"Add it to docs/regimes/{PROFILES_FILENAME} or correct the token.")
        elif (class_number, slug) not in anchors:
            failures.append(
                f"{where}: token [{class_number}@{slug}] has no definition site. "
                f"Add '### [{class_number}@{slug}]' to docs/regimes/{slug}.md "
                "or remove the reference.")

    for (class_number, slug), defining in sorted(anchors.items()):
        where = ", ".join(sorted(set(defining)))
        if (class_number, slug) not in references:
            failures.append(
                f"{where}: anchor [{class_number}@{slug}] is never referenced. "
                f"Cite it from docs/checks/{class_number}.md or remove the subsection.")
        if len(set(defining)) > 1:
            failures.append(
                f"{where}: anchor [{class_number}@{slug}] has several definition sites. "
                "Keep exactly one.")
    return failures


def check_headers(root: pathlib.Path, today: datetime.date) -> tuple:
    """Return regime header failures and staleness warnings."""
    failures = []
    warnings = []
    for path in _regime_files(root):
        text = _read(path)
        if DISCLAIMER not in text:
            failures.append(
                f"{path.name}: header omits the not-legal-advice line. "
                f"Add a line beginning '{DISCLAIMER}'.")
        sources = SOURCES_PATTERN.search(text)
        if sources is None or not sources.group(1).strip():
            failures.append(
                f"{path.name}: header omits a non-empty Sources line. "
                "Add the statutory and regulator URLs the file draws from.")
        reviewed = REVIEWED_PATTERN.search(text)
        if reviewed is None:
            failures.append(
                f"{path.name}: header omits a Last reviewed line. "
                "Add the date the file was last checked against the source.")
            continue
        raw = reviewed.group(1)
        try:
            reviewed_on = datetime.date.fromisoformat(raw)
        except ValueError:
            failures.append(
                f"{path.name}: Last reviewed value {raw} is not an ISO date. "
                "Use YYYY-MM-DD.")
            continue
        if reviewed_on > today:
            failures.append(
                f"{path.name}: Last reviewed value {raw} falls in the future. "
                "Set it to the date the file was last checked against the source.")
            continue
        age = (today - reviewed_on).days
        if age > STALENESS_THRESHOLD_DAYS:
            warnings.append(
                f"{path.name}: Last reviewed {age} days ago. "
                "Re-read the source and refresh the date.")
    return failures, warnings


def check_profiles(root: pathlib.Path, profiles: dict) -> list:
    """Return every profile-table failure as a message."""
    failures = []
    known = profiles["slugs"]
    reachable = set()
    for name, expansion in sorted(profiles["profiles"].items()):
        unknown = sorted(expansion - known)
        if unknown:
            failures.append(
                f"{PROFILES_FILENAME}: profile '{name}' expands to unknown "
                f"{', '.join(unknown)}. Add each to the slug table or correct the row.")
        reachable |= expansion
    orphans = sorted(known - reachable)
    if orphans:
        failures.append(
            f"{PROFILES_FILENAME}: {', '.join(orphans)} appear in no profile. "
            "Add each to at least one profile row so a declaration can reach it.")
    present = {path.stem for path in _regime_files(root)}
    for slug in sorted(known - present):
        failures.append(
            f"{PROFILES_FILENAME}: slug '{slug}' has no docs/regimes/{slug}.md. "
            "Add the file or remove the slug.")
    for slug in sorted(present - known):
        failures.append(
            f"docs/regimes/{slug}.md: slug '{slug}' is absent from the slug table. "
            f"Add it to docs/regimes/{PROFILES_FILENAME} or remove the file.")
    return failures


def build_matrix(root: pathlib.Path, profiles: dict) -> str:
    """Return the class-by-regime matrix as markdown."""
    anchors = collect_anchors(root)
    slugs = sorted(profiles["slugs"])
    classes = sorted(_known_classes(root), key=lambda value: int(value.split(".")[1]))
    lines = [
        "# Regime delta matrix",
        "",
        "Generated by `scripts/check_regime_refs.py --write-matrix`. Do not edit.",
        "",
        "A mark shows a `[class@slug]` delta exists. An empty cell means the",
        "regime leaves that class at baseline.",
        "",
        "| Class | " + " | ".join(slugs) + " |",
        "|---|" + "---|" * len(slugs),
    ]
    for class_number in classes:
        cells = ["x" if (class_number, slug) in anchors else "" for slug in slugs]
        lines.append(f"| {class_number} | " + " | ".join(cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    """Check the reference graph and return a process exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--write-matrix", action="store_true",
                        help="regenerate docs/regimes/README.md")
    arguments = parser.parse_args(argv)
    root = pathlib.Path(arguments.root).resolve()
    directory = root / "docs" / "regimes"
    if not directory.is_dir():
        print(f"{directory}: directory missing. Run from the repository root.",
              file=sys.stderr)
        return 1

    profiles = load_profiles(root)
    failures = check_profiles(root, profiles)
    failures += check_graph(root, profiles)
    header_failures, warnings = check_headers(root, datetime.date.today())
    failures += header_failures

    for warning in warnings:
        print(f"warning: {warning}")
    for failure in failures:
        print(f"error: {failure}", file=sys.stderr)
    if failures:
        return 1
    if arguments.write_matrix:
        (directory / MATRIX_FILENAME).write_text(
            build_matrix(root, profiles), encoding="utf-8")
        print(f"wrote docs/regimes/{MATRIX_FILENAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
