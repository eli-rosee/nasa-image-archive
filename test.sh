#!/bin/bash
FILE="images.db"

if test -f $FILE; then
    echo "$FILE exists and is being deleted"
    rm $FILE
fi

python3 main.py