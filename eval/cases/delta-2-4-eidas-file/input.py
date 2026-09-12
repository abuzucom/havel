"""Fixture exercising 2.4 under eidas."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def request_attributes(wallet):
    """Ask for a whole credential where a predicate proof is available."""
    return wallet.request(["date_of_birth", "full_name", "address"])
