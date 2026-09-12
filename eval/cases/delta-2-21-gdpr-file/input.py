"""Fixture exercising 2.21 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def read_record(actor, subject_id):
    return db.people.get(subject_id)
