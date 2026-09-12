#!/usr/bin/env python3
"""Structural invariants for AUDIT.md.

Guard the contract the harness, the bundles, and the checkers rely on.
Anti-duplication tests catch a class reusing a surface an existing class owns.
"""
import difflib
import importlib.util
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AUDIT_PATH = REPO_ROOT / "AUDIT.md"
RUN_EVAL_PATH = REPO_ROOT / "eval" / "run_eval.py"
AUDIT_CHAR_CEILING = 32768
EXPECTED_SECTIONS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
EXPECTED_BLOCKER_COUNT = 10
OVERLAP_THRESHOLD = 0.8
EXPECTED_MODES = {"PR", "File", "Piece", "Wholesale", "Data-map"}
DISCLAIMER_LINE = "NOT LEGAL ADVICE: engineering findings from a static review."

SURFACE_KEYS = {
    "2.1": "basis", "2.2": "notice", "2.3": "purpose", "2.4": "minimization",
    "2.5": "sensitive", "2.6": "children", "2.7": "retention", "2.8": "rights",
    "2.9": "optout", "2.10": "gpc", "2.11": "cmp", "2.12": "processor",
    "2.13": "transfer", "2.14": "tracking", "2.15": "telemetry",
    "2.16": "logging", "2.17": "model", "2.18": "adm", "2.19": "deid",
    "2.20": "secproc", "2.21": "breach", "2.22": "ropa", "2.23": "vendor",
    "2.24": "retaliation", "2.25": "proofing", "2.26": "marketing",
    "2.27": "inventory", "2.28": "copies", "2.29": "accuracy",
}


