# Scope profiles

A declared scope names profiles, slugs, or both. This table is the
authoritative expansion. `scripts/build_bundle.py` and
`scripts/check_regime_refs.py` both read it through one parser.

Not legal advice. Profile membership reflects an engineering grouping rather
than a legal determination.

## Profiles

| Profile | Expands to |
|---|---|
| `all` | every known slug |
| `baseline` | none |
| `eu` | `gdpr`, `eprivacy`, `eidas` |
| `eea` | `gdpr`, `eprivacy`, `eidas` |
| `uk` | `uk-gdpr`, `pecr` |
| `de` | `gdpr`, `eprivacy`, `eidas`, `de-national` |
| `germany` | `gdpr`, `eprivacy`, `eidas`, `de-national` |
| `us` | `ccpa`, `tdpsa`, `vcdpa`, `cpa`, `ctdpa`, `ucpa` |
| `us-ca` | `ccpa` |
| `us-tx` | `tdpsa` |
| `us-va` | `vcdpa` |
| `us-co` | `cpa` |
| `us-ct` | `ctdpa` |
| `us-ut` | `ucpa` |
| `canada` | `pipeda`, `law25` |
| `canada-qc` | `law25` |
| `brazil` | `lgpd` |

## Slugs

| Slug | Regime |
|---|---|
| `gdpr` | General Data Protection Regulation |
| `eprivacy` | ePrivacy Directive |
| `eidas` | eIDAS 2.0, privacy provisions only |
| `de-national` | German national implementations |
| `uk-gdpr` | UK General Data Protection Regulation |
| `pecr` | Privacy and Electronic Communications Regulations |
| `ccpa` | California Consumer Privacy Act as amended |
| `tdpsa` | Texas Data Privacy and Security Act |
| `vcdpa` | Virginia Consumer Data Protection Act |
| `cpa` | Colorado Privacy Act |
| `ctdpa` | Connecticut Data Privacy Act |
| `ucpa` | Utah Consumer Privacy Act |
| `pipeda` | Personal Information Protection and Electronic Documents Act |
| `law25` | Quebec Law 25 |
| `lgpd` | Lei Geral de Protecao de Dados |

## Adding a jurisdiction

Add one `docs/regimes/<slug>.md` file. Add the slug to the slug table. Add the
slug to at least one profile row. `ScopeProfileTest` fails on a slug reachable
from no profile.

A pinned commit freezes the expansion. A new statute never widens an existing
audit without a deliberate bump.
