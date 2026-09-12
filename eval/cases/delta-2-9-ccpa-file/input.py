"""Fixture exercising 2.9 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def share_for_ads(user):
    ad_partner.send(user.email, user.segments)
