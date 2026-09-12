# eIDAS 2.0, privacy provisions only (eidas)
Last reviewed: 2026-09-12
Sources: https://eur-lex.europa.eu/eli/reg/2014/910/oj, https://eur-lex.europa.eu/eli/reg/2024/1183/oj
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A digital identity wallet integration.
- A qualified trust service provider integration.
- An attribute attestation or verifiable credential exchange.
- An EU signal paired with an identity verification flow.

Facts only an operator or a lawyer can confirm:

- Relying party registration status.
- Wallet provider or trust service provider role.

This file carries the privacy provisions alone. Signature formats, timestamp
qualification, certificate chain validation, revocation checking, and key
custody fall outside havel entirely. `docs/scope-boundary.md` routes each to
`abuzucom/foucault`.

## Class deltas

### [2.4@eidas]
A relying party requests only the attributes necessary for the service. Where the wallet supports a predicate proof, requesting the underlying attribute instead is over-collection. Proving an age threshold must not reveal a birth date.
Severity shift: raise MEDIUM to HIGH where a predicate is available and unused.

### [2.17@eidas]
A wallet provider keeps transaction data separate from personal data held for other services it offers. It collects no more than the wallet service requires.
Severity shift: none.

### [2.25@eidas]
Attribute attestation exchanges are processing. A relying party records which attributes it requested and why. Wallet use must not be traceable by the provider beyond service provision.
Severity shift: none.

## Terms of art

- Relying party maps to the service requesting an attribute.
- Attestation maps to a signed attribute claim.
- Selective disclosure maps to revealing one attribute rather than a whole credential.
- Predicate proof maps to proving a statement about an attribute without revealing it.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Request only necessary attributes | Every request | None |

## What this regime does not add

- No signature format requirement reaching havel. Qualified electronic signature formats, timestamp qualification, and certificate handling route to foucault.
- No rights set of its own. Class 2.8 deltas live in `gdpr.md`.
- No retention schedule of its own. Class 2.7 deltas live in `gdpr.md`.
