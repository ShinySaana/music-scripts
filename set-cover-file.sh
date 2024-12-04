#!/bin/bash

set -e

audio_path="$1"
picture_path="$(realpath "$2")"

kid3-cli -c "set picture:'$picture_path' 1" "$audio_path"
