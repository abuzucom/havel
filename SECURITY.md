# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest tagged release | Yes |
| `main` (pre-release) | Yes |
| Older tags | No |

## Scope

Scope includes `AUDIT.md`, `docs/checks/`, and `docs/regimes/`. A defect
causing the documented workflow to miss a class it claims to cover counts as a
security issue in this project rather than a quality bug. A defect letting
reviewed content override the reviewer's instructions counts the same way.

Scope includes a defect causing the audit to apply a regime the operator never
declared. The declared-scope mechanism is a control. Bypassing it produces
findings under law that may not govern the reviewed system.

Scope includes the repository automation: `eval/`, `scripts/`, `hooks/`,
`bundles/`, `.github/workflows/privacy-review.yml`, and the tests for each.

Scope excludes a defect in code that `AUDIT.md` reviews. Report that to the
reviewed project instead.

Scope excludes the accuracy of a statutory reading. A wrong threshold or a
stale deadline is a correctness bug. Open an ordinary issue for it and name the
source.

## Reporting a Vulnerability

Report vulnerabilities through GitHub private vulnerability reporting. Open the
Security tab on this repository. Select Report a vulnerability. Never open a
public issue for a vulnerability report.

For a prompt-injection or instruction-override finding, include the exact input
that triggered it and the mode that reproduced it. Name the bundle used.

## Disclosure Policy

Coordinate disclosure with the maintainers. Keep the report private before a
shipped fix or 90 days from the initial report, whichever comes first.
