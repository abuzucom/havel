"""Fixture exercising 2.13 under law25."""

PROVINCES = ["QC"]
LOCALE = "fr-CA"


def store_records(records):
    warehouse.write(records, region="us-east-1")
