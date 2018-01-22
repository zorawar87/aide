#!/bin/bash

if [ -f "$1" ]; then
  EPOCH=$(./show.sh)
  EPOCH=$(($EPOCH+1))
  echo "./sanitise.sh all"
  ./sanitise.sh all
  echo "./controller.py $1 log $EPOCH"
  ./controller.py $1 log $EPOCH
else
  echo "$1 is not a valid file"
fi
