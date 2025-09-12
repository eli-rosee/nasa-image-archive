from nasa_image import NasaImage
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import sqlite3

# class is built to store a pandas dataframe of the nasa image objects
class ImageDatabase:

    def __init__(self):
        self.req = requests.get(NasaImage.link)

        self.image_count = 0
        self.image_missed = 0
        self.scrape_errors = 0

        self.images = []
        self.data_list = []

        self.conn = None
        self.cursor = None

        soup = BeautifulSoup(self.req.text, 'lxml')
        pages = soup.find_all('a', class_='page-numbers')
        self.page_count = int(pages[-2].text)

    def open_db(self):
        self.conn = sqlite3.connect('data/images.db')
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

        for i in tqdm(range(1, self.page_count + 1), desc='Total Scrape Progress: '):
            self.images = []
            print(f'\n\n\nStarting Page {i} Search:\n')
            response = ''
            if i == 1:
                response = self.fetch_images()
            else:
                response = self.fetch_images(f'/page/{i}/')

            self.image_count += response[0]
            self.image_missed += response[1]

            for image in self.images:
                self.conn.execute(
                    """
                    INSERT INTO images (link, src, title, date, author, credit, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (image.link, image.src, image.title, image.date, image.author, image.credit, image.description)
                )
            
            self.conn.commit()

            print(f'\n-------Page {i} Search-------')

            print(f'Images on Page {i} found: {response[0]}')
            print(f'Images on Page {i} missed: {response[1]}\n')

            print(f'Total Images found: {self.conn.execute("SELECT COUNT(id) FROM images").fetchone()[0]}')
            print(f'Total Images missed: {self.image_missed}')

            print('--------------------------\n')

            print(f'\nScraping Image sites for Page {i}')
            self.scrape_list(self.images)

    def fetch_images(self, path='') -> None:
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
        
        return [image_count, invalid_image_count]
    
    def select_db(self, sql):
        response = self.cursor.execute(sql)

        for row in response:
            print(row)

    def scrape_list(self, images) -> None:
        for image in images:
            try:
                image.image_scrape()
            except Exception as e:
                print(f'{e}. Skipping...')
                self.scrape_errors += 1
