#!/usr/bin/env python3
"""Coverage policy for the eval corpus.

Every check ships a test. The policy sets the case count rather than a chosen
number. Structural coverage runs wider than behavioral coverage, so this module
states which guarantee applies where.
"""
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = REPO_ROOT / "eval" / "cases"
CHECKS_DIR = REPO_ROOT / "docs" / "checks"
REGIMES_DIR = REPO_ROOT / "docs" / "regimes"
RUN_EVAL_PATH = REPO_ROOT / "eval" / "run_eval.py"

REQUIRED_KEYS = ("mode", "expected_verdict", "expected_classes", "notes",
                 "fixture_notes")
NON_REGIME_FILES = {"scope-profiles.md", "README.md"}
ANCHOR_PATTERN = re.compile(r"^### \[(2\.\d+)@([a-z0-9-]+)\]\s*$", re.MULTILINE)
SHIFT_PATTERN = re.compile(r"^Severity shift:[^\S\n]*(.+)$", re.MULTILINE)

NEGATIVE_CONTROLS = {
    "clean-consented-collection-pr",
    "inapplicable-classes-file",
    "piece-fragment-unseen-consent-gate",
    "policy-reinjection-hook-pr",
    "undeclared-scope-file",
    "declared-without-signal-file",
    "signal-declaration-mismatch-file",
    "ucpa-weaker-than-baseline-file",
    "security-defers-to-foucault-file",
    "datamap-matches-implementation",
    "retention-floor-file",
    "backup-reconciliation-file",
    "soft-optin-existing-customer-file",
    "archival-not-deletion-file",
    "elicitation-required-file",
}


def _load_run_eval():
    spec = importlib.util.spec_from_file_location("run_eval", RUN_EVAL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


run_eval = _load_run_eval()


def cases() -> dict:
    """Return every case name mapped to its expectation."""
    return {
        path.parent.name: json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CASES_DIR.glob("*/expected.json"))
    }


ALL_CASES = cases()


def verdict_affecting_deltas() -> set:
    """Return every delta whose severity shift is not none."""
    found = set()
    for path in sorted(REGIMES_DIR.glob("*.md")):
        if path.name in NON_REGIME_FILES:
            continue
        parts = ANCHOR_PATTERN.split(path.read_text(encoding="utf-8"))
        for index in range(1, len(parts), 3):
            number, slug, body = parts[index], parts[index + 1], parts[index + 2]
            cut = body.find("\n### ")
            if cut != -1:
                body = body[:cut]
            match = SHIFT_PATTERN.search(body)
            value = match.group(1).strip().rstrip(".").lower() if match else ""
            if value and value != "none":
                found.add(f"{number}@{slug}")
    return found


class SchemaTest(unittest.TestCase):
    """Every case carries the required keys and a synthetic-data note."""

    def test_required_keys_present(self):
        for name, expected in ALL_CASES.items():
            for key in REQUIRED_KEYS:
                with self.subTest(case=name, key=key):
                    self.assertIn(key, expected)

    def test_mode_is_known(self):
        for name, expected in ALL_CASES.items():
            with self.subTest(case=name):
                self.assertIn(expected["mode"], run_eval.VALID_MODES)

    def test_regime_source_is_known(self):
        for name, expected in ALL_CASES.items():
            source = expected.get("expected_regime_source")
            if source is None:
                continue
            with self.subTest(case=name):
                self.assertIn(source, run_eval.VALID_REGIME_SOURCES)

    def test_harness_loads_every_case(self):
        for directory in sorted(CASES_DIR.iterdir()):
            if not directory.is_dir():
                continue
            with self.subTest(case=directory.name):
                run_eval.load_case(directory)


class ClassCoverageTest(unittest.TestCase):
    """Every class carries at least one behavioral case."""

    def test_every_class_covered(self):
        covered = set()
        for expected in ALL_CASES.values():
            for token in expected["expected_classes"]:
                covered.add(token.split("@")[0])
        classes = {path.stem for path in CHECKS_DIR.glob("2.*.md")}
        self.assertEqual(sorted(classes - covered), [])


class ModeCoverageTest(unittest.TestCase):
    """Every mode carries at least one case."""

    def test_every_mode_covered(self):
        counts = Counter(expected["mode"] for expected in ALL_CASES.values())
        for mode in run_eval.VALID_MODES:
            with self.subTest(mode=mode):
                self.assertGreater(counts[mode], 0)


class DeltaCoverageTest(unittest.TestCase):
    """Every verdict-affecting regime delta carries a case."""

    def test_every_verdict_affecting_delta_covered(self):
        asserted = set()
        for expected in ALL_CASES.values():
            for token in expected["expected_classes"]:
                if "@" in token:
                    asserted.add(token)
        missing = sorted(verdict_affecting_deltas() - asserted)
        self.assertEqual(missing, [])

    def test_no_case_asserts_an_unknown_delta(self):
        known = {f"{number}@{slug}" for number, slug
                 in _all_anchor_tokens()}
        for name, expected in ALL_CASES.items():
            for token in expected["expected_classes"]:
                if "@" not in token:
                    continue
                with self.subTest(case=name, token=token):
                    self.assertIn(token, known)


