"""Fixture exercising 2.22 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def profile_everyone():
    for person in db.people.all():
        scores.write(person.id, model.score(person))
