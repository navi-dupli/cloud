#!/bin/bash

set -o errexit
set -o nounset

celery -A tareas.celery worker --loglevel=$CELERY_LOG