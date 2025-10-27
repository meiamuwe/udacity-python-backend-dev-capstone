#!/bin/bash

######################################################
# Bulding the application in production
######################################################

# Exit immediately if a command exits with a non-zero status.
set -e

# Set up environment variables
echo "Setting up environment variables..."
source setup_env_prod.sh


# Install all requirements 
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# Set up the database: Bring to current version
export DATABASE_URL=$DATABASE_URL_TEST
echo "Ensuring DB schema is at most current version..."
flask db upgrade

echo "Running application tests..."
python3 -m unittest tests

echo "Application is ready for deployment!"