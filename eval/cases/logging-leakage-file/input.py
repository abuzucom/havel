"""Order API."""

import logging

log = logging.getLogger(__name__)


def create_order(request):
    log.info("creating order for %s", request.json)
    try:
        return orders.create(request.json)
    except Exception:
        log.exception("order failed for user %s", request.user.email)
        raise
