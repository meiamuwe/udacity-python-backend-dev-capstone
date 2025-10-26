#!/bin/bash

######################################################
# Bulding the application in production
######################################################

# Set up environment variables
echo "Setting up environment variables..."
./setup_env_prod.sh


# Install all requirements 
echo "Installing requirements..."
pip install -r requirements.txt

# Set up the database: Bring to current version
echo "Ensuring DB schema is at most current version..."
flask db upgrade

echo "Running application tests..."
export DATABASE_URL=$DATABASE_URL_TEST
python3 -m unittest tests

echo "Application is ready for de deployment!"