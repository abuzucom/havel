# Personal Information Protection and Electronic Documents Act (pipeda)
Last reviewed: 2026-09-12
Sources: https://laws-lois.justice.gc.ca/eng/acts/P-8.6/
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Canadian province enumeration.
- A bilingual English and French locale pair.
- A Canadian postal code validation.

Facts only an operator or a lawyer can confirm:

- Collecting, using, or disclosing personal information in commercial activity.
- Whether a provincial law substantially similar to the federal one governs instead.

## Class deltas

### [2.2@pipeda]
Openness requires policies and practices readily available in an understandable
form. Identifying purposes must happen at or before collection. The notice
names the accountable individual.
Severity shift: none.

### [2.8@pipeda]
Access requires informing the person of the existence, use, and disclosure of
that information and giving access to it. An organization addresses a
challenge to accuracy. Refusal of access requires stated reasons.
Severity shift: none.

### [2.21@pipeda]
A breach posing a real risk of significant harm requires report to the
Commissioner and notification to affected people as soon as feasible. A record
of every breach persists for 24 months regardless of reporting.
Severity shift: raise MEDIUM to HIGH where the organization keeps no breach record at all.

## Terms of art

- Organization maps to the controller concept.
- Personal information maps to information about an identifiable individual.
- Real risk of significant harm maps to the breach notification trigger.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to an access request | 30 days | Extension permitted with notice |
| Report a qualifying breach | As soon as feasible | None |
| Retain breach records | 24 months | None |

## What this regime does not add

- No sale opt-out link requirement. Class 2.9 carries no delta here.
- No cookie consent rule of its own. Class 2.14 carries no delta here.
