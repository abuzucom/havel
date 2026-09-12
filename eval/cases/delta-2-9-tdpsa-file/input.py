"""Fixture exercising 2.9 under tdpsa."""

STATE_OPT_OUT = {"TX": "/opt-out"}


def share_for_ads(user):
    ad_partner.send(user.email, user.segments)
