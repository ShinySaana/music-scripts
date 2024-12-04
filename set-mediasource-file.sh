#!/bin/bash

set -e

audio_path="$1"
media="$2"

kid3-cli -c "set media '$media' 2" "$audio_path"
