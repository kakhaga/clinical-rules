#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if a DELAY_START variable is provided
if [ -n "$DELAY_START" ]; then
  echo "⏱️ Delaying startup by $DELAY_START seconds..."
  sleep "$DELAY_START"
fi

echo "📦 Running database migrations..."
alembic upgrade head

echo "👟 Starting Evaluation Service..."
exec python -m app.main