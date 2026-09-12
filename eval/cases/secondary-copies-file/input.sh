#!/usr/bin/env bash
set -euo pipefail

pg_dump "$PRODUCTION_DATABASE_URL" > /tmp/prod.sql
psql "$STAGING_DATABASE_URL" < /tmp/prod.sql
echo "staging refreshed from production"
