#!/bin/bash

######################################################
# Run the application in production
######################################################

# Exit immediately if a command exits with a non-zero status.
set -e

# Set up environment variables
echo "Setting up environment variables..."
source setup_env_prod.sh

# Use the correct database for production
export DATABASE_URL=$DATABASE_URL_PROD

# Start the app using Unicorn web server
# Port is specified in the production environment.
gunicorn --bind 0.0.0.0:${PORT} --workers 4 --worker-class gthread --threads 5 "app:app"

