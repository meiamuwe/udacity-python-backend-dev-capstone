#!/bin/bash

######################################################
# Setup environment variables for local development
######################################################

# --- Flask configuration
export FLASK_APP=app

# --- Database configuration
if [ -z "$DATABASE_URL_PROD" ]; then
    echo "Error: The DATABASE_URL_PROD environment variable is not set. Please define it." >&2
    failed="true"
fi

if [ -z "$DATABASE_URL_TEST" ]; then
    echo "Error: The DATABASE_URL_TEST environment variable is not set. Please define it." >&2
    failed="true"
fi


# --- Application port exposed
if [ -z "$PORT" ]; then
    echo "Error: The PORT environment variable is not set. Please define it." >&2
    failed="true"
fi


# --- External Auth Provider configuration: Auth0
export AUTH0_DOMAIN="dev-1syaxqsv2ewrr52u.us.auth0.com"
export AUTH0_AUDIENCE="movieworld-api"

# Setup callback for local development
export AUTH0_CALLBACK_SCHEME="https"
export AUTH0_CALLBACK_SERVER="movieworld-udacity-capstone.onrender.com"

# Check for required Auth0 environment variables. These should be set in your
# shell environment or a local .env file, not committed to version control.
if [ -z "$AUTH0_CLIENT_ID" ]; then
    echo "Error: The AUTH0_CLIENT_ID environment variable is not set. Please define it. Check the project submission comments." >&2
    failed="true"
fi

if [ -z "$AUTH0_CLIENT_SECRET" ]; then
    echo "Error: The AUTH0_CLIENT_SECRET environment variable is not set. Please define it. Check the project submission comments." >&2
    failed="true"
fi


if [ "$failed" = "true" ]; then
    exit 1
fi



