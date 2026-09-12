# Connecticut Data Privacy Act (ctdpa)
Last reviewed: 2026-09-12
Sources: https://www.cga.ct.gov/2022/act/Pa/pdf/2022PA-00015-R00SB-00006-PA.PDF
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Connecticut entry in a state residency map or enumeration.
- A state-keyed opt-out table containing Connecticut.

Facts only an operator or a lawyer can confirm:

- Conducting business in Connecticut or targeting Connecticut residents.
- Consumer volume thresholds.

## Class deltas

### [2.10@ctdpa]
A controller honors an opt-out preference signal. The signal carries an
affirmative choice rather than a browser default, and it must not unfairly
disadvantage another controller.
Severity shift: raise MEDIUM to HIGH where the code reads a signal and ignores it.

## Terms of art

- Opt-out preference signal maps to a browser or device level opt-out.
- Consumer maps to a Connecticut resident acting in an individual context.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | 45 days | One further 45 days |
| Respond to an appeal | 60 days | None |
| Honor an opt-out preference signal | Required | None |

## What this regime does not add

- No confirmed opt-in for marketing. Class 2.26 carries no delta here.
- No separate notice content list beyond the shared state shape.
