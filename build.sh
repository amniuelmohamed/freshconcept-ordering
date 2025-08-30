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

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    admin_user = User.objects.create_superuser('admin', 'admin@freshconcept.com', 'admin123')
    # Set the role to admin for superuser
    admin_user.role = 'admin'
    admin_user.save()
    print('Superuser created: admin/admin123 with admin role')
else:
    print('Superuser already exists')
"

echo "Build completed successfully!"
