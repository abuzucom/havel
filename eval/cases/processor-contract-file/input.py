"""Third-party fan-out."""

import requests

PARTNERS = os.environ["PARTNER_ENDPOINTS"].split(",")


def broadcast_signup(user):
    for endpoint in PARTNERS:
        requests.post(endpoint, json={"email": user.email, "name": user.name})
