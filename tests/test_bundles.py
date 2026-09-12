#!/usr/bin/env python3
"""The committed bundle artifacts.

test_build_bundle.py asserts the producing logic. This module asserts the
committed output. The first five assertions are manifest-driven and port to
abuzucom/foucault and abuzucom/adorno unchanged. Only the last knows what a
regime is.
"""
import importlib.util
import json
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BUNDLES_DIR = REPO_ROOT / "bundles"
CHECKS_DIR = REPO_ROOT / "docs" / "checks"
BUILDER_PATH = REPO_ROOT / "scripts" / "build_bundle.py"
BOUNDARY_TITLE = "# Scope boundary"
REPO_PATH_PATTERN = re.compile(r"`(docs/(?:checks|regimes)/[A-Za-z0-9._-]+\.md)`")


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_bundle", BUILDER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = _load_builder()
MANIFEST = builder.load_manifest(REPO_ROOT)


def bundle_path(scope: str, tier: str) -> Path:
    return builder.output_path(REPO_ROOT, scope, tier)


class CurrencyTest(unittest.TestCase):
    """Every committed bundle matches its sources."""

    def test_check_mode_passes(self):
        self.assertEqual(builder.main([str(REPO_ROOT), "--check"]), 0)


class ManifestPairingTest(unittest.TestCase):
    """Manifest entries and committed bundles correspond exactly."""

    def test_every_entry_has_both_tiers_committed(self):
        for scope in MANIFEST:
            for tier in builder.TIERS:
                with self.subTest(scope=scope, tier=tier):
                    self.assertTrue(bundle_path(scope, tier).is_file())

    def test_no_orphan_bundle(self):
        expected = {bundle_path(scope, tier).name
                    for scope in MANIFEST for tier in builder.TIERS}
        actual = {path.name for path in BUNDLES_DIR.glob("*.md")}
        self.assertEqual(sorted(actual - expected), [])


class SourceResolutionTest(unittest.TestCase):
    """Every manifest source glob resolves to at least one file."""

    def test_every_glob_resolves(self):
        for scope, tiers in MANIFEST.items():
            for tier, patterns in tiers.items():
                with self.subTest(scope=scope, tier=tier):
                    resolved = builder.resolve_sources(REPO_ROOT, patterns)
                    self.assertTrue(resolved)


class DeadPointerTest(unittest.TestCase):
    """A full bundle resolves every repository path it names."""

    def test_full_tier_carries_every_path_it_references(self):
        for scope in MANIFEST:
            text = bundle_path(scope, "full").read_text(encoding="utf-8")
            listed = set(re.findall(r"^- `(.+)`$", text, re.MULTILINE))
            for reference in set(REPO_PATH_PATTERN.findall(text)):
                if reference not in listed:
                    continue
                stem = Path(reference).stem
                with self.subTest(scope=scope, reference=reference):
                    self.assertIn(stem, text)


class HeaderTest(unittest.TestCase):
    """Every bundle states what it is and carries the disclaimer."""

    def test_header_names_scope_and_tier(self):
        for scope in MANIFEST:
            for tier in builder.TIERS:
                with self.subTest(scope=scope, tier=tier):
                    first = bundle_path(scope, tier).read_text(
                        encoding="utf-8").splitlines()[0]
                    self.assertIn(scope, first)
                    self.assertIn(tier, first)

    def test_header_declares_the_scope(self):
        for scope in MANIFEST:
            for tier in builder.TIERS:
                with self.subTest(scope=scope, tier=tier):
                    text = bundle_path(scope, tier).read_text(encoding="utf-8")
                    self.assertIn(f"DECLARED_SCOPE: {scope}", text)

    def test_header_carries_the_disclaimer(self):
        for scope in MANIFEST:
            for tier in builder.TIERS:
                with self.subTest(scope=scope, tier=tier):
                    text = bundle_path(scope, tier).read_text(encoding="utf-8")
                    self.assertIn(builder.DISCLAIMER, text)


class BoundaryDocumentTest(unittest.TestCase):
    """Every bundle carries the scope boundary."""

    def test_boundary_included(self):
        for scope in MANIFEST:
            for tier in builder.TIERS:
                with self.subTest(scope=scope, tier=tier):
                    text = bundle_path(scope, tier).read_text(encoding="utf-8")
                    self.assertIn(BOUNDARY_TITLE, text)


class RegimeContentTest(unittest.TestCase):
    """Havel-only. Tier content matches the scope expansion exactly."""

    def _regimes(self, scope: str) -> set:
        patterns = MANIFEST[scope]["standard"]
        return {Path(p).stem for p in patterns if p.startswith("docs/regimes/")
                and not p.endswith("scope-profiles.md")}

    def test_full_tier_carries_every_class(self):
        expected = sorted(path.stem for path in CHECKS_DIR.glob("2.*.md"))
        for scope in MANIFEST:
            text = bundle_path(scope, "full").read_text(encoding="utf-8")
            for number in expected:
                with self.subTest(scope=scope, number=number):
                    self.assertIn(f"# {number} ", text)

    def test_standard_tier_carries_no_class_body(self):
        for scope in MANIFEST:
            text = bundle_path(scope, "standard").read_text(encoding="utf-8")
            with self.subTest(scope=scope):
                self.assertNotIn("## Barrier list", text)

    def test_tier_carries_exactly_the_scope_regimes(self):
        every = {path.stem for path in (REPO_ROOT / "docs" / "regimes").glob("*.md")
                 if path.name not in {"scope-profiles.md", "README.md"}}
        for scope in MANIFEST:
            included = self._regimes(scope)
            for tier in builder.TIERS:
                text = bundle_path(scope, tier).read_text(encoding="utf-8")
                for slug in sorted(every):
                    present = f"({slug})" in text
                    with self.subTest(scope=scope, tier=tier, slug=slug):
                        self.assertEqual(present, slug in included)


if __name__ == "__main__":
    unittest.main()
