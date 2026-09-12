# Colorado Privacy Act (cpa)
Last reviewed: 2026-09-12
Sources: https://leg.colorado.gov/sites/default/files/2021a_190_signed.pdf, https://coag.gov/resources/colorado-privacy-act/
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Colorado entry in a state residency map or enumeration.
- A state-keyed opt-out table containing Colorado.

Facts only an operator or a lawyer can confirm:

- Conducting business in Colorado or targeting Colorado residents.
- Consumer volume thresholds.

## Class deltas

### [2.9@cpa]
Opt-out rights cover targeted advertising, sale, and profiling in furtherance
of decisions producing legal or similarly significant effects. Sale means
exchange for monetary or other valuable consideration.
Severity shift: none.

### [2.10@cpa]
A controller honors a universal opt-out mechanism. The state maintains a list
of recognized mechanisms. The regime makes honoring a recognized mechanism
mandatory.
Severity shift: raise MEDIUM to HIGH where the code reads a recognized mechanism and ignores it.

### [2.18@cpa]
Profiling in furtherance of decisions producing legal or similarly significant
effects carries an opt-out. Such profiling also needs a data protection
assessment.
Severity shift: raise MEDIUM to HIGH where profiling has no opt-out.

## Terms of art

- Universal opt-out mechanism maps to a recognized browser or device signal.
- Profiling maps to automated processing evaluating personal aspects.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | 45 days | One further 45 days |
| Respond to an appeal | 45 days | None |
| Honor a universal opt-out mechanism | Required | None |

## What this regime does not add

- No confirmed opt-in for marketing. Class 2.26 carries no delta here.
