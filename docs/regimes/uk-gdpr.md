# UK General Data Protection Regulation (uk-gdpr)
Last reviewed: 2026-09-12
Sources: https://www.legislation.gov.uk/eur/2016/679/contents, https://www.legislation.gov.uk/ukpga/2018/12/contents
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A United Kingdom entry in a country enumeration with no other EU entry.
- A sterling-only price path.
- A `.uk` domain constant or a UK postal code validation.

Facts only an operator or a lawyer can confirm:

- Establishment in the United Kingdom.
- Offering goods or services to people in the United Kingdom.
- Monitoring behavior of people in the United Kingdom.

The retained regulation tracks the EU text closely. Treat every `gdpr.md` delta
as applying unless this file states otherwise. This file records the
divergences alone.

## Class deltas

### [2.13@uk-gdpr]
Transfer outside the United Kingdom requires a United Kingdom adequacy
regulation, the international data transfer agreement, the addendum to the
standard contractual clauses, or a derogation. EU standard contractual clauses
alone do not satisfy the United Kingdom requirement without the addendum.
Severity shift: raise MEDIUM to HIGH where only EU clauses cover a United Kingdom transfer.

## Terms of art

- Retained regulation maps to the EU text as incorporated into domestic law.
- Information Commissioner maps to the supervisory authority.
- International data transfer agreement maps to the United Kingdom transfer instrument.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | One month | Two further months for complexity |
| Notify the supervisory authority of a breach | 72 hours from awareness | Delay permitted with reasons |

## What this regime does not add

- No divergence on notice content. Class 2.2 deltas in `gdpr.md` apply.
- No divergence on the rights set. Class 2.8 deltas in `gdpr.md` apply.
- No cookie rules of its own. Class 2.14 deltas live in `pecr.md`.
