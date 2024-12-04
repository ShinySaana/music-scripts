#!/bin/bash

set -e

audio_path="$1"
tag="$2"
value="$3"

kid3-cli -c "set '$tag' '$value' 2" "$audio_path"
