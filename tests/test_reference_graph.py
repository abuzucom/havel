#!/usr/bin/env python3
"""The two-axis reference graph between checks and regimes.

The split is only safe while every reference resolves and every anchor is
cited. These assertions carry that guarantee.
"""
import importlib.util
import re
import unittest
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CHECKS_DIR = REPO_ROOT / "docs" / "checks"
REGIMES_DIR = REPO_ROOT / "docs" / "regimes"
CHECKER_PATH = REPO_ROOT / "scripts" / "check_regime_refs.py"

CHECK_HEADINGS = [
    "Barrier list", "Severity posture", "Thresholds",
    "How to investigate", "Boundaries",
]
REGIME_HEADINGS = [
    "Applicability", "Class deltas", "Terms of art",
    "Thresholds and clocks", "What this regime does not add",
]
FROZEN_SLUGS = {
    "gdpr", "eprivacy", "eidas", "de-national", "uk-gdpr", "pecr", "ccpa",
    "tdpsa", "vcdpa", "cpa", "ctdpa", "ucpa", "pipeda", "lgpd", "law25",
}
EXPECTED_CLASS_COUNT = 29
MAX_DELTA_CHARS = 900
NON_REGIME_FILES = {"scope-profiles.md", "README.md"}


def _load_checker():
    """Import the checker by path."""
    spec = importlib.util.spec_from_file_location("check_regime_refs", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = _load_checker()
PROFILES = checker.load_profiles(REPO_ROOT)


def regime_files():
    """Return every regime file."""
    return sorted(p for p in REGIMES_DIR.glob("*.md") if p.name not in NON_REGIME_FILES)


def headings(text: str) -> list:
    """Return the level-two headings of one document in order."""
    return re.findall(r"^## (.+)$", text, re.MULTILINE)


class CheckFileTest(unittest.TestCase):
    """One check file per class, each carrying the template."""

    def test_class_count(self):
        self.assertEqual(len(list(CHECKS_DIR.glob("2.*.md"))), EXPECTED_CLASS_COUNT)

    def test_titles_match_filenames(self):
        for path in CHECKS_DIR.glob("2.*.md"):
            with self.subTest(path=path.name):
                first = path.read_text(encoding="utf-8").splitlines()[0]
                self.assertTrue(first.startswith(f"# {path.stem} "), first)

    def test_headings_present_in_order(self):
        for path in CHECKS_DIR.glob("2.*.md"):
            with self.subTest(path=path.name):
                self.assertEqual(headings(path.read_text(encoding="utf-8")),
                                 CHECK_HEADINGS)

    def test_no_definition_site_in_a_check_file(self):
        for path in CHECKS_DIR.glob("2.*.md"):
            with self.subTest(path=path.name):
                self.assertNotRegex(path.read_text(encoding="utf-8"),
                                    r"^### \[2\.\d+@")


class RegimeFileTest(unittest.TestCase):
    """One regime file per frozen slug, each carrying the template."""

    def test_slug_set_frozen(self):
        self.assertEqual({p.stem for p in regime_files()}, FROZEN_SLUGS)
        self.assertEqual(PROFILES["slugs"], FROZEN_SLUGS)

    def test_headings_present_in_order(self):
        for path in regime_files():
            with self.subTest(path=path.name):
                self.assertEqual(headings(path.read_text(encoding="utf-8")),
                                 REGIME_HEADINGS)

    def test_title_names_the_slug(self):
        for path in regime_files():
            with self.subTest(path=path.name):
                first = path.read_text(encoding="utf-8").splitlines()[0]
                self.assertTrue(first.endswith(f"({path.stem})"), first)


class ReferenceGraphTest(unittest.TestCase):
    """Every reference resolves and every anchor is cited."""

    def setUp(self):
        self.references = checker.collect_references(REPO_ROOT)
        self.anchors = checker.collect_anchors(REPO_ROOT)

    def test_every_reference_has_an_anchor(self):
        self.assertEqual(sorted(set(self.references) - set(self.anchors)), [])

    def test_every_anchor_is_referenced(self):
        self.assertEqual(sorted(set(self.anchors) - set(self.references)), [])

    def test_every_token_names_a_known_class_and_slug(self):
        known = {path.stem for path in CHECKS_DIR.glob("2.*.md")}
        for number, slug in sorted(self.references):
            with self.subTest(token=f"{number}@{slug}"):
                self.assertIn(number, known)
                self.assertIn(slug, FROZEN_SLUGS)

    def test_each_anchor_has_one_definition_site(self):
        for token, files in sorted(self.anchors.items()):
            with self.subTest(token=token):
                self.assertEqual(len(set(files)), 1)

    def test_checker_passes_on_the_real_tree(self):
        self.assertEqual(checker.main([str(REPO_ROOT)]), 0)


class RegimeCurrencyTest(unittest.TestCase):
    """Every regime file carries a usable header."""

    def test_review_date_parses_and_is_not_future(self):
        for path in regime_files():
            with self.subTest(path=path.name):
                match = checker.REVIEWED_PATTERN.search(path.read_text(encoding="utf-8"))
                self.assertIsNotNone(match)
                self.assertLessEqual(date.fromisoformat(match.group(1)), date.today())

    def test_sources_line_is_non_empty(self):
        for path in regime_files():
            with self.subTest(path=path.name):
                match = checker.SOURCES_PATTERN.search(path.read_text(encoding="utf-8"))
                self.assertIsNotNone(match)
                self.assertTrue(match.group(1).strip())

    def test_disclaimer_present(self):
        for path in regime_files():
            with self.subTest(path=path.name):
                self.assertIn(checker.DISCLAIMER, path.read_text(encoding="utf-8"))


class ScopeProfileTest(unittest.TestCase):
    """The profile table reaches every slug and expands only to known ones."""

    def test_profiles_expand_to_known_slugs(self):
        for name, expansion in PROFILES["profiles"].items():
            with self.subTest(profile=name):
                self.assertEqual(sorted(expansion - FROZEN_SLUGS), [])

    def test_every_slug_reachable_from_a_profile(self):
        reachable = set()
        for expansion in PROFILES["profiles"].values():
            reachable |= expansion
        self.assertEqual(sorted(FROZEN_SLUGS - reachable), [])

    def test_all_expands_to_the_frozen_set(self):
        self.assertEqual(PROFILES["profiles"]["all"], FROZEN_SLUGS)

    def test_audit_section_2a_names_every_profile_it_cites(self):
        text = (REPO_ROOT / "AUDIT.md").read_text(encoding="utf-8")
        body = text[text.index("## 2A."):text.index("## 3.")]
        for name in re.findall(r"`([a-z-]+)`", body):
            if name in PROFILES["profiles"] or name in FROZEN_SLUGS:
                continue
            if name.startswith("us-") or name in {"eea", "germany", "canada-qc"}:
                continue
            self.assertIn(name, PROFILES["profiles"], f"unknown profile {name}")


class NoDeltaDuplicationTest(unittest.TestCase):
    """A regime delta must not grow into a check file."""

    def _deltas(self):
        pattern = re.compile(r"^### \[(2\.\d+)@([a-z0-9-]+)\]\s*$", re.MULTILINE)
        for path in regime_files():
            parts = pattern.split(path.read_text(encoding="utf-8"))
            for index in range(1, len(parts), 3):
                body = parts[index + 2]
                for terminator in ("\n## ", "\n### "):
                    cut = body.find(terminator)
                    if cut != -1:
                        body = body[:cut]
                yield path.name, parts[index], parts[index + 1], body

    def test_delta_length_bounded(self):
        for name, number, slug, body in self._deltas():
            with self.subTest(token=f"{number}@{slug}"):
                self.assertLessEqual(len(body.strip()), MAX_DELTA_CHARS, name)

    def test_delta_carries_no_barrier_list(self):
        for name, number, slug, body in self._deltas():
            with self.subTest(token=f"{number}@{slug}"):
                self.assertNotIn("Barrier list", body)

    def test_delta_carries_no_numbered_investigation(self):
        for name, number, slug, body in self._deltas():
            with self.subTest(token=f"{number}@{slug}"):
                self.assertNotRegex(body, re.compile(r"^\d+\. ", re.MULTILINE))

    def test_every_delta_states_a_severity_shift(self):
        for name, number, slug, body in self._deltas():
            with self.subTest(token=f"{number}@{slug}"):
                self.assertRegex(body, re.compile(r"^Severity shift:[^\S\n]*\S", re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
