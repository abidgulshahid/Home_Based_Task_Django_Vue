#!/bin/bash

# Remove existing database
rm -f db.sqlite3

# Remove migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete


# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
echo "DEBUG=True" > .env
echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env

# Run migrations
python3 manage.py makemigrations
python3 manage.py migrate

# Load sample data
python3 load_sample_data.py


# Create superuser
python3 manage.py createsuperuser


echo "Setup complete! Run 'source venv/bin/activate' to activate the virtual environment."
echo "Then run 'python manage.py runserver' to start the development server." 
python3 manage.py runserver
