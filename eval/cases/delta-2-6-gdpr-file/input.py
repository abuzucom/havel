"""Fixture exercising 2.6 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def enroll(user):
    """No age signal reaches the sale path."""
    data_broker.sell(user.email, user.interests)
