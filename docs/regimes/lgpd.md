# Lei Geral de Protecao de Dados (lgpd)
Last reviewed: 2026-09-12
Sources: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A `pt-BR` locale bundle.
- A Brazilian tax identifier field.
- A Brazilian postal code validation or address format.

Facts only an operator or a lawyer can confirm:

- Processing carried out in Brazil.
- Offering goods or services to people in Brazil.
- Data collected in Brazil.

## Class deltas

### [2.1@lgpd]
Processing requires one of ten legal bases recorded per purpose. The set is
wider than the EU set and includes credit protection and health protection.
Consent must be free, informed, and unambiguous, given for a specific purpose.
Severity shift: none.

### [2.2@lgpd]
The notice states the specific purpose, the form and duration of processing,
the controller identity and contact, shared responsibilities, and the rights
set. Generic purpose statements do not satisfy the specificity requirement.
Severity shift: raise MEDIUM to HIGH where the purpose statement is generic.

### [2.5@lgpd]
Sensitive personal data covers racial or ethnic origin, religious belief,
political opinion, union or religious organization membership, health, sex
life, genetic data, and biometric data. Processing requires specific consent or
a narrower listed basis.
Severity shift: none.

### [2.22@lgpd]
A controller maintains a record of processing operations. The authority can
also demand an impact report, particularly where processing rests on legitimate
interest.
Severity shift: none.

## Terms of art

- Controller maps to the controlador.
- Operator maps to the processor concept.
- Holder maps to the data subject.
- National authority maps to the supervisory authority.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Respond to a confirmation or access request | 15 days for a full response | None stated |
| Notify the authority of an incident | Reasonable time as set by the authority | None stated |

## What this regime does not add

- No cookie consent rule of its own. Class 2.14 deltas live in the ePrivacy family.
- No universal opt-out signal requirement. Class 2.10 carries no delta here.
