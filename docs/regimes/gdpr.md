# General Data Protection Regulation (gdpr)
Last reviewed: 2026-09-12
Sources: https://eur-lex.europa.eu/eli/reg/2016/679/oj
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- An EU or EEA country enumeration in an address, shipping, or locale path.
- A euro-only price path with no other currency.
- An EU member locale bundle.
- An EU region constant on a store, queue, or bucket.
- A consent banner carrying a geographic rule naming the EU.

Facts only an operator or a lawyer can confirm:

- Establishment in the Union.
- Offering goods or services to people in the Union.
- Monitoring behavior of people in the Union.
- Controller or processor role for a given flow.

Scope comes from the declaration. This section makes the question answerable.

## Class deltas

### [2.1@gdpr]
Processing requires one of six lawful bases recorded per purpose. Valid consent is free, specific, informed, unambiguous, and demonstrable. Withdrawal takes no more effort than granting. Contract necessity reaches only processing the contract requires.
Severity shift: raise MEDIUM to HIGH where no purpose carries a recorded basis.

### [2.2@gdpr]
The notice enumerates controller identity and contact, data protection officer contact where required, purposes, legal basis per activity, legitimate interests where relied on, recipient categories, transfer safeguards, retention period per category, the rights set covering access, rectification, erasure, restriction, portability and objection, the right to withdraw consent, the right to lodge a complaint with a supervisory authority, whether provision is statutory or contractual, and automated decision-making information.
Severity shift: raise MEDIUM to HIGH where any element is absent.

### [2.3@gdpr]
Further processing must be compatible with the original purpose. Compatibility assessment considers the link between purposes, the context, the nature of the data, the consequences, and the safeguards.
Severity shift: none.

### [2.4@gdpr]
Data protection by design and by default applies. The default setting processes the minimum personal data for each specific purpose, including the amount collected, the extent of processing, the storage period, and accessibility.
Severity shift: raise MEDIUM to HIGH on a non-minimal default exposing data with no action by the person.

### [2.5@gdpr]
Special categories require an explicit condition beyond an ordinary basis. Criminal conviction data carries a separate rule.
Severity shift: raise HIGH to CRITICAL where the code records no condition.

### [2.6@gdpr]
Information society services offered directly to a child require parental authorization below the applicable age. Member states set that age between 13 and 16.
Severity shift: raise MEDIUM to HIGH where no age signal exists.

### [2.7@gdpr]
Storage limitation requires a period no longer than necessary for the purpose. Archiving in the public interest, scientific or historical research, and statistical purposes carry an exception with safeguards.
Severity shift: none.

### [2.8@gdpr]
Six rights need code paths. Those cover access, rectification, erasure, restriction, portability, and objection. Restriction retains the record and suspends processing. Portability requires a structured, commonly used, machine-readable format. Erasure obliges the controller to inform other controllers wherever it published the data.
Severity shift: raise MEDIUM to HIGH where restriction or objection has no path.

### [2.11@gdpr]
Consent is not freely given where performance is conditional on consent unnecessary to that performance. Pre-ticked boxes and silence do not constitute consent.
Severity shift: none.

### [2.12@gdpr]
A processor acts only on documented instructions under a contract stating subject matter, duration, nature, purpose, data types, subject categories, and obligations. Sub-processor engagement requires authorization. Joint controllers determining purposes together require a transparent arrangement.
Severity shift: raise MEDIUM to HIGH where no contract reference exists.

### [2.13@gdpr]
Transfer outside the Union requires an adequacy decision, appropriate safeguards such as standard contractual clauses or binding corporate rules, or a derogation. A transfer impact assessment accompanies safeguard-based transfers.
Severity shift: none.

### [2.15@gdpr]
Analytics processing needs a basis. Legitimate interest requires a balancing assessment recorded before reliance.
Severity shift: none.

### [2.16@gdpr]
Logs holding personal data are a processing operation subject to storage limitation, integrity, and confidentiality.
Severity shift: none.

### [2.17@gdpr]
Model processing needs a basis. Training on personal data requires compatibility with the collection purpose or a separate basis. Output about a person is personal data.
Severity shift: none.

### [2.18@gdpr]
A decision resting solely on automated processing and producing legal or similarly significant effects requires an exception, plus safeguards covering human intervention, the right to express a view, and the right to contest. The controller also provides meaningful information about the logic.
Severity shift: raise HIGH to CRITICAL where no human path exists at all.

### [2.19@gdpr]
Pseudonymized data remains personal data. Anonymous data falls outside the regulation only where re-identification is not reasonably likely by any means.
Severity shift: none.

### [2.20@gdpr]
Security of processing requires measures appropriate to the risk, including pseudonymization and encryption, confidentiality, integrity, availability, resilience, restoration, and regular testing.
Severity shift: none.

### [2.21@gdpr]
Notification to the supervisory authority follows without undue delay and within 72 hours of awareness where risk is likely. Communication to affected people follows without undue delay where risk is high. The controller records every breach regardless of notification.
Severity shift: raise MEDIUM to HIGH where no access logging supports scope determination.

### [2.22@gdpr]
A controller maintains a record of processing activities, subject to stated exemptions for smaller organizations. High-risk processing also needs a data protection impact assessment. Triggers cover systematic and extensive automated evaluation, large-scale special-category processing, and large-scale systematic monitoring of a public area.
Severity shift: raise MEDIUM to HIGH where a triggering activity has no assessment.

### [2.24@gdpr]
Consent conditional on unnecessary processing is not freely given. Detriment for refusing or withdrawing undermines the basis itself.
Severity shift: none.

### [2.25@gdpr]
Biometric data processed to uniquely identify a person is a special category requiring an explicit condition. Proofing artifacts are subject to minimization and storage limitation.
Severity shift: raise HIGH to CRITICAL where the file records no condition.

### [2.27@gdpr]
Accountability requires demonstrating compliance. An inventory supports that demonstration.
Severity shift: none.

### [2.28@gdpr]
A copy into a non-production environment is processing requiring a compatible purpose and equivalent safeguards.
Severity shift: none.

### [2.29@gdpr]
Personal data stays accurate and current. A controller erases or rectifies inaccurate data without delay.
Severity shift: none.

## Terms of art

- Controller maps to the party determining purposes and means.
- Processor maps to the party acting on instructions.
- Special category maps to the sensitive data set in class 2.5.
- Data subject maps to the person the data describes.
- Supervisory authority maps to the national regulator.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a rights request | One month | Two further months for complexity, with notice inside the first month |
| Notify the supervisory authority of a breach | 72 hours from awareness | Delay permitted with reasons |
| Communicate a high-risk breach to affected people | Without undue delay | None stated |
| Provide notice at collection | At collection time | None |

## What this regime does not add

- No confirmed opt-in requirement for direct marketing beyond the ePrivacy rules. Class 2.26 deltas live in `eprivacy.md` and the national files.
- No universal opt-out signal requirement. Class 2.10 deltas live in the American state files.
- No requirement for a sale opt-out link. Class 2.9 deltas live in `ccpa.md` and the American state files.
