#!/bin/bash

# Remove existing database
rm -f db.sqlite3

# Remove migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Install dependencies
pip3 install -r requirements.txt


# Make and apply migrations
python3 manage.py makemigrations
python3 manage.py migrate


# Load sample data
python3 load_sample_data.py

echo "Database has been reset and sample data has been loaded!" 