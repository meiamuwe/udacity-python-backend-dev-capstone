#!/bin/bash

# Use the database and db user for testing
export DATABASE_URL=$DATABASE_URL_TEST

# Run the tests
python3 -m unittest tests