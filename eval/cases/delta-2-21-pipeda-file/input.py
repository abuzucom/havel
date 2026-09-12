"""Fixture exercising 2.21 under pipeda."""

PROVINCES = ["ON", "BC", "QC"]


def read_record(actor, subject_id):
    return db.people.get(subject_id)
