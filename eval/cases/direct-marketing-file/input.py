"""Newsletter."""


def subscribe(email):
    db.subscribers.insert({"email": email, "active": True})
    mailer.send(email, template="welcome_offer")


def send_receipt(order):
    mailer.send(order.email, template="receipt", promo_block=True)
