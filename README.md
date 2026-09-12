# Havel

Operating instructions for an AI agent that audits code for data-privacy
compliance. It works against a pull request, a single file, a code fragment, a
whole codebase, or a declared artifact paired with its implementation.

**Not legal advice.** Havel distills public statutory text into engineering
checklists. It carries no warranty. No output establishes compliance. Every
finding forms an input to legal review rather than a substitute for it. Read
[`docs/legal-disclaimer.md`](docs/legal-disclaimer.md) before relying on any
result.

## Usage

Paste a bundle. The builder generates every file under
[`bundles/`](bundles) and the repository commits the result. Using havel needs
no tooling.

1. Pick the bundle matching the jurisdictions that govern the code.
2. Open the file. Copy it. Paste it into an LLM chat.
3. Paste the code under review after it.
4. Read the verdict line and the trailing not-legal-advice line.

The chosen bundle declares the regime scope. The scope and the text the model
holds become the same choice.

Each scope ships two tiers. The standard tier carries the hub, the scope regime
deltas, and the scope boundary. The full tier adds every class reference file.
A pull request review takes the standard tier. A whole-codebase audit takes the
full tier.

| Bundle | Standard | Full | Regimes applied |
|---|---|---|---|
| `baseline` | 32 KB | 120 KB | none |
| `eu` | 47 KB | 134 KB | gdpr, eprivacy, eidas |
| `de` | 49 KB | 136 KB | gdpr, eprivacy, eidas, de-national |
| `uk` | 36 KB | 124 KB | uk-gdpr, pecr |
| `us` | 46 KB | 133 KB | ccpa, tdpsa, vcdpa, cpa, ctdpa, ucpa |
| `canada` | 36 KB | 123 KB | pipeda, law25 |
| `brazil` | 35 KB | 122 KB | lgpd |
| `all` | 73 KB | 160 KB | every regime |

## Regime coverage

Havel covers 15 regimes across 29 failure-mode classes.

| Territory | Regimes |
|---|---|
| European Union | GDPR, ePrivacy, eIDAS 2.0 privacy provisions |
| Germany | TTDSG and UWG section 7, as `de-national` |
| United Kingdom | UK GDPR, PECR |
| United States | CCPA, TDPSA, VCDPA, CPA, CTDPA, UCPA |
| Canada | PIPEDA, Quebec Law 25 |
| Brazil | LGPD |

Sectoral American law stays out of v1. That exclusion covers HIPAA, GLBA,
COPPA, and FERPA.

The agent never decides which regimes apply. Applicability turns on facts
absent from code. The operator declares the scope by choosing a bundle, by
setting the workflow input, or by answering the question the agent asks.

## What this checks and what it does not

[`docs/scope-boundary.md`](docs/scope-boundary.md) lists every exclusion and
names where it belongs. Every bundle includes it.

Cryptography, certificate handling, key custody, signature formats, and
application security route to
[`abuzucom/foucault`](https://github.com/abuzucom/foucault). Class 2.20 is the
seam. It covers only the controls a privacy regime names as an obligation.
Foucault owns whether a control holds against an attacker. Class 2.20 owns
whether the access model matches processing necessity.

Employment-context processing routes to a separate sibling repository. The data
subject havel reviews is a user or a customer.

## Structure

| Path | Purpose |
|---|---|
| `AUDIT.md` | The hub. Sections 0 through 9 plus the regime scope table |
| `docs/checks/2.N.md` | Per-class mechanism, thresholds, and investigation |
| `docs/regimes/<slug>.md` | Per-regime deltas alone |
| `docs/regimes/scope-profiles.md` | The authoritative profile expansion |
| `bundles/` | Generated paste-ready documents |
| `eval/` | The golden corpus verifying the prompt |

## Versioning

Pin a tag or commit when loading a bundle into a deployment rather than
tracking `main`. `CHANGELOG.md` records what changed release to release. A
pinned commit freezes the profile expansion. A new statute therefore never
widens an existing audit without a deliberate bump.

## Verifying changes

`eval/` holds a golden corpus pairing fixtures with the verdict the prompt
should produce. `python eval/run_eval.py` validates the case set structure.
Add `--model-call module:function` to run it against a real model.

Continuous integration runs the structure check alone. Havel ships no model
credential. Behavioral guarantees need a live run. See
[`eval/README.md`](eval/README.md).

## CI integration

[`.github/workflows/privacy-review.yml`](.github/workflows/privacy-review.yml)
is a reusable `workflow_call` reference implementation. It checks out a pull
request diff, loads the prompt, runs an adopter-supplied model-call command,
posts the report, and optionally fails on `BLOCK` or `NEEDS-HUMAN`. An
escalation is not a pass. Havel ships no model
credential and no provider lock-in. Set the required `regimes` input once.
Take the value from counsel's answer rather than from the codebase appearance.

## Customization

- Name the languages, frameworks, and stores in use. Fixes then stay concrete.
- Record scope boundaries such as monorepo paths and generated files.
- Add a waiver mechanism and state who may use it.

## Contributing

See [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).
