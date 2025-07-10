from nasa_image import NasaImage
from image_database import ImageDatabase

def main():
    db = ImageDatabase()
    db.scrape_data()

if __name__ == '__main__':
    main()