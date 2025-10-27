#!/bin/bash

# Load the database and db user for testing
psql --username=postgres -f movieworld_db_and_user.sql >/dev/null