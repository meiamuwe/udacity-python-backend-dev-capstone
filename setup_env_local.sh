#!/bin/bash

######################################################
# Setup environment variables for local development
######################################################

# --- Flask configuration
export FLASK_APP=app
export FLASK_DEBUG="True"

# --- Database configuration
export DATABASE_URL_TEST='postgresql://movieworld_test:movieworld_test@localhost/movieworld_test'

# --- External Auth Provider configuration: Auth0
export AUTH0_DOMAIN="dev-1syaxqsv2ewrr52u.us.auth0.com"
export AUTH0_AUDIENCE="movieworld-api"

# Setup callback for local development
export AUTH0_CALLBACK_SCHEME="http"
export AUTH0_CALLBACK_SERVER="127.0.0.1:5000"

# Check for required Auth0 environment variables. These should be set in your
# shell environment or a local .env file, not committed to version control.
if [ -z "$AUTH0_CLIENT_ID" ]; then
    echo "Error: The AUTH0_CLIENT_ID environment variable is not set. Please define it. Check the project submission comments." >&2
fi

if [ -z "$AUTH0_CLIENT_SECRET" ]; then
    echo "Error: The AUTH0_CLIENT_SECRET environment variable is not set. Please define it. Check the project submission comments." >&2
fi



