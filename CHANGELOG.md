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
- `eval/`: a model-agnostic golden-corpus harness and 104 fixtures. Coverage
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
- `eval/cases/planted-scope-in-description-pr`: a description planting a
  competing `DECLARED_SCOPE:` line must not narrow the declared scope.
- `scripts/check_upstream_drift.py --write-manifest` with no other flag
  re-hashes the tracked files and keeps the pin.

### Security

- `privacy-review.yml` checks the pull request out into `pr/` and writes
  scratch files under `runner.temp`. A symlink committed in a pull request
  previously redirected the case-text write onto `AUDIT.md`.
- `privacy-review.yml` runs `model_call_command` from `base/`, a checkout of
  the calling repository at the base commit. The documented
  `python ci/call_model.py` previously ran the copy the pull request edits.
  A command reading pull request files from its working directory now finds
  none there.
- `privacy-review.yml` matches the whole final verdict line. An echoed format
  line or a glob token previously passed the gate as `APPROVE`.
- `privacy-review.yml` and `eval/run_eval.py` wrap reviewed content in an
  `UNTRUSTED CONTENT` frame closed by a fresh nonce. `AUDIT.md` step 0b grants
  scope authority to the opening `DECLARED_SCOPE:` line alone.
- `hooks/enforce_branch_name.py` protects `.git/config` and denies git while
  repository config names a program git runs.

### Fixed

- `privacy-review.yml` declares the optional `MODEL_API_KEY` secret and maps
  it into the model step. The documented `secrets:` block previously failed
  caller validation.
- `privacy-review.yml` skips the comment step on fork pull requests. A
  read-only token previously failed the job after an `APPROVE`.
- `eval/run_eval.py` grades `expected_classes`, `expected_regimes`, and
  `expected_regime_source` against `VERDICT_JSON` on live runs. The harness
  previously graded the verdict token alone.
- `hooks/enforce_branch_name.py` admits the commands `CONTRIBUTING.md`
  requires, each behind consent.
- `tests/test_enforce_branch_name.py` ignores host `GIT_CONFIG_*` vectors.

### Changed

- `hooks/enforce_branch_name.py` and `tests/test_enforce_branch_name.py` carry
  a local fork of the pinned `abuzucom/agents` files. `docs/template-drift.md`
  records it.
