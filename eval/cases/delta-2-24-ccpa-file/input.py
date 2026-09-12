"""Fixture exercising 2.24 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def price_for(user):
    return 19.0 if user.opted_out_of_sale else 12.0
