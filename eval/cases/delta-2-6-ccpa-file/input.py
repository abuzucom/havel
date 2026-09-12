"""Fixture exercising 2.6 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def enroll(user):
    """No age signal reaches the sale path."""
    data_broker.sell(user.email, user.interests)
