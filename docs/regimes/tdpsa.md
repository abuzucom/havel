# Texas Data Privacy and Security Act (tdpsa)
Last reviewed: 2026-09-12
Sources: https://statutes.capitol.texas.gov/Docs/BC/htm/BC.541.htm
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Texas entry in a state residency map or enumeration.
- A state-keyed opt-out table containing Texas.

Facts only an operator or a lawyer can confirm:

- Conducting business in Texas or producing products or services consumed there.
- Small business status under the federal definition.

The comprehensive American state laws share most obligations. Treat the
baseline classes as governing. This file records the divergences alone.

## Class deltas

### [2.9@tdpsa]
Opt-out rights cover targeted advertising, sale of personal data, and profiling
in furtherance of decisions producing legal or similarly significant effects.
Sale means disclosure for monetary or other valuable consideration. A required
notice states that the controller sells sensitive or biometric data where it
does so, using the statutory wording.
Severity shift: raise MEDIUM to HIGH where sensitive data is sold with no statutory notice.

## Terms of art

- Controller maps to the party determining purpose and means.
- Processor maps to the party acting on behalf of a controller.
- Sale maps to disclosure for monetary or other valuable consideration.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | 45 days | One further 45 days |
| Honor a universal opt-out signal | Required | None |
| Cure period before enforcement | 30 days | None |

## What this regime does not add

- No confirmed opt-in for marketing. Class 2.26 carries no delta here.
- No separate notice content list beyond the shared state shape. Class 2.2 carries no delta here.
