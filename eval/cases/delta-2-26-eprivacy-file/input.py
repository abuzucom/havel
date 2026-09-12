"""Fixture exercising 2.26 under eprivacy."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def subscribe(email):
    db.subscribers.insert({"email": email, "active": True})
    mailer.send(email, template="offer")
