#!/bin/bash

set -e

audio_path="$1"
format='%{disc"-"}%{track}. %{title}'

kid3-cli -c "fromtag '$format' 2" "$audio_path"