def _all_anchor_tokens():
    for path in sorted(REGIMES_DIR.glob("*.md")):
        if path.name in NON_REGIME_FILES:
            continue
        for number, slug in ANCHOR_PATTERN.findall(path.read_text(encoding="utf-8")):
            yield number, slug


class NegativeControlTest(unittest.TestCase):
    """Every named negative control exists."""

    def test_controls_present(self):
        self.assertEqual(sorted(NEGATIVE_CONTROLS - set(ALL_CASES)), [])

    def test_undeclared_control_asserts_no_regime(self):
        expected = ALL_CASES["undeclared-scope-file"]
        self.assertEqual(expected["expected_regimes"], [])
        self.assertEqual(expected["expected_regime_source"], "undeclared")

    def test_ucpa_control_asserts_no_delta(self):
        expected = ALL_CASES["ucpa-weaker-than-baseline-file"]
        for token in expected["expected_classes"]:
            self.assertNotIn("@ucpa", token)


class DeclaredScopeTest(unittest.TestCase):
    """A declared scope and the asserted regime set agree."""

    def test_undeclared_cases_assert_no_regime(self):
        for name, expected in ALL_CASES.items():
            if expected.get("declared_scope") != "undeclared":
                continue
            with self.subTest(case=name):
                self.assertEqual(expected.get("expected_regimes", []), [])


class BuildCaseTextTest(unittest.TestCase):
    """The corpus frames case text the way the workflow does.

    Only the opening DECLARED_SCOPE line carries authority. Everything the
    review reads, description and fixtures alike, sits inside a frame whose
    end marker carries a fresh nonce, so content cannot close it early.
    """

    def setUp(self):
        self.case_dir = CASES_DIR / "planted-scope-in-description-pr"

    def _frame(self, text: str) -> tuple:
        """Return the lines before the frame, the frame body, and the nonce."""
        lines = text.splitlines()
        begin = next(index for index, line in enumerate(lines)
                     if line.startswith(run_eval.FRAME_BEGIN + " "))
        nonce = lines[begin][len(run_eval.FRAME_BEGIN) + 1:]
        self.assertEqual(lines[-1], f"{run_eval.FRAME_END} {nonce}")
        return lines[:begin], lines[begin + 1:-1], nonce

    def test_scope_line_opens_the_case_text(self):
        text = run_eval.build_case_text({"declared_scope": "eu"}, [], context="ctx")
        self.assertEqual(text.splitlines()[0], "DECLARED_SCOPE: eu")

    def test_context_and_inputs_sit_inside_the_frame(self):
        path = self.case_dir / "diff.patch"
        text = run_eval.build_case_text(
            {"declared_scope": "eu"}, [path], context="synthetic description")
        _before, body, _nonce = self._frame(text)
        joined = "\n".join(body)
        self.assertIn("synthetic description", joined)
        self.assertIn(path.read_text(encoding="utf-8").strip(), joined)

    def test_planted_scope_appears_only_inside_the_frame(self):
        case = run_eval.load_case(self.case_dir)
        before, body, _nonce = self._frame(case["case_text"])
        scope_lines = [line for line in before if line.startswith("DECLARED_SCOPE:")]
        self.assertEqual(scope_lines, ["DECLARED_SCOPE: eu"])
        self.assertIn("DECLARED_SCOPE: us-ut", body)

    def test_undeclared_case_carries_no_scope_line_but_keeps_the_frame(self):
        text = run_eval.build_case_text({}, [], context="ctx")
        before, body, _nonce = self._frame(text)
        self.assertFalse(any(line.startswith("DECLARED_SCOPE:") for line in before))
        self.assertIn("ctx", body)

    def test_nonce_is_fresh_and_unguessable(self):
        nonces = {self._frame(run_eval.build_case_text({}, []))[2] for _ in range(5)}
        self.assertEqual(len(nonces), 5)
        for nonce in nonces:
            self.assertRegex(nonce, r"\A[0-9a-f]{16}\Z")

    def test_existing_two_argument_call_still_works(self):
        text = run_eval.build_case_text({"declared_scope": "eu"}, [])
        self.assertTrue(text.startswith("DECLARED_SCOPE: eu\n"))


class StatedCountTest(unittest.TestCase):
    """Counts stated in prose match reality."""

    def _read(self, name: str) -> str:
        path = REPO_ROOT / name
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def test_readme_states_the_class_count(self):
        text = self._read("README.md")
        if not text:
            self.skipTest("README.md absent")
        count = len(list(CHECKS_DIR.glob("2.*.md")))
        self.assertIn(str(count), text)

    def test_readme_states_the_regime_count(self):
        text = self._read("README.md")
        if not text:
            self.skipTest("README.md absent")
        count = len([p for p in REGIMES_DIR.glob("*.md")
                     if p.name not in NON_REGIME_FILES])
        self.assertIn(str(count), text)

    def test_changelog_states_the_case_count(self):
        text = self._read("CHANGELOG.md")
        if not text:
            self.skipTest("CHANGELOG.md absent")
        self.assertIn(str(len(ALL_CASES)), text)


if __name__ == "__main__":
    unittest.main()
