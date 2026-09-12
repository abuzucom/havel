"""Fixture exercising 2.10 under cpa."""

STATE_OPT_OUT = {"CO": "/opt-out"}


def boot(request):
    load_pixel()
    signal = request.headers.get("Sec-GPC")
