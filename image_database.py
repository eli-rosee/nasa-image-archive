from nasa_image import NasaImage
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm

# class is built to store a pandas dataframe of the nasa image objects
class ImageDatabase:

    def __init__(self):
        print('\nInitializing Nasa Daily Image DataBase!\n')
        self.images = []
        self.image_count = 0
        self.image_missed = 0
        self.req = requests.get(NasaImage.link)
        soup = BeautifulSoup(self.req.text, 'lxml')
        pages = soup.find_all('a', class_='page-numbers')
        self.page_count = int(pages[-2].text)

        for i in tqdm(range(1, self.page_count + 1), desc='Total Scrape Progress: '):
            print(f'\n\n\nStarting Page {i} Scrape:\n')
            response = ''
            if i == 1:
                response = self.fetch_images()
            else:
                response = self.fetch_images(f'/page/{i}/')

            self.images = response[0]
            self.image_count += response[1]
            self.image_missed += response[2]

            self.scrape_list(self.images)

            print(f'\n-------Page {i} scrape-------')

            print(f'Images on Page {i} found: {response[1]}')
            print(f'Images on Page {i} missed: {response[2]}\n')

            print(f'Total Images found: {self.image_count}')
            print(f'Total Images missed: {self.image_missed}')

            print('--------------------------\n')

        self.scrape_list(self.images)
        maxes = self.get_max()

        print(f'SRC Max: {maxes[0]}')
        print(f'Title Max: {maxes[1]}')
        print(f'Author Max: {maxes[2]}')
        print(f'Credit Max: {maxes[3]}')
        print(f'Description Max: {maxes[4]}')


    def fetch_images(self, path='') -> list:
        self.req = requests.get(NasaImage.link + path)
        image_count = 0
        invalid_image_count = 0

        if(self.req.status_code == 200):
            html_text = BeautifulSoup(self.req.text, 'lxml')

            for i, tag in enumerate(html_text.find_all(class_='hds-gallery-item-link', href=True)):
                try:
                    image = NasaImage(tag['href'])
                    self.images.append(image)
                    image_count += 1

                except Exception as e:
                    print(f'{e}. Skipping...')
                    invalid_image_count += 1

        else:
            raise Exception("Nasa Website could not be found")
        
        return [self.images, image_count, invalid_image_count]

    def scrape_list(self, images) -> None:
        for image in images:
            image.image_scrape()

    def images_to_data(self, images) -> pd.DataFrame:
        data_list = []
        for image in images:
            data_list.append(image.to_list())
        
        return pd.DataFrame(data= np.array(data_list), index=np.arange(1, len(images) + 1), columns=NasaImage.index_list)
