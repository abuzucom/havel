"""Customer intake."""

SUPPORTED_COUNTRIES = ["DE", "FR", "AT"]
LOCALES = ["de-DE", "fr-FR"]


def intake(form):
    return db.customers.insert({"email": form["email"]})
