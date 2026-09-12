"""Fixture exercising 2.8 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def handle_rights_request(kind, subject):
    if kind == "access":
        return db.users.get(subject)
    return {"status": "refused"}
