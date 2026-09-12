# Scope boundary

This document states what havel does not check. Every bundle includes it.

A bundle reads as comprehensive. A clean verdict from it otherwise risks
reading as a statement that the cryptography, the signature formats, the
certificate handling, and the compliance program are sound. Havel checks none
of those.

Each exclusion names a destination. An exclusion with no destination sends the
reader nowhere.

## Security and cryptography

Routes to `abuzucom/foucault`.

- Cryptographic strength, algorithm choice, and construction.
- Certificate chain validation and revocation checking.
- Key custody, hardware security modules, and secret storage.
- Qualified electronic signature and timestamp formats.
- Authentication, authorization bypass, and injection.
- General application security.

Class 2.20 is the seam. It covers only the controls a privacy regime names as
an obligation, such as encryption at rest for personal data and least privilege
on personal-data stores. Foucault owns whether a control holds against an
attacker. Class 2.20 owns whether the access model matches processing
necessity.

## Employment context

Routes to the employment sibling repository.

The data subject havel reviews is a user or a customer. Employee, candidate,
and contractor data falls outside.

That boundary resolves four classes without a per-class carve-out. Class 2.15
keeps consumer telemetry and releases workplace device monitoring. Class 2.18
keeps consumer profiling and releases hiring analytics. Class 2.25 keeps
customer identity verification and releases employment background checks. Class
2.5 keeps customer health data and releases occupational health records.

## Organizational and process obligations

Routes to whoever runs the compliance program.

- Appointing a data protection officer.
- Assigning data stewards or custodians.
- Audit scheduling and internal review cadence.
- Staff training.
- Supervisory authority registration and engagement.

Havel reviews code and declared artifacts. No repository contains an
appointment.

## Contract and consumer law

Routes nowhere. Outside havel entirely.

- Liability limitation and warranty disclaimer.
- Intellectual property and license grants.
- Termination conditions and notice periods.
- Dispute resolution and governing law.
- Pricing terms and refund policy.

A terms document falls in scope only for the claims it makes about personal
data. A statement that no data reaches third parties is in scope for that
sentence alone.

## Sectoral American law

Deferred beyond v1.

- HIPAA and health information covered entities.
- GLBA and financial institutions.
- COPPA and operators of child-directed services.
- FERPA and educational records.

Class 2.6 covers children's data under the comprehensive regimes. It does not
carry the COPPA operator obligations.
