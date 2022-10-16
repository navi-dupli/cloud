#!/bin/bash

set -o errexit
set -o nounset

celery -A tareas.tareas worker --loglevel=$CELERY_LOG