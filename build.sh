#!/usr/bin/env bash
# Build script for Render deployment

# Exit on any error
set -o errexit

# Install Python dependencies
pip install -r requirements-production.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

echo "Build completed successfully!"
