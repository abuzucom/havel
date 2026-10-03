# Template drift against abuzucom/agents

`abuzucom/agents` is the org's primary source of truth for AI-development
policy. This file records how havel's adoption differs from it, per the agents
`DRIFT.md` convention.

Pinned commit: `e6ddde181b60b23c542c064152ceaf2be6fa5ba3` (`abuzucom/agents`,
dated 2026-09-11). `upstream-files.json` records a per-file hash of every file
copied from that commit. Havel copies from `abuzucom/adorno`. Adorno pins the
same commit and carries two files foucault lacks.

## Expected to differ

- `AGENTS.md` is a bespoke document adapted from the generic template. It keeps
  the non-negotiable core adapted to this product, branch naming, git identity,
  and the full Style section. It drops container and runtime-root rules,
  dependency-lockfile rules, and function-size, nesting, and line-length code
  quality rules. This repository has no application code and no Dockerfiles.
- Non-negotiable rule 1 merges the foucault and adorno forms. Foucault forbids
  a real credential. Adorno forbids a real person's data. Havel fixtures carry
  both shapes. Rule 1 therefore forbids both. It adds a prohibition on copying
  a real privacy notice, record of processing, or impact assessment from a real
  organization.
- Non-negotiable rule 4 requires a stated unlawful-processing scenario.
  Foucault requires an exploit scenario. Adorno requires a user-harm scenario.
- Non-negotiable rule 10 is havel-only. It restates the enforcement-claim rule
  because this repository states several limitations where tooling coverage
  falls short of a rule.
- `.github/workflows/ci.yml` runs this repository's own checkers rather than
  reusing agents compliance workflows.
- `tests/test_enforce_branch_name.py` keeps the adorno trimmed `HOOK_MATCHERS`
  covering the two adopted hooks. The local fork below also changes it.

## Not adopted

- No `scripts/sync.py` and no generated tool instruction copies. `AGENTS.md` is
  the only instruction file for v1.
- No `.pre-commit-config.yaml` and none of the agents compliance workflows.
- No consent gate, destructive-command gates, or infrastructure-access gate.
  Havel adopts the same tooling subset the siblings adopted.
- No `scripts/run_tests.py` and no hook-coverage tooling. The runner imports
  `check_hook_coverage`. That module belongs to an adoption step this
  repository declines. Tests run through `python -m unittest discover -s tests`.
- No `adopters/` directory. Both siblings ship one. That convention tracks
  downstream repositories pinning and loading the prompt. All three
  repositories serve a paste workflow. No pin exists to record. No integration
  exists to track. The siblings should make the same removal.

## Kept where the siblings dropped

- Concurrency rules. Both siblings drop the set on the grounds of having no
  concurrency. The adopted upstream worker helpers `json_line_worker.py`,
  `json_line_worker_child.py`, and `persistent_main_worker.py` drive
  multi-process hook tests. Havel keeps the rules for that reason.
  Havel-authored code stays single-threaded.

## Divergence from the siblings

- Blocking threshold follows foucault at CRITICAL or HIGH rather than adorno's
  CRITICAL only. A HIGH privacy finding carries live statutory exposure.
- Hard blocker count is 10. Foucault ships 9. Adorno ships 5.
- `AUDIT.md` prose is style-checked, following adorno rather than foucault.
- Class detail splits into `docs/checks/`, following adorno.
- A second split axis, `docs/regimes/`, has no sibling equivalent.
- Two operating principles have no sibling equivalent. Credit a control only
  after tracing it to effect. Classify by observed behavior rather than by
  declared label.

## Originated here

Three files stay repo-agnostic for verbatim copy into the siblings.
Both siblings share the paste workflow and need the same tooling.

- `scripts/build_bundle.py`. Manifest-driven. It knows nothing about regimes,
  profiles, or classes.
- `bundles.json`. The manifest shape degrades correctly across all three
  repositories.
- The portable assertions in `tests/test_bundles.py`. Only the final assertion
  knows what a regime is.

Adorno needs the port most. Its `AUDIT.md` pasted alone tells a model that
thresholds and investigation steps live in 23 files it cannot see.

## Manual checks with no automated gate

- Cross-repository boundary drift. Class 2.20 and `docs/scope-boundary.md` name
  foucault classes. A foucault renumber leaves both stale. No test reads across
  repositories. Check the foucault references before each havel release.
- Source accuracy. `scripts/check_regime_refs.py` verifies a regime file
  carries a parseable date and a non-empty sources line. It cannot verify the
  statutory reading behind either.

## True drift

This section tracks a copied file's content diverging from its pinned upstream
commit. Run `python scripts/check_upstream_drift.py --check-local` in CI and
`--check-upstream --agents-path <checkout>` before each release.

Two files carry a deliberate local fork. A wholesale security review found
three defects across the pair. The fixes landed here first rather than waiting
for `abuzucom/agents`.

- `hooks/enforce_branch_name.py`. The `WORKFLOW_SCRIPT_ARGUMENTS` allowlist
  named three upstream scripts absent here. It denied every command
  `CONTRIBUTING.md` requires. The fork lists the havel commands and admits the
  prose checkers over existing Markdown files. Every form stays consent-gated.
- `hooks/enforce_branch_name.py`. The gate admitted git while repository config
  could name a program git runs. The fork protects `.git/config` and denies git
  when repository config carries an exec-capable key. `git config` without
  `--edit` stays reachable to remove one.
- `tests/test_enforce_branch_name.py`. One test inherited the host's
  `GIT_CONFIG_COUNT` vectors and failed on any runner exporting one. The fork
  removes those variables for that test. It also adds tests for both hook
  changes.

`python scripts/check_upstream_drift.py --write-manifest` re-hashed both files
and kept the pin. `--check-upstream` reports both as CHANGED by design. Port
the three fixes to `abuzucom/agents`, then re-adopt the upstream files and drop
this entry.
