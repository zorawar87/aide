#!/bin/bash

EPOCH=$(./show.sh)
EPOCH=$(($EPOCH+1))
echo "./sanitise.sh all"
./sanitise.sh all
echo "./controller.py all log $EPOCH"
./controller.py all log $EPOCH
