# Virginia Consumer Data Protection Act (vcdpa)
Last reviewed: 2026-09-12
Sources: https://law.lis.virginia.gov/vacodefull/title59.1/chapter53/
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Virginia entry in a state residency map or enumeration.
- A state-keyed opt-out table containing Virginia.

Facts only an operator or a lawyer can confirm:

- Conducting business in Virginia or targeting Virginia residents.
- Consumer volume thresholds.

## Class deltas

### [2.8@vcdpa]
A controller must establish an appeal process for a refused rights request. The
appeal response states the reasons and provides a method to contact the
Attorney General.
Severity shift: raise MEDIUM to HIGH where a refusal path exists with no appeal route.

### [2.9@vcdpa]
Opt-out rights cover targeted advertising, sale of personal data, and profiling
in furtherance of decisions producing legal or similarly significant effects.
Sale covers exchange for monetary consideration alone. That definition runs
narrower than the California one.
Severity shift: none.

## Terms of art

- Sale maps to exchange for monetary consideration alone.
- Targeted advertising maps to advertising selected from cross-context activity.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | 45 days | One further 45 days |
| Respond to an appeal | 60 days | None |

## What this regime does not add

- No universal opt-out signal requirement. Class 2.10 carries no delta here.
- No confirmed opt-in for marketing. Class 2.26 carries no delta here.
