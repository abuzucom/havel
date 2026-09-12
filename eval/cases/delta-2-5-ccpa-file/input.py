"""Fixture exercising 2.5 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def store_sensitive(user_id, form):
    return db.profiles.update(user_id, {"religion": form["religion"]})
