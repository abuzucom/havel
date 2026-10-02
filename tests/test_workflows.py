#!/usr/bin/env python3
"""Workflow integrity tests.

Text-level assertions on .github/workflows/ci.yml and privacy-review.yml. No
YAML parser is available. Each assertion targets one regression the prose
rules call out: unpinned actions, inherited secrets, missing scripts, and
direct interpolation of pull request content into shell commands.
"""
import os
import re
import shutil
import subprocess
import tempfile
import textwrap
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
STEP_SPLIT = "\n      - "
GIT_IDENTITY = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid"]


def review_step(name: str) -> str:
    """Return the text of one privacy-review.yml step, header included."""
    text = REVIEW_PATH.read_text(encoding="utf-8")
    start = text.index(f"- name: {name}\n")
    end = text.find(STEP_SPLIT, start)
    return text[start:] if end == -1 else text[start:end]


def step_script(name: str) -> str:
    """Return the dedented shell body of one privacy-review.yml run step."""
    step = review_step(name)
    body = step.split("run: |\n", 1)[1]
    return textwrap.dedent(body)


def run_step(name: str, cwd: Path, environment: dict) -> subprocess.CompletedProcess:
    """Run one step body the way the runner does: bash with errexit and pipefail."""
    return subprocess.run(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", step_script(name)],
        cwd=cwd, env={**os.environ, **environment},
        capture_output=True, text=True, check=False,
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

    def test_review_is_not_a_sibling_workflow(self):
        """CONFORMANCE is adorno's design token. Havel audits privacy.

        This once also asserted ACCURACY appears in the workflow, which held
        while the gate grepped every mode's token. The gate now reads
        VERDICT alone, so the only remaining occurrence is the comment
        explaining that, and the assertion passed for the wrong reason.
        VerdictGateTest.test_gate_reads_the_pr_mode_token_alone carries the
        real contract, scoped to the grep line. Only the sibling guard
        survives here.
        """
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

    def _step(self) -> str:
        """Return the Parse verdict step body."""
        step = self.review.split("name: Parse verdict", 1)[1]
        return step.split("name: Post PR comment", 1)[0]

    def _executable_lines(self) -> list:
        """Return the step's lines that run, excluding comments."""
        return [
            line for line in self._step().splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]

    def test_gate_blocks_on_needs_human(self):
        """An escalation is not a pass.

        AUDIT.md section 1 escalates to NEEDS-HUMAN where the audit cannot
        establish lawfulness. Treating that as unblocked merges the exact
        change the audit declined to clear.

        Read the executable lines rather than the whole step. The comment
        above the case statement names NEEDS-HUMAN, so an assertion over the
        step text stays green after a revert to a BLOCK-only gate.
        """
        executable = self._executable_lines()
        self.assertTrue(any("NEEDS-HUMAN" in line for line in executable))

    def test_gate_reads_the_verdict_token_alone(self):
        """The reason must not decide the gate.

        Searching the whole line fails closed on
        'VERDICT: APPROVE - resolved earlier BLOCK findings' and fails open
        on 'VERDICT: REJECT', which matches no alternative and merges.
        """
        executable = "\n".join(self._executable_lines())
        self.assertIn("case ", executable)
        self.assertIn("APPROVE)", executable)
        self.assertNotIn("grep -qE 'BLOCK|NEEDS-HUMAN'", executable)

    def test_unrecognized_token_fails_the_step(self):
        """A malformed verdict is not a verdict.

        fail_on_block governs which verdicts block, not whether output
        carrying no valid verdict counts as a pass.
        """
        executable = "\n".join(self._executable_lines())
        self.assertIn("Unrecognized verdict token", executable)
        self.assertIn("exit 1", executable)

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


class PullRequestIsolationTest(unittest.TestCase):
    """Pull request content stays data. It never runs and never receives a write.

    The pull request controls every file in its checkout, symlinks included.
    A write into that tree follows a planted link. A command resolved inside
    it runs code the author chose.
    """

    def setUp(self):
        self.review = REVIEW_PATH.read_text(encoding="utf-8")

    def test_pull_request_checks_out_into_its_own_directory(self):
        self.assertIn("path: pr\n", review_step("Checkout pull request"))

    def test_model_call_runs_from_the_base_commit(self):
        base = review_step("Checkout base commit")
        self.assertIn("repository: ${{ github.repository }}", base)
        self.assertIn("ref: ${{ github.event.pull_request.base.sha }}", base)
        self.assertIn("path: base\n", base)
        self.assertIn("working-directory: base\n", review_step("Run model call"))

    def test_every_checkout_drops_its_credential(self):
        checkouts = self.review.count("uses: actions/checkout@")
        self.assertEqual(checkouts, 3)
        self.assertEqual(self.review.count("persist-credentials: false"), checkouts)

    def test_scratch_files_live_in_runner_temp(self):
        for name in ("Build case text", "Run model call", "Parse verdict",
                     "Post PR comment"):
            step = review_step(name)
            with self.subTest(step=name):
                self.assertNotRegex(step, r"(?<![\w/])(case_text|response)\.txt")
        for variable in ("CASE_TEXT_FILE", "RESPONSE_FILE"):
            with self.subTest(variable=variable):
                values = re.findall(rf"^\s+{variable}: (.+)$", self.review, re.MULTILINE)
                self.assertTrue(values)
                for value in values:
                    self.assertTrue(value.startswith("${{ runner.temp }}/"), value)

    def test_prompt_path_is_absolute(self):
        self.assertIn("AUDIT_PROMPT_FILE: ${{ github.workspace }}/.havel/AUDIT.md",
                      review_step("Run model call"))


class ModelSecretTest(unittest.TestCase):
    """The documented credential reaches the model call and nothing else."""

    def setUp(self):
        self.review = REVIEW_PATH.read_text(encoding="utf-8")

    def _halves(self) -> list:
        """Split at the top-level jobs key. The header comment also says jobs:."""
        halves = self.review.split("\njobs:\n", 1)
        self.assertEqual(len(halves), 2)
        return halves

    def test_secret_is_declared_on_the_call(self):
        trigger = self._halves()[0].split("\non:\n", 1)[1]
        secrets = trigger.split("    secrets:\n", 1)
        self.assertEqual(len(secrets), 2, "workflow_call declares no secrets block")
        self.assertIn("MODEL_API_KEY:", secrets[1])
        self.assertIn("required: false", secrets[1])

    def test_secret_maps_into_the_model_step_alone(self):
        mapping = "MODEL_API_KEY: ${{ secrets.MODEL_API_KEY }}"
        self.assertIn(mapping, review_step("Run model call"))
        self.assertEqual(self._halves()[1].count("secrets.MODEL_API_KEY"), 1)


class ForkPullRequestTest(unittest.TestCase):
    """A fork pull request carries a read-only token, so no comment is attempted."""

    def test_comment_step_skips_forks(self):
        step = review_step("Post PR comment")
        self.assertIn(
            "github.event.pull_request.head.repo.full_name == github.repository", step)


class BuildCaseTextBehaviorTest(unittest.TestCase):
    """The Build case text step, run for real against a hostile checkout."""

    def setUp(self):
        if shutil.which("bash") is None or shutil.which("git") is None:
            self.skipTest("bash and git are required to run a workflow step")
        self._directory = tempfile.TemporaryDirectory()
        self.workspace = Path(self._directory.name) / "workspace"
        self.runner_temp = Path(self._directory.name) / "runner-temp"
        self.workspace.mkdir()
        self.runner_temp.mkdir()
        # The sentinel stands in for .havel/AUDIT.md: a trusted file outside
        # the pull request that a planted link points at.
        self.sentinel = Path(self._directory.name) / "sentinel.txt"
        self.sentinel.write_text("trusted\n", encoding="utf-8")
        self.base_sha, self.head_sha = self._pull_request_repository()

    def tearDown(self):
        self._directory.cleanup()

    def _git(self, *arguments: str) -> str:
        result = subprocess.run(
            ["git", *GIT_IDENTITY, "-C", str(self.workspace), *arguments],
            capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def _pull_request_repository(self) -> tuple:
        """Build a two-commit pull request whose head plants hostile symlinks.

        The workspace root holds the pull request, as a checkout without a
        path does. pr/ holds a clone of it, as a checkout with path: pr does.
        Both layouts carry the planted links, so the test fails whichever
        layout the step writes into.
        """
        self._git("init", "-q")
        (self.workspace / "app.py").write_text("print('base')\n", encoding="utf-8")
        self._git("add", "app.py")
        self._git("commit", "-q", "-m", "base")
        base = self._git("rev-parse", "HEAD")
        (self.workspace / "app.py").write_text("print('head')\n", encoding="utf-8")
        for name in ("case_text.txt", "response.txt"):
            (self.workspace / name).symlink_to(self.sentinel)
        self._git("add", "-A")
        self._git("commit", "-q", "-m", "head")
        head = self._git("rev-parse", "HEAD")
        self._git("clone", "-q", str(self.workspace), str(self.workspace / "pr"))
        return base, head

    def _run(self) -> subprocess.CompletedProcess:
        return run_step("Build case text", self.workspace, {
            "PR_TITLE": "feat: synthetic change",
            "PR_BODY": "Synthetic body.",
            "BASE_SHA": self.base_sha,
            "HEAD_SHA": self.head_sha,
            "DECLARED_REGIMES": "eu",
            "CASE_TEXT_FILE": str(self.runner_temp / "case_text.txt"),
            "RUNNER_TEMP": str(self.runner_temp),
        })

    def test_planted_symlink_never_receives_the_write(self):
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.sentinel.read_text(encoding="utf-8"), "trusted\n")

    def test_case_text_lands_in_runner_temp(self):
        result = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        case_text = (self.runner_temp / "case_text.txt").read_text(encoding="utf-8")
        self.assertTrue(case_text.startswith("DECLARED_SCOPE: eu\n"))
        self.assertIn("+print('head')", case_text)


if __name__ == "__main__":
    unittest.main()
