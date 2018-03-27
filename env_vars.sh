#!/bin/bash
# Script to set required environment variables for local development.
# Before running Django server for the first time, source this file.
#
# $ source env_vars.sh
# $ python manage.py runserver

export DJANGO_SECRET_KEY="!dg1bv&u2hxh%f#ohd_^l^dyw+m0iu)^0o50bldpan@ks&4s5n"
export DJANGO_DEBUG="True"
export DB_USER="apollo-user"
export DB_PSWD="f1r3dutt"
export CLOUDSQL_CONNECTION_STRING="ece397-198318:us-central1:apollo-db-dev"
export GCS_STATIC_FILES_BUCKET="ece397-apollo-static"