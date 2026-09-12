"""Fixture exercising 2.26 under pecr."""

SUPPORTED_COUNTRIES = ["GB"]
CURRENCY = "GBP"


def subscribe(email):
    db.subscribers.insert({"email": email, "active": True})
    mailer.send(email, template="offer")
