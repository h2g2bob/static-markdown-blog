#!/bin/bash
set -o nounset
set -o errexit

source env.sh

rsync --chmod=Da+rx,Fa+r --progress -r public/ "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
