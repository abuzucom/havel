#!/usr/bin/env python3
"""Prose file coverage completeness.

The ci.yml prose step lists the governance prose the style checkers gate.
A tracked .md file missing from that list ships unchecked. Compare the
tracked set against the prose step.

Exempt by design: eval/cases/ files are fixture data. docs/checks/ files
are technical checklists that share the label-colon structure of the
AUDIT.md schema sections. Both are data, not governance prose.
"""
import re
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CI_PATH = REPO_ROOT / ".github" / "workflows" / "ci.yml"
EXEMPT_PREFIXES = ("eval/cases/", "docs/checks/", "bundles/")


def tracked_markdown() -> list:
    """Return every tracked .md file as a POSIX relative path."""
    result = subprocess.run(
        ["git", "ls-files", "--", "*.md"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def prose_step_body(ci_text: str) -> str:
    """Extract the block under the 'name: Prose style' step."""
    match = re.search(
        r"name: Prose style(.*?)(?=\n  \w|\Z)",
        ci_text,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("ci.yml has no 'name: Prose style' step")
    return match.group(1)


class ProseCoverageTest(unittest.TestCase):
    """Every tracked governance .md file appears in the prose step."""

    def test_every_tracked_markdown_file_is_covered(self):
        ci_text = CI_PATH.read_text(encoding="utf-8")
        body = prose_step_body(ci_text)
        explicit = set(re.findall(r"[\w./-]+\.md", body))
        docs_globbed = "docs/*.md" in body
        missing = []
        for name in tracked_markdown():
            if name.startswith(EXEMPT_PREFIXES):
                continue
            covered = name in explicit
            if not covered and docs_globbed and name.startswith("docs/"):
                covered = True
            if not covered:
                missing.append(name)
        self.assertEqual(missing, [])

    def test_audit_md_is_covered(self):
        ci_text = CI_PATH.read_text(encoding="utf-8")
        body = prose_step_body(ci_text)
        self.assertIn("AUDIT.md", body)


class ProseCommentTest(unittest.TestCase):
    """ci.yml must not claim AUDIT.md is absent or exempt from gating."""

    def test_no_absent_or_exempt_claim(self):
        ci_text = CI_PATH.read_text(encoding="utf-8")
        self.assertNotIn("deliberately absent", ci_text)
        self.assertNotIn("AGENTS.md exempts", ci_text)


if __name__ == "__main__":
    unittest.main()
