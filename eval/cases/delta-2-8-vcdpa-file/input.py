"""Fixture exercising 2.8 under vcdpa."""

STATE_OPT_OUT = {"VA": "/opt-out"}


def handle_rights_request(kind, subject):
    if kind == "access":
        return db.users.get(subject)
    return {"status": "refused"}
