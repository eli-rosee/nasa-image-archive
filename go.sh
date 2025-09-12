#!/bin/bash
DATABASE="data/images.db"
MAIN="src/main.py"
# OUTPUT="out.log"
# ERROR="error.log"

echo -e "\nStart script called! Beginning file management before running main."

if test -f $DATABASE; 
then
    rm $DATABASE
fi

# if test -f $OUTPUT; 
# then
#     rm $OUTPUT
# fi

# if test -f $ERROR; 
# then
#     rm $ERROR
# fi

# touch $OUTPUT
# touch $ERROR

echo
echo "File management completed! Executing main."

python3 $MAIN

echo
echo -e "Program Completed!"