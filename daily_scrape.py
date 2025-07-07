# imports
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageDraw, ImageFont
import shutil
import textwrap

# declares url base and sends a get request to the website
url_base = 'https://www.nasa.gov/'
https_response = requests.get(url_base)

# only runs the program if the get response is confirmed
if https_response.status_code == 200:

    # extracts the html text from the get request and turns it into soup with lxml parser
    html_page = https_response.text
    soup = BeautifulSoup(html_page, 'lxml')

    # extracts the image of the day html block
    image_block = soup.find('div', 'hds-image-of-the-day')

    # finds and stores the image title, description, and src
    image_title = image_block.find('p', 'heading-22').text
    image_text = image_block.find('p', 'p-md').text
    image_src = image_block.find('img').attrs['src']

    # if the image src was successfully obtained, run the rest of program
    if image_src:

        # request the image file specifically with a get request
        r = requests.get(image_src, stream=True)

        # opens up a file for the image and dumps the binary into it
        with open('images/daily_image.png', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        # opens the image file
        with Image.open('images/daily_image.png') as image:

            # draws the image to the screen
            draw = ImageDraw.Draw(image)

            # defining basic parameters for the draw text
            font = ImageFont.load_default(20)
            text_list = []

            # determining the color by sampling a pixel in the bottom middle and using
            # the complement to that color for the text for visibility purposes
            rgb_image = image.load()
            width, height = image.size
            r, g, b = rgb_image[width/2, height - 25]
            color = (255 - r, 255 - g, 255 - b)
            
            # Breaks the description up into multiple lines so that it can be drawn to the image without width being an issue
            for line in textwrap.wrap(image_text, width/15):
                text_list.append(line)
            
            # reverses the list for the enumeration to be accurate
            text_list.reverse()
            
            # draws each line of the description at different heights based on the enumeration (bottom center alignment)
            for i, line in enumerate(text_list):
                draw.text((width/2, height - (i * 25)), line, fill=color, font=font, align='center', anchor='md')

            # show and save the image
            image.show(image_title)
            image.save('images/daily_image_text.png')

    else:
        raise Exception("Image download could not be found")
else:
   raise Exception("Website could not be scraped")
