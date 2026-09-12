# Quebec Law 25 (law25)
Last reviewed: 2026-09-12
Sources: https://www.legisquebec.gouv.qc.ca/en/document/cs/p-39.1
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A Quebec entry in a province enumeration.
- An `fr-CA` locale bundle.

Facts only an operator or a lawyer can confirm:

- Carrying on an enterprise in Quebec.
- Collecting personal information from people in Quebec.

## Class deltas

### [2.13@law25]
Communication outside Quebec requires a privacy impact assessment considering
the sensitivity of the information, the purpose, the protection measures, and
the legal framework of the destination. The assessment must conclude the
information will receive adequate protection.
Severity shift: raise MEDIUM to HIGH where personal information leaves Quebec with no assessment.

## Terms of art

- Enterprise maps to the controller concept.
- Communication outside Quebec maps to the cross-border transfer concept.
- Privacy impact assessment maps to the transfer assessment requirement.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to an access or rectification request | 30 days | None stated |
| Report a confidentiality incident carrying a risk of significant injury | Promptly | None |

## What this regime does not add

- No cookie consent rule of its own. Class 2.14 carries no delta here.
- No universal opt-out signal requirement. Class 2.10 carries no delta here.
