from nasa_image import NasaImage
from image_database import ImageDatabase

import requests

# Tests the scraping script
def database_builder():
    db = ImageDatabase()
    db.open_db()
    db.scrape_data()
    db.close_db()

# Tests an individual image
def individual_image(link):
    image = NasaImage(link)
    image.image_scrape()

# Tests an individual page
def individual_page(page_num):
    db = ImageDatabase()
    db.fetch_images(f'/page/{page_num}/')
    db.scrape_list(db.images)

def main():
    database_builder()

if __name__ == '__main__':
    main()