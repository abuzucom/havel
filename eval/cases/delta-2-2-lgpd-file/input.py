"""Fixture exercising 2.2 under lgpd."""

LOCALE = "pt-BR"
TAX_ID_FIELD = "cpf"


def collect(form):
    """Write personal data behind a notice that lists no legal basis."""
    return db.people.insert({"email": form["email"], "phone": form["phone"]})
