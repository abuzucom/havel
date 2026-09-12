"""Fixture exercising 2.8 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def handle_rights_request(kind, subject):
    if kind == "access":
        return db.users.get(subject)
    return {"status": "refused"}
