"""Fixture exercising 2.5 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def store_sensitive(user_id, form):
    return db.profiles.update(user_id, {"religion": form["religion"]})
