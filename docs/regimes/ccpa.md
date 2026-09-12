# California Consumer Privacy Act as amended (ccpa)
Last reviewed: 2026-09-12
Sources: https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5, https://cppa.ca.gov/regulations/
Not legal advice. An engineering checklist distilled from public text.

## Applicability

Code-observable signals worth citing when proposing this regime:

- A `Do Not Sell or Share My Personal Information` route or link.
- A California entry in a state residency map or enumeration.
- A CCPA or CPRA configuration key.
- An advertising recipient paired with a state branch.

Facts only an operator or a lawyer can confirm:

- Doing business in California.
- Annual revenue threshold, records threshold, or revenue share from selling data.
- Business, service provider, contractor, or third party role for a given flow.

## Class deltas

### [2.2@ccpa]
Notice at collection states the categories collected, the sources, the business and commercial purposes, the third parties receiving each category, whether the category is sold or shared, and the retention period per category. A separate rights disclosure and an opt-out link accompany it.
Severity shift: raise MEDIUM to HIGH where the sale or share disclosure is absent.

### [2.3@ccpa]
Use beyond the disclosed purpose requires a new notice. Purposes must be compatible with the context of collection.
Severity shift: none.

### [2.5@ccpa]
Sensitive personal information carries a right to limit its use and disclosure to stated permitted purposes. The category includes precise geolocation, racial or ethnic origin, religious belief, union membership, genetic and biometric data, health, and sex life.
Severity shift: raise MEDIUM to HIGH where no limitation path exists.

### [2.6@ccpa]
Selling or sharing personal information of a person under 16 requires opt-in. Under 13 requires parental opt-in.
Severity shift: raise HIGH to CRITICAL where minor data is sold with no opt-in.

### [2.7@ccpa]
The notice discloses a retention period per category. Retention beyond the disclosed period violates the regime independent of the underlying purpose.
Severity shift: none.

### [2.8@ccpa]
Rights cover know, delete, correct, portability, and opt-out. A deletion request obliges the business to direct service providers and contractors to delete. Verification must be reasonable and proportionate.
Severity shift: raise MEDIUM to HIGH where deletion does not propagate to service providers.

### [2.9@ccpa]
Sale and share both trigger an opt-out. Share covers cross-context behavioral advertising with no exchange of value. The homepage carries the opt-out link and a person reaches it without an account.
Severity shift: raise MEDIUM to HIGH where no opt-out link exists.

### [2.10@ccpa]
A business honors an opt-out preference signal as a valid request. The regime makes honoring it mandatory rather than optional.
Severity shift: raise MEDIUM to HIGH where the code reads the signal and ignores it.

### [2.12@ccpa]
A service provider or contractor relationship requires contract terms restricting use to the business purpose. A recipient outside those terms is a third party and the flow is a sale or share. The label does not settle the classification.
Severity shift: raise MEDIUM to HIGH on a mischaracterized relationship.

### [2.24@ccpa]
The regime prohibits discrimination for exercising a right. That covers denying goods, charging different prices, providing a different quality, or suggesting any of those. A financial incentive stays permissible where the business discloses it, requires opt-in, and relates it reasonably to the value of the data.
Severity shift: raise MEDIUM to HIGH where a feature or price varies by privacy choice with no disclosed incentive.

## Terms of art

- Business maps to the controller concept.
- Service provider and contractor map to the processor concept.
- Sell maps to disclosure for monetary or other valuable consideration.
- Share maps to disclosure for cross-context behavioral advertising.
- Sensitive personal information maps to the class 2.5 category set with a different membership from the EU one.
- Consumer maps to a California resident.

## Thresholds and clocks

| Obligation | Deadline | Extension |
|---|---|---|
| Acknowledge a rights request | 10 business days | None |
| Respond to a rights request | 45 calendar days | One further 45 days with notice |
| Honor an opt-out | 15 business days | None |
| Notify prior recipients of an opt-out | 90 days | None |

## What this regime does not add

- No confirmed opt-in requirement for direct marketing. Class 2.26 carries no delta here.
- No general consent requirement before processing. The model is opt-out for adults.
- No cookie consent requirement of its own. Class 2.14 deltas live in the ePrivacy family.
