"""Customer intake."""


def intake(form):
    """Store a customer with no basis recorded."""
    return db.customers.insert({"email": form["email"], "name": form["name"]})
