#!/bin/bash

if [ ! -d  "images/" ]; then
    echo "Images directory does not exist! Creating a new one..."
    mkdir images/
fi

if [ -e "images/readme_image.png" ]; then
    echo "Removing readme_image.png..."
    rm images/readme_image.png
fi


if [ -e "images/daily_image.png" ]; then
    echo "Removing current daily_image.png..."
    rm images/daily_image.png
fi

if [ -e "images/daily_image_text.png" ]; then
    echo "Removing current daily_image_text.png..."
    rm images/daily_image_text.png
fi

python3 nasa_daily_image.py