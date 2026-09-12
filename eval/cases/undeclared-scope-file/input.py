"""Customer intake."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL", "IE"]
LOCALES = ["de-DE", "fr-FR", "it-IT"]
CURRENCY = "EUR"


def intake(form):
    """Store a customer with no basis and no retention period."""
    return db.customers.insert({
        "email": form["email"],
        "postal_code": form["postal_code"],
        "country": form["country"],
    })
