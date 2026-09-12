# Privacy and Electronic Communications Regulations (pecr)
Last reviewed: 2026-09-12
Sources: https://www.legislation.gov.uk/uksi/2003/2426/contents
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- Any signal supporting the `uk` profile.
- Browser storage writes on a surface serving United Kingdom visitors.
- A marketing send path reaching United Kingdom recipients.

Facts only an operator or a lawyer can confirm:

- Directing services to the United Kingdom market.
- Whether a recipient is an individual subscriber or a corporate one.

## Class deltas

### [2.14@pecr]
Storage on or access to terminal equipment requires consent unless strictly
necessary for a service the subscriber requested. The consent standard follows
the retained regulation. The rule covers cookies and every equivalent storage
technique.
Severity shift: raise HIGH to CRITICAL where non-essential storage precedes consent on a surface serving United Kingdom visitors.

### [2.26@pecr]
Unsolicited electronic marketing to an individual subscriber requires prior
consent. The soft opt-in exception permits marketing similar products where the
details came from a sale or negotiation, an opt-out appeared at collection, and
an opt-out appears in every message. Corporate subscribers carry a
different rule.
Severity shift: raise MEDIUM to HIGH where no opt-out appears in the message.

## Terms of art

- Subscriber maps to the person or organization holding the service contract.
- Soft opt-in maps to the existing-customer marketing exception.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Obtain consent before non-essential storage | Before the write | None |
| Provide an opt-out in every marketing message | Every message | None |

## What this regime does not add

- No rights set of its own. Class 2.8 deltas live in `gdpr.md`.
- No transfer mechanism of its own. Class 2.13 deltas live in `uk-gdpr.md`.
