"""Signup handler."""


def create_account(form):
    """Persist an account with no recorded lawful basis."""
    return db.users.insert({
        "email": form["email"],
        "name": form["name"],
        "marketing_consent": form.get("marketing", False),
    })
