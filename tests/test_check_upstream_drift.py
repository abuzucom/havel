#!/usr/bin/env python3
"""Behavior of the upstream drift manifest refresh.

A refresh re-hashes the files the manifest already tracks and keeps its
upstream pin. Run it against a real temporary directory holding real files.
"""
import hashlib
import importlib.util
import os
import pathlib
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retrying_temp_directory import RetryingTemporaryDirectory

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DRIFT_PATH = REPO_ROOT / "scripts" / "check_upstream_drift.py"
PINNED_COMMIT = "e" * 40


def _load_drift():
    """Import the drift checker by path."""
    spec = importlib.util.spec_from_file_location("check_upstream_drift", DRIFT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


drift = _load_drift()


class RefreshedManifestTest(unittest.TestCase):
    """A refresh re-hashes tracked files and keeps the pin."""

    def setUp(self):
        self._directory = RetryingTemporaryDirectory()
        self.root = pathlib.Path(self._directory.name)
        (self.root / "hooks").mkdir()
        (self.root / "hooks" / "gate.py").write_bytes(b"print('a')\r\n")
        (self.root / "notes.md").write_bytes(b"line\n")
        self.manifest = {
            "agents_commit": PINNED_COMMIT,
            "agents_repo": "abuzucom/agents",
            "files": {"hooks/gate.py": "stale", "notes.md": "stale"},
        }

    def tearDown(self):
        self._directory.cleanup()

    def test_every_tracked_file_is_rehashed(self):
        refreshed = drift.refreshed_manifest(self.manifest, self.root)
        self.assertEqual(
            refreshed["files"]["notes.md"],
            hashlib.sha256(b"line\n").hexdigest())

    def test_line_endings_are_normalized(self):
        refreshed = drift.refreshed_manifest(self.manifest, self.root)
        self.assertEqual(
            refreshed["files"]["hooks/gate.py"],
            hashlib.sha256(b"print('a')\n").hexdigest())

    def test_pin_and_repository_are_kept(self):
        refreshed = drift.refreshed_manifest(self.manifest, self.root)
        self.assertEqual(refreshed["agents_commit"], PINNED_COMMIT)
        self.assertEqual(refreshed["agents_repo"], "abuzucom/agents")

    def test_tracked_set_is_unchanged(self):
        (self.root / "untracked.py").write_text("x\n", encoding="utf-8")
        refreshed = drift.refreshed_manifest(self.manifest, self.root)
        self.assertEqual(sorted(refreshed["files"]), ["hooks/gate.py", "notes.md"])

    def test_input_manifest_is_not_mutated(self):
        drift.refreshed_manifest(self.manifest, self.root)
        self.assertEqual(self.manifest["files"]["notes.md"], "stale")

    def test_missing_tracked_file_raises(self):
        (self.root / "notes.md").unlink()
        with self.assertRaises(OSError):
            drift.refreshed_manifest(self.manifest, self.root)


if __name__ == "__main__":
    unittest.main()
