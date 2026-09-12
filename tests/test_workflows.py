#!/usr/bin/env python3
"""Workflow integrity tests.

Text-level assertions on .github/workflows/ci.yml and privacy-review.yml. No
YAML parser is available. Each assertion targets one regression the prose
rules call out: unpinned actions, inherited secrets, missing scripts, and
direct interpolation of pull request content into shell commands.
"""
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
REVIEW_PATH = REPO_ROOT / ".github" / "workflows" / "privacy-review.yml"
SHA_PIN_RE = re.compile(r"@[0-9a-f]{40}\b")
SCRIPT_REF_RE = re.compile(r"scripts/\w+\.py")
USES_LINE_RE = re.compile(r"^\s+uses:")
SECRETS_INHERIT_RE = re.compile(r"^\s+secrets:\s*inherit\b")

PR_INTERPOLATION_PATTERNS = (
    "${{ github.event.pull_request.title }}",
    "${{ github.event.pull_request.body }}",
)


class UsesPinningTest(unittest.TestCase):
    """Every action reference is pinned to a full commit SHA."""

    def test_every_uses_line_is_sha_pinned(self):
        for path in (CI_PATH, REVIEW_PATH):
            text = path.read_text(encoding="utf-8")
            uses_lines = [
                line for line in text.splitlines() if USES_LINE_RE.match(line)
            ]
            self.assertTrue(uses_lines)
            for line in uses_lines:
                with self.subTest(file=path.name, line=line.strip()):
                    self.assertRegex(line, SHA_PIN_RE)


class SecretsTest(unittest.TestCase):
    """The reusable workflow must not receive every caller secret."""

    def test_no_secrets_inherit(self):
        for path in (CI_PATH, REVIEW_PATH):
            text = path.read_text(encoding="utf-8")
            for line in text.splitlines():
                with self.subTest(file=path.name, line=line.strip()):
                    self.assertIsNone(SECRETS_INHERIT_RE.match(line))


class ScriptReferenceTest(unittest.TestCase):
    """Scripts ci.yml names exist on disk."""

    def test_referenced_scripts_exist(self):
        text = CI_PATH.read_text(encoding="utf-8")
        references = set(SCRIPT_REF_RE.findall(text))
        self.assertTrue(references)
        for reference in references:
            with self.subTest(script=reference):
                self.assertTrue((REPO_ROOT / reference).is_file())

    def test_ci_references_run_eval(self):
        text = CI_PATH.read_text(encoding="utf-8")
        self.assertIn("eval/run_eval.py", text)


class ModelCallContractTest(unittest.TestCase):
    """The model_call_command contract names both environment files."""

    def test_input_description_names_env_files(self):
        text = REVIEW_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"model_call_command:\s*\n\s*description:\s*\"([^\"]+)\"",
            text,
        )
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertIn("AUDIT_PROMPT_FILE", description)
        self.assertIn("CASE_TEXT_FILE", description)


class InterpolationSafetyTest(unittest.TestCase):
    """Pull request title and body reach shell through env vars only.

    Direct interpolation of pull request content into a run block executes
    attacker-controlled text as shell. The workflows assign it to an env
    var and the run block reads the var.
    """

    def _run_blocks(self, text: str) -> list:
        blocks = []
        for match in re.finditer(r"run: \|(.*?)(?=\n      - |\Z)", text, re.DOTALL):
            blocks.append(match.group(1))
        return blocks

    def test_pr_fields_not_interpolated_in_shell(self):
        for path in (CI_PATH, REVIEW_PATH):
            text = path.read_text(encoding="utf-8")
            for block in self._run_blocks(text):
                for pattern in PR_INTERPOLATION_PATTERNS:
                    with self.subTest(file=path.name, pattern=pattern):
                        self.assertNotIn(pattern, block)


class HavelWorkflowTest(unittest.TestCase):
    """Steps havel adds beyond the sibling skeleton."""

    def setUp(self):
        self.ci = CI_PATH.read_text(encoding="utf-8")
        self.review = REVIEW_PATH.read_text(encoding="utf-8")

    def test_ci_runs_the_regime_reference_checker(self):
        self.assertIn("scripts/check_regime_refs.py", self.ci)

    def test_ci_runs_the_bundle_currency_check(self):
        self.assertIn("scripts/build_bundle.py --check", self.ci)

    def test_prose_step_covers_regimes_and_excludes_generated_output(self):
        self.assertIn("docs/regimes/*.md", self.ci)
        self.assertNotIn("bundles/*.md", self.ci)

    def test_review_requires_the_regimes_input(self):
        self.assertIn("regimes:", self.review)
        block = self.review.split("regimes:", 1)[1].split("jobs:", 1)[0]
        self.assertIn("required: true", block)

    def test_review_emits_the_declared_scope_line(self):
        self.assertIn("DECLARED_SCOPE:", self.review)

    def test_review_greps_the_accuracy_token(self):
        self.assertIn("ACCURACY", self.review)
        self.assertNotIn("CONFORMANCE", self.review)

    def test_review_fails_without_the_disclaimer_line(self):
        self.assertIn("NOT LEGAL ADVICE:", self.review)


class VerdictGateTest(unittest.TestCase):
    """The merge gate reads the report's own verdict and holds on doubt."""

    def setUp(self):
        self.review = REVIEW_PATH.read_text(encoding="utf-8")

    def test_gate_reads_the_last_verdict_line(self):
        """A quoted verdict earlier in the report must not win.

        A report quotes the diff under review. Reading the first match lets
        a planted VERDICT: APPROVE line in a pull request body decide the
        gate. Section 6 puts the authoritative verdict last.
        """
        self.assertIn("tail -1", self.review)
        self.assertNotIn("head -1", self.review)

    def test_gate_blocks_on_needs_human(self):
        """An escalation is not a pass.

        AUDIT.md section 1 escalates to NEEDS-HUMAN where the audit cannot
        establish lawfulness. Treating that as unblocked merges the exact
        change the audit declined to clear.
        """
        self.assertIn("NEEDS-HUMAN", self.review)

    def test_gate_reads_the_pr_mode_token_alone(self):
        """The workflow always runs PR mode, so only VERDICT: gates it.

        Accepting RISK: or ACCURACY: lets a report answering in another mode
        satisfy a merge gate that mode never addressed.
        """
        step = self.review.split("name: Parse verdict", 1)[1]
        step = step.split("name: Post PR comment", 1)[0]
        grep_lines = [
            line for line in step.splitlines()
            if "grep" in line and not line.lstrip().startswith("#")
        ]
        self.assertTrue(grep_lines)
        verdict_greps = [line for line in grep_lines if "VERDICT" in line]
        self.assertEqual(len(verdict_greps), 1)
        self.assertIn("'^VERDICT:'", verdict_greps[0])
        self.assertNotIn("RISK", verdict_greps[0])
        self.assertNotIn("ACCURACY", verdict_greps[0])


if __name__ == "__main__":
    unittest.main()
