#!/bin/bash

# Load the database and db user for testing
psql --username=postgres -f movieworld_db_test.sql >/dev/null