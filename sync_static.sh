#!/bin/bash
gsutil rsync -R static/ gs://$GCS_STATIC_FILES_BUCKET/static
