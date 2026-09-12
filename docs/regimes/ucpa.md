# Utah Consumer Privacy Act (ucpa)
Last reviewed: 2026-09-12
Sources: https://le.utah.gov/xcode/Title13/Chapter61/13-61.html
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Utah entry in a state residency map or enumeration.
- A state-keyed opt-out table containing Utah.

Facts only an operator or a lawyer can confirm:

- Conducting business in Utah or targeting Utah residents.
- Revenue and consumer volume thresholds. Both sit higher than the other state laws.

## Class deltas

### [2.9@ucpa]
Opt-out rights cover targeted advertising and sale of personal data. Sale means
exchange for monetary consideration alone. Profiling carries no opt-out under
this regime.
Severity shift: none.

## Terms of art

- Sale maps to exchange for monetary consideration alone.
- Targeted advertising maps to advertising selected from cross-context activity.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | 45 days | One further 45 days |
| Cure period before enforcement | 30 days | None |

## What this regime does not add

This regime is materially weaker than the other comprehensive state laws. An
audit must not manufacture a finding by citing it.

- No appeal process requirement. Class 2.8 carries no delta here.
- No universal opt-out signal requirement. Class 2.10 carries no delta here.
- No profiling opt-out. Class 2.18 carries no delta here.
- No data protection assessment requirement. Class 2.22 carries no delta here.
- No right to correct personal data. The rights set is narrower.
