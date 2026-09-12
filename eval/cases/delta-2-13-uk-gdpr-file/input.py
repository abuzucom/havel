"""Fixture exercising 2.13 under uk-gdpr."""

SUPPORTED_COUNTRIES = ["GB"]
CURRENCY = "GBP"


def store_records(records):
    warehouse.write(records, region="us-east-1")
