"""Invoice retention."""

STATUTORY_HOLD_YEARS = 7
RETENTION = {
    "invoices": {"years": STATUTORY_HOLD_YEARS, "basis": "legal_obligation"},
    "sessions": {"days": 30, "basis": "purpose_exhausted"},
}


def sweep():
    """Skip records under a recorded statutory retention obligation."""
    for record in db.invoices.expired_by_purpose():
        if record.basis == "legal_obligation":
            continue
        record.delete()
