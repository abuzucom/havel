"""Fixture exercising 2.12 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def send_to_partner(user):
    """Labeled a service provider with no restricting contract term."""
    partner.post({"email": user.email}, label="service_provider")
