#!/bin/bash
DATABASE="images.db"
OUTPUT="out.log"
ERROR="error.log"

if test -f $DATABASE; 
then
    echo "$DATABASE exists and is being deleted"
    rm $DATABASE
fi

if test -f $OUTPUT; 
then
    echo "$DATABASE exists and is being deleted"
    rm $DATABASE
fi

if test -f $ERROR; 
then
    echo "$DATABASE exists and is being deleted"
    rm $DATABASE
fi

touch $OUTPUT
touch $ERROR

python3 main.py >$OUTPUT 2>$ERROR