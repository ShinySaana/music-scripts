#!/bin/bash

set -e

# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

python3 -m venv $SCRIPT_DIR/venv
source $SCRIPT_DIR/venv/bin/activate

$SCRIPT_DIR/set-musicbrainz-release-data.py "$@"
