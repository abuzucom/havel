"""Orders."""

RETENTION_DAYS = {"accounts": 730, "orders": 2555}


def create_account(form):
    return db.accounts.insert({"email": form["email"], "basis": "contract"})


def charge(order):
    return payments.charge(order.total, reference=order.id)
