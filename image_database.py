from nasa_image import NasaImage
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import sqlite3

# class is built to store a pandas dataframe of the nasa image objects
class ImageDatabase:

    def __init__(self):

        self.images = []
        self.image_count = 0
        self.image_missed = 0
        self.data_list = []
        self.req = requests.get(NasaImage.link)
        self.conn = None
        self.cursor = None

        soup = BeautifulSoup(self.req.text, 'lxml')
        pages = soup.find_all('a', class_='page-numbers')
        self.page_count = int(pages[-2].text)

    def open_db(self):
        self.conn = sqlite3.connect('images.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                    CREATE TABLE images (
                        id INTEGER PRIMARY KEY,
                        link TEXT,
                        src TEXT,
                        title TEXT,
                        date TEXT,
                        author TEXT,
                        credit TEXT,
                        description TEXT
                    );
                    ''')
        
    def close_db(self):
        self.conn.close()

    def scrape_data(self):

        print('\nScrape Data method called! Starting Nasa image archive complete scrape...\n')

        for i in tqdm(range(1, self.page_count + 1), desc='Total Scrape Progress: '):
            self.images = []
            print(f'\n\n\nStarting Page {i} Search:\n')
            response = ''
            if i == 1:
                response = self.fetch_images()
            else:
                response = self.fetch_images(f'/page/{i}/')

            self.images = response[0]
            self.image_count += response[1]
            self.image_missed += response[2]

            print(f'\n-------Page {i} Search-------')

            print(f'Images on Page {i} found: {response[1]}')
            print(f'Images on Page {i} missed: {response[2]}\n')

            print(f'Total Images found: {self.image_count}')
            print(f'Total Images missed: {self.image_missed}')

            print('--------------------------\n')

            print(f'\nScraping Image sites for Page {i}')
            self.scrape_list(self.images)

            for image in self.images:
                self.data_list.append(image.to_tuple())
                        
            self.cursor.executemany('INSERT INTO images(link, src, title, date, author, credit, description) VALUES (?, ?, ?, ?, ?, ?, ?)', self.data_list)

    def fetch_images(self, path='') -> list:
        self.req = requests.get(NasaImage.link + path)
        self.image_count = 0
        self.invalid_image_count = 0

        if(self.req.status_code == 200):
            html_text = BeautifulSoup(self.req.text, 'lxml')

            for i, tag in enumerate(html_text.find_all(class_='hds-gallery-item-link', href=True)):
                try:
                    image = NasaImage(tag['href'])
                    self.images.append(image)
                    self.image_count += 1

                except Exception as e:
                    print(f'{e}. Skipping...')
                    self.invalid_image_count += 1

        else:
            raise Exception("Nasa Website could not be found")
        
        return [self.images, self.image_count, self.invalid_image_count]
    
    def select_db(self, sql):
        response = self.cursor.execute(sql)

        for row in response:
            print(row)

    def scrape_list(self, images) -> None:
        for image in images:
            image.image_scrape()
