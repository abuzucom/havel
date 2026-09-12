"""Fixture exercising 2.1 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def create_account(form):
    """No lawful basis is recorded for any purpose."""
    return db.people.insert({"email": form["email"]})