def _load_run_eval():
    """Import the harness by path."""
    spec = importlib.util.spec_from_file_location("run_eval", RUN_EVAL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_eval = _load_run_eval()
AUDIT_TEXT = AUDIT_PATH.read_text(encoding="utf-8")


def section(number: str) -> str:
    """Return the body of one level-two section."""
    start = AUDIT_TEXT.index(f"## {number}.")
    remainder = AUDIT_TEXT[start + 1:]
    end = remainder.find("\n## ")
    return remainder if end == -1 else remainder[:end]


class AuditPresenceTest(unittest.TestCase):
    """AUDIT.md exists at the repository root."""

    def test_audit_md_exists(self):
        self.assertTrue(AUDIT_PATH.is_file())


class SectionOrderTest(unittest.TestCase):
    """Sections 0 through 9 appear exactly once, in order."""

    def test_sections_are_sorted_and_complete(self):
        found = [int(number) for number in re.findall(r"^## (\d+)\.", AUDIT_TEXT, re.MULTILINE)]
        self.assertEqual(found, sorted(found))
        self.assertEqual(found, EXPECTED_SECTIONS)

    def test_regime_section_does_not_disturb_numbering(self):
        self.assertIn("## 2A.", AUDIT_TEXT)
        self.assertEqual(re.findall(r"^## (\d+)\.", "## 2A. Heading", re.MULTILINE), [])


class SizeCeilingTest(unittest.TestCase):
    """The prompt stays under its character ceiling."""

    def test_audit_md_under_ceiling(self):
        self.assertLessEqual(len(AUDIT_TEXT), AUDIT_CHAR_CEILING)


class VerdictJsonExampleTest(unittest.TestCase):
    """The section 6 VERDICT_JSON example stays parseable and complete."""

    def _extract_block(self) -> str:
        match = re.search(r"VERDICT_JSON:\s*(\{[^`]+\})", AUDIT_TEXT)
        self.assertIsNotNone(match)
        return match.group(1)

    def test_example_block_parses(self):
        json.loads(self._extract_block())

    def test_example_block_has_required_keys(self):
        parsed = json.loads(self._extract_block())
        for key in ("mode", "regimes", "regime_source", "verdict", "findings"):
            with self.subTest(key=key):
                self.assertIn(key, parsed)


class SectionSixTokensTest(unittest.TestCase):
    """Every verdict token named in section 6 is one the pattern accepts."""

    def test_section_six_tokens_match_verdict_pattern(self):
        body = section("6")
        for token in ("VERDICT", "RISK", "RISK (partial)", "ACCURACY"):
            with self.subTest(token=token):
                self.assertIn(token, body)
                self.assertIsNotNone(
                    run_eval.VERDICT_LINE_RE.search(f"{token}: synthetic test line"))


class BlockerCountTest(unittest.TestCase):
    """Section 5 carries exactly the declared blocker count."""

    def test_section_five_bullet_count(self):
        bullets = [line for line in section("5").splitlines() if line.startswith("- ")]
        self.assertEqual(len(bullets), EXPECTED_BLOCKER_COUNT)


class ModeTableTest(unittest.TestCase):
    """Section 0 names exactly the modes the harness accepts."""

    def test_section_zero_names_every_mode(self):
        body = section("0")
        for mode in EXPECTED_MODES:
            with self.subTest(mode=mode):
                self.assertIn(mode, body)

    def test_harness_modes_match(self):
        self.assertEqual(run_eval.VALID_MODES, EXPECTED_MODES)


class SeverityFloorTest(unittest.TestCase):
    """Section 1 forbids a regime delta lowering a baseline severity."""

    def test_floor_rule_present(self):
        self.assertIn("never lower it below baseline", section("1"))


class BlockerThresholdTest(unittest.TestCase):
    """Section 6 keeps the foucault blocking threshold."""

    def test_pr_bullet_blocks_on_critical_or_high(self):
        self.assertIn("CRITICAL or HIGH", section("6"))


class RegimeScopeTest(unittest.TestCase):
    """Step 0b names all three branches and section 2A stays advisory."""

    def test_precedence_branches_present(self):
        body = section("3")
        for phrase in ("declared scope", "ask one question", "undeclared"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, body)

    def test_never_infers_a_regime(self):
        body = section("3")
        self.assertIn("Never apply an undeclared regime", body)

    def test_signals_shape_the_question_only(self):
        start = AUDIT_TEXT.index("## 2A.")
        body = AUDIT_TEXT[start:AUDIT_TEXT.index("## 3.")]
        self.assertIn("Signals shape the question alone", body)
        self.assertIn("raises no finding", body)


class DisclaimerTest(unittest.TestCase):
    """The not-legal-advice requirement appears where deployments cannot drop it."""

    def test_preamble_carries_the_disclaimer(self):
        preamble = AUDIT_TEXT[:AUDIT_TEXT.index("## 0.")]
        self.assertIn("NOT LEGAL ADVICE", preamble)

    def test_section_six_mandates_the_trailing_line(self):
        self.assertIn(DISCLAIMER_LINE, section("6"))
        self.assertIn("in every mode", section("6"))

    def test_section_seven_forbids_asserting_compliance(self):
        self.assertIn("Never assert compliance", section("7"))


class SurfaceKeyTest(unittest.TestCase):
    """A class must not reuse a declared surface an existing class owns."""

    def test_surface_keys_are_unique(self):
        surfaces = list(SURFACE_KEYS.values())
        self.assertEqual(len(surfaces), len(set(surfaces)))

    def test_surface_key_count(self):
        self.assertEqual(len(SURFACE_KEYS), 29)

    def test_every_class_row_present(self):
        for number in SURFACE_KEYS:
            with self.subTest(number=number):
                self.assertIn(f"**{number}**", AUDIT_TEXT)


class BulletOverlapTest(unittest.TestCase):
    """Class rows from different classes must not share most characters."""

    def test_no_row_pair_overlaps(self):
        rows = [line for line in section("2").splitlines() if line.startswith("| **2.")]
        violations = []
        for index, first in enumerate(rows):
            for second in rows[index + 1:]:
                ratio = difflib.SequenceMatcher(None, first.lower(), second.lower()).ratio()
                if ratio > OVERLAP_THRESHOLD:
                    violations.append((first[:40], second[:40], ratio))
        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
