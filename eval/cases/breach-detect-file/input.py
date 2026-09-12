"""Admin console."""


def view_customer(admin, customer_id):
    """Return a full customer record with no audit write."""
    return db.customers.get(customer_id)


def export_all(admin):
    return db.customers.all()
