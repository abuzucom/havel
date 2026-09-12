"""Fixture exercising 2.2 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def collect(form):
    """Write personal data behind a notice that lists no legal basis."""
    return db.people.insert({"email": form["email"], "phone": form["phone"]})
