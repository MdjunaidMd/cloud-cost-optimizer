#!/bin/sh
set -e

echo "Waiting for Postgres..."

until pg_isready -h db -U postgres > /dev/null 2>&1; do
  sleep 2
done

echo "Postgres is up, starting app..."
exec "$@"
