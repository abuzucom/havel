"""Fixture exercising 2.10 under ccpa."""

STATE_OPT_OUT = {"CA": "/do-not-sell"}


def boot(request):
    load_pixel()
    signal = request.headers.get("Sec-GPC")
