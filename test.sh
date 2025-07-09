#!/bin/bash
FILE="images.db"

if test -f $FILE; then
    echo f"\n$FILE exists and is being deleted"
    rm $FILE
fi

python3 main.py