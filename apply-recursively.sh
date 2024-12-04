#!/bin/bash

set -e

directory_path="$1"
shift

pattern="$1"
shift

script="$1"
shift

files=$(find "$directory_path" -regextype posix-egrep -regex "$pattern")

IFS=$'\n'
for file in $files
do
    "$script" "$file" $@
done
