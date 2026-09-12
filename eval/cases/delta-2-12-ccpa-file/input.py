"""Fixture exercising 2.12 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def send_to_partner(user):
    """Labeled a service provider with no restricting contract term."""
    partner.post({"email": user.email}, label="service_provider")
