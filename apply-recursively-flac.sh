#!/bin/bash

set -e

directory_path="$1"
shift

script="$1"
shift

pattern='.*\.flac$'

# https://stackoverflow.com/a/246128
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

"$SCRIPT_DIR/apply-recursively.sh" "$directory_path" "$pattern" "$script" $@
