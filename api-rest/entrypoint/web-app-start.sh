#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

gunicorn --bind 0.0.0.0:2000 app:app