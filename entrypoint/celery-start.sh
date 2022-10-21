#!/bin/bash

set -o errexit
set -o nounset

celery -A tareas.tareas.celery_app worker --loglevel=$CELERY_LOG