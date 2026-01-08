#!/usr/bin/env bash

# Install all Python dependencies
pip install -r requirements.txt

# Collect static files (CSS, JS, images) into STATIC_ROOT for production
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate
