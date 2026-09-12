#!/usr/bin/env python3
"""Behavior of the bundle builder.

test_bundles.py asserts the committed artifacts. This module asserts the
producing logic. Deterministic ordering matters most. A builder inheriting
filesystem order produces a different byte stream per machine.
"""
import importlib.util
import json
import os
import pathlib
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from retrying_temp_directory import RetryingTemporaryDirectory

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILDER_PATH = REPO_ROOT / "scripts" / "build_bundle.py"


def _load_builder():
    """Import the builder by path."""
    spec = importlib.util.spec_from_file_location("build_bundle", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = _load_builder()

BOUNDARY = "docs/scope-boundary.md"

MANIFEST = {
    "baseline": {
        "standard": ["AUDIT.md", BOUNDARY],
        "full": ["AUDIT.md", "docs/checks/*.md", BOUNDARY],
    },
    "eu": {
        "standard": ["AUDIT.md", "docs/regimes/gdpr.md", BOUNDARY],
        "full": ["AUDIT.md", "docs/checks/*.md", "docs/regimes/gdpr.md", BOUNDARY],
    },
}


def build_tree(root: str, manifest=None) -> pathlib.Path:
    """Write a minimal repository shaped like havel and return its root."""
    base = pathlib.Path(root)
    (base / "docs" / "checks").mkdir(parents=True)
    (base / "docs" / "regimes").mkdir(parents=True)
    (base / "bundles").mkdir()
    (base / "AUDIT.md").write_text("# AUDIT\n\nHub.\n", encoding="utf-8")
    for number in ("2.1", "2.2", "2.10"):
        (base / "docs" / "checks" / f"{number}.md").write_text(
            f"# {number} Title\n\nBody.\n", encoding="utf-8")
    (base / "docs" / "regimes" / "gdpr.md").write_text(
        "# GDPR (gdpr)\n\nDeltas.\n", encoding="utf-8")
    (base / "docs" / "scope-boundary.md").write_text(
        "# Scope boundary\n\nExclusions.\n", encoding="utf-8")
    (base / "bundles.json").write_text(
        json.dumps(MANIFEST if manifest is None else manifest), encoding="utf-8")
    return base


class ManifestTest(unittest.TestCase):
    """Manifest parsing rejects malformed input with a recovery action."""

    def test_missing_manifest_raises(self):
        with RetryingTemporaryDirectory() as temp:
            base = pathlib.Path(temp)
            (base / "bundles").mkdir()
            with self.assertRaises(builder.BundleError):
                builder.load_manifest(base)

    def test_malformed_manifest_raises(self):
        with RetryingTemporaryDirectory() as temp:
            base = build_tree(temp)
            (base / "bundles.json").write_text("{not json", encoding="utf-8")
            with self.assertRaises(builder.BundleError):
                builder.load_manifest(base)

    def test_missing_tier_raises(self):
        with RetryingTemporaryDirectory() as temp:
            base = build_tree(temp, manifest={"eu": {"standard": ["AUDIT.md"]}})
            with self.assertRaises(builder.BundleError):
                builder.load_manifest(base)


class ResolutionTest(unittest.TestCase):
    """Glob resolution is deterministic and rejects empty and escaping paths."""

    def setUp(self):
        self.temp = RetryingTemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = build_tree(self.temp.name)

    def test_glob_sorts_by_class_number(self):
        resolved = builder.resolve_sources(self.root, ["docs/checks/*.md"])
        names = [path.name for path in resolved]
        self.assertEqual(names, ["2.1.md", "2.2.md", "2.10.md"])

    def test_resolution_is_stable_across_calls(self):
        first = builder.resolve_sources(self.root, ["docs/checks/*.md"])
        second = builder.resolve_sources(self.root, ["docs/checks/*.md"])
        self.assertEqual(first, second)

    def test_glob_matching_nothing_raises(self):
        with self.assertRaises(builder.BundleError):
            builder.resolve_sources(self.root, ["docs/absent/*.md"])

    def test_missing_literal_source_raises(self):
        with self.assertRaises(builder.BundleError):
            builder.resolve_sources(self.root, ["docs/checks/9.9.md"])

    def test_source_escaping_the_root_raises(self):
        with self.assertRaises(builder.BundleError):
            builder.resolve_sources(self.root, ["../outside.md"])

    def test_unresolved_root_resolves_the_same_sources(self):
        """An unresolved root must not read as a path escaping the root.

        relative_to raises ValueError against an unnormalized root, and the
        handler reports that as an escaping source. A caller passing a
        relative or symlinked root then gets a security-shaped error for a
        sound path.
        """
        unresolved = self.root / "docs" / ".."
        self.assertEqual(
            builder.resolve_sources(unresolved, ["docs/checks/*.md"]),
            builder.resolve_sources(self.root, ["docs/checks/*.md"]),
        )


class RenderTest(unittest.TestCase):
    """Rendered bundles carry a header and every source section."""

    def setUp(self):
        self.temp = RetryingTemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = build_tree(self.temp.name)
        self.manifest = builder.load_manifest(self.root)

    def test_header_states_scope_and_tier(self):
        text = builder.render(self.root, "eu", "standard", self.manifest)
        self.assertIn("eu", text.splitlines()[0])
        self.assertIn("standard", text)

    def test_header_source_names_use_posix_separators(self):
        """A rebuild on Windows must produce the same bytes.

        str() on a relative path yields backslashes there, so every header
        source name would differ and --check would report the whole tree
        stale.
        """
        text = builder.render(self.root, "eu", "full", self.manifest)
        header = text.split(builder.SEPARATOR, 1)[0]
        self.assertIn("- `docs/checks/2.1.md`", header)
        self.assertNotIn("\\", header)

    def test_render_accepts_an_unresolved_root(self):
        text = builder.render(self.root / "docs" / "..", "eu", "standard",
                              self.manifest)
        self.assertEqual(text, builder.render(self.root, "eu", "standard",
                                              self.manifest))

    def test_header_carries_the_disclaimer(self):
        text = builder.render(self.root, "eu", "standard", self.manifest)
        self.assertIn(builder.DISCLAIMER, text)

    def test_boundary_document_is_included(self):
        text = builder.render(self.root, "eu", "standard", self.manifest)
        self.assertIn("Scope boundary", text)

    def test_standard_tier_omits_check_sections(self):
        text = builder.render(self.root, "eu", "standard", self.manifest)
        self.assertNotIn("2.10 Title", text)

    def test_full_tier_includes_every_check_section(self):
        text = builder.render(self.root, "eu", "full", self.manifest)
        for number in ("2.1", "2.2", "2.10"):
            self.assertIn(f"{number} Title", text)

    def test_unknown_tier_raises(self):
        with self.assertRaises(builder.BundleError):
            builder.render(self.root, "eu", "deluxe", self.manifest)

    def test_unknown_scope_raises(self):
        with self.assertRaises(builder.BundleError):
            builder.render(self.root, "atlantis", "standard", self.manifest)


class WriteTest(unittest.TestCase):
    """Writing produces every bundle and refuses to escape bundles/."""

    def setUp(self):
        self.temp = RetryingTemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = build_tree(self.temp.name)

    def test_build_writes_both_tiers_per_scope(self):
        self.assertEqual(builder.main([str(self.root)]), 0)
        for name in ("baseline.md", "baseline-full.md", "eu.md", "eu-full.md"):
            self.assertTrue((self.root / "bundles" / name).is_file(), name)

    def test_output_path_stays_inside_bundles(self):
        with self.assertRaises(builder.BundleError):
            builder.output_path(self.root, "../escape", "standard")


class CheckModeTest(unittest.TestCase):
    """--check compares without writing."""

    def setUp(self):
        self.temp = RetryingTemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = build_tree(self.temp.name)

    def test_check_passes_on_a_current_tree(self):
        self.assertEqual(builder.main([str(self.root)]), 0)
        self.assertEqual(builder.main([str(self.root), "--check"]), 0)

    def test_check_fails_on_a_stale_bundle(self):
        self.assertEqual(builder.main([str(self.root)]), 0)
        (self.root / "docs" / "checks" / "2.1.md").write_text(
            "# 2.1 Title\n\nChanged.\n", encoding="utf-8")
        self.assertEqual(builder.main([str(self.root), "--check"]), 1)

    def test_check_fails_on_a_missing_bundle(self):
        self.assertEqual(builder.main([str(self.root)]), 0)
        (self.root / "bundles" / "eu-full.md").unlink()
        self.assertEqual(builder.main([str(self.root), "--check"]), 1)

    def test_check_writes_nothing(self):
        self.assertEqual(builder.main([str(self.root)]), 0)
        before = (self.root / "bundles" / "eu.md").read_bytes()
        (self.root / "docs" / "regimes" / "gdpr.md").write_text(
            "# GDPR (gdpr)\n\nChanged.\n", encoding="utf-8")
        self.assertEqual(builder.main([str(self.root), "--check"]), 1)
        self.assertEqual((self.root / "bundles" / "eu.md").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
