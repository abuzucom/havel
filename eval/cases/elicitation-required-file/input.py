"""Customer intake."""


def intake(form):
    return db.customers.insert({"email": form["email"], "phone": form["phone"]})
