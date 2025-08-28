#!/bin/bash
DATABASE="images.db"
OUTPUT="out.log"
ERROR="error.log"

echo -e "\nStart script called! Beginning file management before running main."

if test -f $DATABASE; 
then
    rm $DATABASE
fi

if test -f $OUTPUT; 
then
    rm $OUTPUT
fi

if test -f $ERROR; 
then
    rm $ERROR
fi

touch $OUTPUT
touch $ERROR

echo
echo "File management completed! Executing main."

python3 main.py > $OUTPUT 2> $ERROR

echo
echo -e "Program Completed! See $OUTPUT and $ERROR for output."