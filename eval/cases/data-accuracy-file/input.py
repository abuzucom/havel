"""Risk scoring."""


def get_risk_tier(user_id):
    """Return a tier computed once at signup and never recomputed."""
    return db.risk_tiers.get(user_id)["tier"]


def update_email(user_id, email):
    db.users.update(user_id, {"email": email})
