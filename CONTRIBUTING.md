# Contributing

## Ground rules

Follow `AGENTS.md`. It governs branch naming, git identity, style, and scope
for every change to this repository, human or agent-authored.

## No build step

Everything runs on the standard library.

```console
python scripts/build_bundle.py --check
python scripts/check_regime_refs.py
python eval/run_eval.py
python -m unittest discover -s tests
```

## Changing AUDIT.md, a check file, or a regime delta

Any change affecting a verdict, a hard blocker (section 5), or a severity
mapping (section 1.7) needs a new or updated `eval/cases/` entry demonstrating
the change is still caught correctly. `AGENTS.md` non-negotiable rule 3 states
that requirement.

Assess every incoming checklist against what the taxonomy already says. Add
nothing an existing rule already covers. Each item has one of three outcomes.
An item already covered needs no change. An item covered in principle by a rule
too vague to fire needs that rule extended in place. An item introducing a
genuinely new sink, scenario, or obligation needs a new rule. Extend by
default. A parallel rule naming a sink an existing rule already names is a
defect.

Keep `AUDIT.md` under its 32768-character ceiling. Split reference material out
before exceeding it. Regime specifics belong in `docs/regimes/`, never in the
hub.

## Adding a regime

1. Add `docs/regimes/<slug>.md` with the five headings in order.
2. Add the slug to the slug table in `docs/regimes/scope-profiles.md`.
3. Add the slug to at least one profile row. A slug reachable from no profile
   fails `ScopeProfileTest`.
4. Add the scope to `bundles.json` where a new profile appears.
5. Reference each new `[2.N@slug]` token from the matching check file.
6. Add an eval case for every delta whose severity shift is not `none`.
7. Run `python scripts/check_regime_refs.py --write-matrix`.
8. Run `python scripts/build_bundle.py` and commit the regenerated bundles.

## Regime currency

Every regime file carries a `Last reviewed` date and a `Sources` line.
Refreshing that date is a review step rather than a background chore. Re-read
the source before changing the date. `scripts/check_regime_refs.py` warns for
any file older than six months and exits 0. A missing or malformed date fails
hard.

A `Sources` line cites statute and regulator publication alone. Vendor
guidance and blog restatements serve as review input. No such source belongs on
that line.

## Bundles

`bundles/` holds generated output. Never edit a bundle. Edit the sources and
run `python scripts/build_bundle.py`. Continuous integration runs
`--check` and fails on any byte difference.

## Version contract

Consumers pin a commit. Five changes are major.

- A class renumber.
- A verdict token change.
- A `VERDICT_JSON` schema change.
- A bundle rename or removal.
- A new hard blocker.

A new class, a new regime file, and a widened barrier list are minor. A wording
fix and a refreshed `Last reviewed` date are patch.

## Validation

Match the validation path to the artifact.

- Executable behavior. Write the failing test first. Run it. Implement second.
- Executable configuration. Add a behavioral test ahead of the behavior change.
- Policy and documentation. Run the static validation before and after. Never
  invent a behavioral test for prose.

`AUDIT.md`, `docs/checks/*.md`, and `docs/regimes/*.md` are the product rather
than documentation. An eval case running a real model against that prompt is a
genuine behavioral test.

Continuous integration runs the corpus in structure-only mode. Havel ships no
model credential. A change affecting a verdict finishes only after a live run
with `--model-call`.

## Pull requests

Open every pull request as a draft. Never push to `main`. State what changed.
For a verdict-affecting change, name the `eval/cases/` entries covering it.
