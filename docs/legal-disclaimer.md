# Not legal advice

Havel produces engineering findings. It does not produce legal advice.

## What this repository is

A set of checklists distilled from public statutory text, written for an audit
agent reviewing code. Each regime file cites the statute it draws from and
records the date of the reading.

## What this repository is not

- Not legal advice, and not a substitute for a lawyer.
- Not a certification, an attestation, or an audit opinion.
- Not a warranty of any kind.
- Not a determination that any regime applies to any organization.

## What a finding means

A finding names an obligation the reviewed code appears not to meet. It is an
input to legal review. Confirm every finding with counsel before acting on it.

## What a clean result means

A clean result means the audit found no unmet obligation within its scope. It
establishes no compliance. Read `scope-boundary.md` for what falls outside.
Read the report scope statement for which regimes the audit applied and which
it did not.

An audit reporting `regime_source: "undeclared"` never ran the regime layer at
all. That result is not a statement about any jurisdiction.

## Currency

Statutes change. Every regime file carries a `Last reviewed` date and its
sources. A file older than six months carries an advisory warning from
`scripts/check_regime_refs.py`. Check the date before relying on a threshold or
a deadline.

## Applicability

Havel never determines which regimes apply to an organization. Applicability
turns on facts absent from code, including establishment, revenue, record
volume, and the controller or processor role for a given flow. The operator
declares the scope. Confirm that declaration with counsel.
