#!/usr/bin/env python3
"""Behavior of the regime reference checker.

The checker guards the reference graph between AUDIT.md, docs/checks, and
docs/regimes. An untested checker leaves that graph unguarded.
"""
import datetime
import importlib.util
import os
import pathlib
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retrying_temp_directory import RetryingTemporaryDirectory

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKER_PATH = REPO_ROOT / "scripts" / "check_regime_refs.py"


def _load_checker():
    """Import the checker by path."""
    spec = importlib.util.spec_from_file_location("check_regime_refs", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()

PROFILES = """# Scope profiles

## Profiles

| Profile | Expands to |
|---|---|
| `all` | every known slug |
| `baseline` | none |
| `eu` | `gdpr` |

## Slugs

| Slug | Regime |
|---|---|
| `gdpr` | General Data Protection Regulation |
"""

REGIME = """# General Data Protection Regulation (gdpr)
Last reviewed: {date}
Sources: https://example.invalid/gdpr
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Signals.

## Class deltas

### [2.1@gdpr]
A delta.
Severity shift: none.

## Terms of art

- Controller maps to the controller.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond | One month | None |

## What this regime does not add

- Nothing.
"""

CHECK = """# 2.1 Lawful Basis

## Barrier list

- **A barrier.** A defect. A check. A harm. Fix: a fix.

## Severity posture

- **HIGH:** something.

## Thresholds

- Baseline: a floor. Regime deltas: `[2.1@gdpr]`.

## How to investigate

1. Look.

## Boundaries

- 2.2 owns something else. 2.1 owns this.
"""


def build_tree(root: str, *, profiles=PROFILES, regime=None, check=CHECK,
               audit="# AUDIT\n\nNo tokens here.\n") -> pathlib.Path:
    """Write a minimal repository shaped like havel and return its root."""
    base = pathlib.Path(root)
    (base / "docs" / "checks").mkdir(parents=True)
    (base / "docs" / "regimes").mkdir(parents=True)
    (base / "AUDIT.md").write_text(audit, encoding="utf-8")
    (base / "docs" / "regimes" / "scope-profiles.md").write_text(profiles, encoding="utf-8")
    if regime is None:
        today = datetime.date.today().isoformat()
        regime = REGIME.format(date=today)
    (base / "docs" / "regimes" / "gdpr.md").write_text(regime, encoding="utf-8")
    if check is not None:
        (base / "docs" / "checks" / "2.1.md").write_text(check, encoding="utf-8")
    return base


class ExpandScopeTest(unittest.TestCase):
    """Profile expansion resolves to known slugs."""

    def setUp(self):
        self.temp = RetryingTemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = build_tree(self.temp.name)
        self.profiles = checker.load_profiles(self.root)

    def test_named_profile_expands(self):
        self.assertEqual(checker.expand_scope("eu", self.profiles), {"gdpr"})

    def test_all_expands_to_every_slug(self):
        self.assertEqual(checker.expand_scope("all", self.profiles), {"gdpr"})

    def test_baseline_expands_to_nothing(self):
        self.assertEqual(checker.expand_scope("baseline", self.profiles), set())

    def test_undeclared_expands_to_nothing(self):
        self.assertEqual(checker.expand_scope("undeclared", self.profiles), set())

    def test_bare_slug_expands_to_itself(self):
        self.assertEqual(checker.expand_scope("gdpr", self.profiles), {"gdpr"})

    def test_mixed_list_expands(self):
        self.assertEqual(checker.expand_scope("eu, gdpr", self.profiles), {"gdpr"})

    def test_unknown_name_raises(self):
        with self.assertRaises(checker.ScopeError):
            checker.expand_scope("atlantis", self.profiles)


class PassingTreeTest(unittest.TestCase):
    """A well-formed tree exits 0."""

    def test_clean_tree_passes(self):
        with RetryingTemporaryDirectory() as temp:
            root = build_tree(temp)
            self.assertEqual(checker.main([str(root)]), 0)


class ReferenceGraphFailureTest(unittest.TestCase):
    """Every graph defect exits 1."""

    def _run(self, **kwargs) -> int:
        temp = RetryingTemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = build_tree(temp.name, **kwargs)
        return checker.main([str(root)])

    def test_token_with_no_definition_fails(self):
        check = CHECK.replace("[2.1@gdpr]", "[2.7@gdpr]")
        self.assertEqual(self._run(check=check), 1)

    def test_anchor_with_no_reference_fails(self):
        self.assertEqual(self._run(check=None), 1)

    def test_unknown_slug_in_reference_fails(self):
        check = CHECK.replace("[2.1@gdpr]", "[2.1@atlantis]")
        self.assertEqual(self._run(check=check), 1)

    def test_unknown_class_number_fails(self):
        check = CHECK.replace("[2.1@gdpr]", "[2.99@gdpr]")
        self.assertEqual(self._run(check=check), 1)

    def test_anchor_inside_a_check_file_fails(self):
        check = CHECK + "\n### [2.1@gdpr]\nWrong file.\n"
        self.assertEqual(self._run(check=check), 1)


class RegimeHeaderFailureTest(unittest.TestCase):
    """A malformed regime header exits 1."""

    def _run(self, regime: str) -> int:
        temp = RetryingTemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = build_tree(temp.name, regime=regime)
        return checker.main([str(root)])

    def _regime(self, date: str) -> str:
        return REGIME.format(date=date)

    def test_missing_review_date_fails(self):
        regime = self._regime(datetime.date.today().isoformat())
        regime = "\n".join(
            line for line in regime.splitlines() if not line.startswith("Last reviewed:"))
        self.assertEqual(self._run(regime + "\n"), 1)

    def test_malformed_review_date_fails(self):
        self.assertEqual(self._run(self._regime("not-a-date")), 1)

    def test_future_review_date_fails(self):
        future = datetime.date.today() + datetime.timedelta(days=30)
        self.assertEqual(self._run(self._regime(future.isoformat())), 1)

    def test_missing_sources_fails(self):
        regime = self._regime(datetime.date.today().isoformat())
        regime = regime.replace("Sources: https://example.invalid/gdpr\n", "")
        self.assertEqual(self._run(regime), 1)

    def test_empty_sources_fails(self):
        regime = self._regime(datetime.date.today().isoformat())
        regime = regime.replace("Sources: https://example.invalid/gdpr", "Sources:")
        self.assertEqual(self._run(regime), 1)

    def test_missing_disclaimer_fails(self):
        regime = self._regime(datetime.date.today().isoformat())
        regime = regime.replace("Not legal advice. An engineering checklist distilled from public text.\n", "")
        self.assertEqual(self._run(regime), 1)


class StalenessTest(unittest.TestCase):
    """A stale review date warns and exits 0."""

    def test_stale_date_warns_without_failing(self):
        stale = datetime.date.today() - datetime.timedelta(
            days=checker.STALENESS_THRESHOLD_DAYS + 1)
        with RetryingTemporaryDirectory() as temp:
            root = build_tree(temp, regime=REGIME.format(date=stale.isoformat()))
            self.assertEqual(checker.main([str(root)]), 0)


class ProfileFailureTest(unittest.TestCase):
    """A profile table defect exits 1."""

    def _run(self, profiles: str) -> int:
        temp = RetryingTemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = build_tree(temp.name, profiles=profiles)
        return checker.main([str(root)])

    def test_profile_expanding_to_unknown_slug_fails(self):
        profiles = PROFILES.replace("| `eu` | `gdpr` |", "| `eu` | `atlantis` |")
        self.assertEqual(self._run(profiles), 1)

    def test_slug_absent_from_every_profile_fails(self):
        profiles = PROFILES.replace(
            "| `gdpr` | General Data Protection Regulation |",
            "| `gdpr` | General Data Protection Regulation |\n| `orphan` | Orphan Regime |")
        self.assertEqual(self._run(profiles), 1)

    def test_slug_without_a_regime_file_fails(self):
        profiles = PROFILES.replace("| `eu` | `gdpr` |", "| `eu` | `gdpr`, `ghost` |")
        profiles = profiles.replace(
            "| `gdpr` | General Data Protection Regulation |",
            "| `gdpr` | General Data Protection Regulation |\n| `ghost` | Ghost Regime |")
        self.assertEqual(self._run(profiles), 1)


class MatrixTest(unittest.TestCase):
    """The generated matrix reflects the anchors."""

    def test_write_matrix_creates_readme(self):
        with RetryingTemporaryDirectory() as temp:
            root = build_tree(temp)
            self.assertEqual(checker.main([str(root), "--write-matrix"]), 0)
            matrix = (root / "docs" / "regimes" / "README.md").read_text(encoding="utf-8")
            self.assertIn("gdpr", matrix)
            self.assertIn("2.1", matrix)


if __name__ == "__main__":
    unittest.main()
