from nasa_image import NasaImage
from image_database import ImageDatabase

def main():
    image = NasaImage('https://www.nasa.gov/image-article/stellar-duo/')
    image.image_scrape()
    print(image.date_conversion())

if __name__ == '__main__':
    main()