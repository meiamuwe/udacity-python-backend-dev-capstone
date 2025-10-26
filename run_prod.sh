#!/bin/bash

######################################################
# Run the application in production
######################################################

# Use the correct database for production
export DATABASE_URL=$DATABASE_URL_PROD

# Start the app using Unicorn web server
# Port is specified in the production environment.
gunicorn --bind 0.0.0.0:${PORT} --workers 4 --worker-class gthread --threads 5 "app:app"

