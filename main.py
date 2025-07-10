from nasa_image import NasaImage
from image_database import ImageDatabase

# Tests the scraping script
def test1():
    db = ImageDatabase()
    db.open_db()
    db.scrape_data()
    db.close_db()

# Tests an individual image
def test2(link):
    image = NasaImage(link)
    image.image_scrape()

def main():
    test1()

if __name__ == '__main__':
    main()