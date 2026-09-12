"""Fixture exercising 2.10 under ctdpa."""

STATE_OPT_OUT = {"CT": "/opt-out"}


def boot(request):
    load_pixel()
    signal = request.headers.get("Sec-GPC")
