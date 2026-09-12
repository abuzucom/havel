"""Onboarding."""


def save_health_profile(user_id, form):
    """Store health answers on the ordinary profile path."""
    return db.profiles.update(user_id, {
        "blood_type": form["blood_type"],
        "conditions": form["conditions"],
        "medications": form["medications"],
    })
