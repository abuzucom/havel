"""Fixture exercising 2.18 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def decide(applicant):
    return {"decision": "declined" if model.score(applicant) < 0.4 else "approved"}
