"""Nightly job."""


def build_marketing_segments():
    """Read delivery addresses collected for shipping and segment on them."""
    rows = db.query("SELECT user_id, shipping_city, order_total FROM orders")
    for row in rows:
        marketing.add_to_segment(row["user_id"], city=row["shipping_city"])
