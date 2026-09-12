"""Fixture exercising 2.25 under gdpr."""

SUPPORTED_COUNTRIES = ["DE", "FR", "IT", "ES", "NL"]


def verify(user_id, document, selfie):
    db.kyc.insert({"user_id": user_id, "document": document, "selfie": selfie})
