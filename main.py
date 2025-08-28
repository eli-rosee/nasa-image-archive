from nasa_image import NasaImage
from image_database import ImageDatabase

import requests

# Tests the scraping script
def database_builder():
    print('\nDatabase Builder Called! Starting Nasa image archive complete scrape...\n')

    db = ImageDatabase()
    db.open_db()
    db.scrape_data()
    db.close_db()

# Tests an individual image
def individual_image(link):
    print('\nIndividual Image Test Called! Starting image scrape...\n')

    image = NasaImage(link)
    image.image_scrape()

# Tests an individual page
def individual_page(page_num):
    print(f'\nIndividual Page Number Test Called! Starting Page {page_num} scrape...\n')

    db = ImageDatabase()
    db.fetch_images(f'/page/{page_num}/')
    db.scrape_list(db.images)

def main():
    individual_page('38')

if __name__ == '__main__':
    main()