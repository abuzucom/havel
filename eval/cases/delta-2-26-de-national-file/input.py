"""Fixture exercising 2.26 under de-national."""

SUPPORTED_COUNTRIES = ["DE"]
LOCALE = "de-DE"


def subscribe(email):
    db.subscribers.insert({"email": email, "active": True})
    mailer.send(email, template="offer")
