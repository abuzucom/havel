# Changelog

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows SemVer. Pin a tag or commit when loading a bundle into a
deployment.

## [Unreleased]

### Added

- `AUDIT.md`: the data-privacy compliance audit-agent system prompt. Five
  review modes (PR, File, Piece, Wholesale, Data-map), ten operating
  principles, 29 failure-mode classes (2.1-2.29), a regime scope elicitation
  section, a mode-aware ten-step workflow centered on a personal-data lifecycle
  trace, ten hard blockers (section 5), a reporting format with a
  `VERDICT_JSON` companion and a required not-legal-advice trailing line,
  prompt-injection and false-positive discipline, and a zero-findings protocol.
- `docs/checks/`: 29 class reference files carrying barrier lists, severity
  posture, thresholds, investigation steps, and boundaries against adjacent
  classes.
- `docs/regimes/`: 15 regime files carrying deltas alone, plus
  `scope-profiles.md` holding the authoritative profile expansion and a
  generated delta matrix. Regimes cover GDPR, ePrivacy, eIDAS privacy
  provisions, German national implementations, UK GDPR, PECR, CCPA, TDPSA,
  VCDPA, CPA, CTDPA, UCPA, PIPEDA, LGPD, and Quebec Law 25.
- `bundles/`: 16 generated paste-ready documents. Eight scopes ship a standard
  tier and a full tier. Picking a bundle declares the regime scope.
- `scripts/build_bundle.py` and `bundles.json`: a manifest-driven,
  repo-agnostic bundle builder with a `--check` mode detecting stale output.
- `scripts/check_regime_refs.py`: reference-graph, profile-table, and regime
  currency verification, plus matrix generation.
- `eval/`: a model-agnostic golden-corpus harness and 103 fixtures. Coverage
  runs one case per class, one per hard blocker, one per mode, one per
  verdict-affecting regime delta, and 15 negative controls.
- `docs/scope-boundary.md`: every exclusion with a named destination.
  `docs/legal-disclaimer.md`: the not-legal-advice statement in full.
- `.github/workflows/privacy-review.yml`: a reusable, adoptable reference
  workflow running the prompt against a pull request.
  `.github/workflows/ci.yml`: branch name, git identity, structural eval,
  reference graph, bundle currency, tests, upstream drift, and prose checkers.
- `AGENTS.md`: a bespoke, privacy-work-specific instruction file. Adopts the
  branch-name and git-identity hooks plus the prose checkers from
  `abuzucom/agents`.
- `docs/template-drift.md`, `upstream-files.json`,
  `scripts/check_upstream_drift.py`: drift tracking against the pinned
  `abuzucom/agents` commit.
- `CONTRIBUTING.md` and `SECURITY.md`.
