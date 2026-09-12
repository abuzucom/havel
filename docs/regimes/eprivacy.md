# ePrivacy Directive (eprivacy)
Last reviewed: 2026-09-12
Sources: https://eur-lex.europa.eu/eli/dir/2002/58/oj, https://eur-lex.europa.eu/eli/dir/2009/136/oj
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- Any signal supporting the `eu` profile.
- A cookie banner carrying a geographic rule naming the EU.
- Browser storage writes on a surface serving EU visitors.

Facts only an operator or a lawyer can confirm:

- Which member state implementation governs a given user.
- Whether the service is a provider of electronic communications.

National implementations vary. This directive binds member states rather than
organizations directly. Germany implements it as TTDSG, recorded in
`de-national.md`. The United Kingdom implements the equivalent as PECR,
recorded in `pecr.md`. Enumerating every member state implementation stays out
of v1 scope. Where a specific member state governs and no file exists, mark the
national delta NEEDS-HUMAN rather than assuming the directive text applies
verbatim.

## Class deltas

### [2.1@eprivacy]
Consent for storage on or access to terminal equipment takes the GDPR consent standard. Strictly necessary storage and storage solely to carry a communication are exempt.
Severity shift: none.

### [2.11@eprivacy]
Refusal must be as easy as acceptance. A banner offering acceptance at the first layer and refusal only through a settings journey fails.
Severity shift: raise MEDIUM to HIGH where no same-level refusal control exists.

### [2.14@eprivacy]
Storage on or access to terminal equipment requires prior consent unless strictly necessary. The rule covers cookies, local storage, session storage, IndexedDB, cache entries, device fingerprinting, and any equivalent technique. Technology neutrality means the mechanism does not matter.
Severity shift: raise HIGH to CRITICAL where non-essential storage precedes consent on a surface serving EU visitors.

### [2.15@eprivacy]
Analytics storage is not strictly necessary. Consent applies unless a member state recognizes a narrow audience-measurement exemption.
Severity shift: none.

### [2.26@eprivacy]
Unsolicited electronic marketing requires prior consent. An existing-customer exception permits marketing similar products where the contact details came from a sale, an opt-out appeared at collection, and an opt-out appears in every message.
Severity shift: raise MEDIUM to HIGH where no opt-out appears in the message.

## Terms of art

- Terminal equipment maps to a person's own device and its storage.
- Strictly necessary maps to storage without which the requested service cannot function.
- Electronic mail maps to email, SMS, and equivalent messaging.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Obtain consent before non-essential storage | Before the write | None |
| Provide an opt-out in every marketing message | Every message | None |

## What this regime does not add

- No rights set of its own. Class 2.8 deltas live in `gdpr.md`.
- No retention schedule of its own. Class 2.7 deltas live in `gdpr.md`.
- No transfer mechanism of its own. Class 2.13 deltas live in `gdpr.md`.
