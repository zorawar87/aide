#!/bin/bash

tail -1 out.json | egrep -o --color=auto \"mid\":\ [0-9]+ | tail -1 | egrep -o [0-9]+
