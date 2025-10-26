#!/bin/bash

######################################################
# Setup environment variables local development
######################################################

source setup_env_local.sh

# Install all requirements 
pip install -r requirements.txt

# Set up the database: Bring to current version
export DATABASE_URL=$DATABASE_URL_TEST
flask db upgrade

# Start the app using Flask in development mode with reload
flask run

