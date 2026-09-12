"""Post-purchase mail."""


def send_similar_product_offer(customer):
    """Market a similar product to an existing customer."""
    if not customer.purchased_before:
        raise ValueError("soft opt-in requires a prior purchase")
    if customer.marketing_opted_out:
        return None
    return mailer.send(
        customer.email,
        template="similar_product",
        unsubscribe_url=unsubscribe_link(customer),
        footer="You receive this because you bought a similar product.",
    )
