from nasa_image import NasaImage
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

class ImageDatabase:

    def __init__(self):
        pass

    def fetch_images(self, path) -> list:
        req = requests.get(NasaImage.link + path)
        images = []

        if(req.status_code == 200):
            html_text = BeautifulSoup(req.text, 'lxml')

            for tag in html_text.find_all(class_='hds-gallery-item-link', href=True):
                image = NasaImage(tag['href'])
                images.append(image)

        else:
            raise Exception("Nasa Website could not be found")
        
        return images

    def scrape_list(self, images) -> None:
        for image in images:
            image.image_scrape()

    def images_to_data(self, images) -> pd.DataFrame:
        data_list = []
        for image in images:
            data_list.append(image.to_list())
        
        return pd.DataFrame(data= np.array(data_list), index=np.arange(1, len(images) + 1), columns=NasaImage.index_list)
    
if __name__ == "__main__":
    path = "/"
    db = ImageDatabase()
    images = db.fetch_images(path)
    db.scrape_list(images)
    df_daily = db.images_to_data(images)

    print(df_daily)