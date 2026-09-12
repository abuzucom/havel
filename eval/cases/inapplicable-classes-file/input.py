"""Currency formatting."""

from decimal import Decimal, ROUND_HALF_UP


def format_amount(amount: Decimal, currency: str) -> str:
    """Return a display string for a monetary amount."""
    quantized = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    symbol = {"USD": "$", "EUR": "E", "GBP": "L"}.get(currency, "")
    return f"{symbol}{quantized}"
