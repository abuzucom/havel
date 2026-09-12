"""Fixture exercising 2.2 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def collect(form):
    """Write personal data behind a notice that lists no legal basis."""
    return db.people.insert({"email": form["email"], "phone": form["phone"]})
