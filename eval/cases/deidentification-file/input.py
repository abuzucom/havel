"""Analytics export."""

import hashlib


def pseudonymize(email):
    return hashlib.sha256(email.encode()).hexdigest()


def export_row(user):
    return {
        "uid": pseudonymize(user.email),
        "email": user.email,
        "postal_code": user.postal_code,
        "birth_date": user.birth_date,
    }
