#!/bin/bash

set -e

audio_path="$1"

# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

"$SCRIPT_DIR/set-tag.sh" "$audio_path" compilation 0
