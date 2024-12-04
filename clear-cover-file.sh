#!/bin/bash

set -e

audio_path="$1"

kid3-cli -c "set picture:' ' 1" "$audio_path"
