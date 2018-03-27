#!/bin/bash
# Important: Set development environment variables before using this script!
# $ source env_vars.sh
./cloud_sql_proxy -instances=$CLOUDSQL_CONNECTION_STRING=tcp:5432