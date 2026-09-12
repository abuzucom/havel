# Eval harness

Golden-corpus regression tests for the audit prompt. Each case under `cases/`
pairs a small privacy fixture with the verdict a careful reviewer applying
`AUDIT.md` should produce. `AGENTS.md` requires a new or updated case for any
change affecting a verdict, a hard blocker, or a severity mapping.

## Why this exists

`AUDIT.md` is a system prompt. Nothing about a well-written instruction
document guarantees a model follows it. This harness is the difference between
trusting the prompt and checking it.

## What CI proves and what it does not

Continuous integration runs the structure check alone. It confirms every
`expected.json` parses, every fixture loads, every declared scope resolves, and
every asserted token names a real class and a real slug. It proves no model
behavior whatever.

Every behavioral guarantee needs a live run. That covers the negative controls,
the calibration controls, the verdict-affecting delta cases, and the required
not-legal-advice trailing line. A verdict-affecting change validated by CI
alone stays unvalidated.

## Model-agnostic by design

`run_eval.py` never calls a model API and ships no credentials. Point it at a
locally supplied callable:

```console
python eval/run_eval.py --model-call mymodule:call_model
```

`call_model(system_prompt, mode, case_text) -> str` loads `AUDIT.md` as the
system prompt, sends `case_text` as a user turn, and returns the raw response.
Wire it to whichever provider a deployment uses.

`--model-call` resolves to an importable module and executes its code. Treat it
as a trusted input. Supply it only from a local invocation or a CI
configuration under this repository's control, never from pull request content.
`ci.yml` never passes it.

`eval/example_echo.py` provides a credential-free stub for testing the seam.

## Case format

```
eval/cases/<slug>/
  diff.patch | input.<ext> | datamap.md | ropa.json | notice.md
  context.md                 optional: description or ticket text
  expected.json              required
```

A Data-map case pairs a declared artifact with the implementation under review.

`expected.json` fields:

| Field | Meaning |
|---|---|
| `mode` | PR, File, Piece, Wholesale, or Data-map |
| `declared_scope` | Input side. A profile, a slug list, `all`, or `undeclared`. Absent means the case tests the ask branch |
| `expected_verdict` | Substring the verdict line must contain |
| `expected_classes` | Class numbers plus any `2.N@slug` delta tokens |
| `expected_regimes` | Assertion side. The fully expanded slug list |
| `expected_regime_source` | `declared`, `elicited`, or `undeclared` |
| `expect_json` | Whether to require a parseable `VERDICT_JSON` line |
| `notes` | Why this case expects that verdict |
| `fixture_notes` | Required. States the personal data is synthetic |
| `allow_non_ascii` | Set where the fixture needs non-ASCII content |

`declared_scope` reaches the prompt through a `DECLARED_SCOPE:` line at the
head of the case text. The reference workflow emits the same line. The corpus
exercises the real channel rather than a fixture-only one.

## Synthetic fixtures

Every fixture uses synthetic, freshly invented personal data. `fixture_notes`
states that on every case. `AGENTS.md` non-negotiable rule 1 forbids a real
person's data anywhere in this repository.

The ASCII rule reaches a fixture through the string-literal carve-out rather
than through an exemption. A synthetic name exercising class 2.19 or locale
handling counts as required domain data. A fixture identifier and a fixture
comment carry no such license. `allow_non_ascii` records the domain
requirement and forces the reason into `fixture_notes`.

## Coverage policy

The policy sets the case count rather than a chosen number. The corpus holds
103 cases.

- Every class 2.1 through 2.29 carries at least one behavioral case.
- Every hard blocker carries at least one case.
- Every mode carries at least one case.
- Every calibration rule in section 8 carries a negative control.
- Every regime delta shifting a verdict or a severity carries a case.

Structural coverage runs wider. `tests/test_reference_graph.py` asserts every
delta anchor exists and every reference resolves. Every delta therefore
carries a structural test. Only verdict-affecting deltas carry a behavioral
one.

## A limitation worth stating

A single-turn harness cannot assert the ask branch of the regime scope step.
`call_model` offers no channel for a follow-up question.
`elicitation-required-file` covers it on a weaker condition. The assertion
accepts a response asking the question. It accepts a response taking the
undeclared branch. It rejects a response applying a regime silently.
