# German national implementations (de-national)
Last reviewed: 2026-09-12
Sources: https://www.gesetze-im-internet.de/ttdsg/, https://www.gesetze-im-internet.de/uwg_2004/, https://www.gesetze-im-internet.de/bdsg_2018/
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A German locale bundle.
- A German address format or postal code validation.
- A German-language consent banner.
- A `.de` domain constant.

Facts only an operator or a lawyer can confirm:

- Establishment in Germany.
- Directing services to the German market.

This file carries German national implementations together rather than one file
per statute. TTDSG implements the ePrivacy storage rules. UWG section 7 governs
direct marketing. BDSG supplements the GDPR. A file per statute multiplies
without limit.

## Class deltas

### [2.14@de-national]
TTDSG requires consent for storage on or access to terminal equipment, with a strictly necessary exemption. The rule stands independently of whether the stored data is personal.
Severity shift: none.

### [2.26@de-national]
UWG section 7 treats unsolicited advertising as an unreasonable nuisance. Email advertising requires prior express consent. Confirmed opt-in is the accepted method of demonstrating it, since a single opt-in cannot show the address owner consented. The existing-customer exception is narrow and requires notice at collection and in every message.
Severity shift: raise MEDIUM to HIGH where marketing sends without a validated confirmation step.

## Terms of art

- TTDSG maps to the German telecommunications and telemedia data protection act.
- UWG maps to the act against unfair competition.
- BDSG maps to the federal data protection act.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Validate a marketing confirmation before first send | Before activation | None |

## What this regime does not add

- No separate rights set. Class 2.8 deltas live in `gdpr.md`.
- No separate transfer mechanism. Class 2.13 deltas live in `gdpr.md`.
- No separate notice content list. Class 2.2 deltas live in `gdpr.md`.
