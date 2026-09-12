"""Fixture exercising 2.14 under pecr."""

SUPPORTED_COUNTRIES = ["GB"]
CURRENCY = "GBP"


def head():
    return '<script src="https://cdn.example.invalid/analytics.js"></script>'
