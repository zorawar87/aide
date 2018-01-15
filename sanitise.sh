#!/bin/bash

# Utility to uniquely sort (sanitise) N files
# Usage: ./sanitise <file1 file2 ...>
# BUG: the true echo line should not print the name of $var

for var in "$@"
do
  if [ -f "$var" ]; then
    sort -uR "$var" -o "$var"
    echo "sorted uniquely into" $(wc -l "$var") "lines"
  else
    echo "$var is an invalid file"
    exit 1
  fi
done

