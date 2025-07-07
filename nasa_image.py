# imports
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

class NasaImage:
    link = "https://www.nasa.gov/image-of-the-day/"
    index_list = np.array(['Link', 'Image', 'Date', 'Author', 'Credit', 'Description'])

    @staticmethod
    def scrape_list(images) -> None:
        for image in images:
            image.image_scrape()

    @classmethod
    def images_to_data(cls, images) -> pd.DataFrame:
        data_list = []
        for image in images:
            data_list.append(image.to_list())
        
        return pd.DataFrame(data= np.array(data_list), index=np.arange(1, len(images) + 1), columns=cls.index_list)
    
    @classmethod
    def fetch_images(cls, path) -> list:
        req = requests.get(cls.link + path)
        images = []

        if(req.status_code == 200):
            html_text = BeautifulSoup(req.text, 'lxml')

            for tag in html_text.find_all(class_='hds-gallery-item-link', href=True):
                image = cls(tag['href'])
                images.append(image)

        else:
            raise Exception("Nasa Website could not be found")
        
        return images

    def __init__(self, link: str):
        self.link = link
        self.image = None
        self.title = None
        self.date = None
        self.author = None
        self.credit = None
        self.description = None

        req = requests.get(self.link)

        if req.status_code == 200:
            self.html_text = BeautifulSoup(req.text, 'lxml')
        else:
            raise Exception("Image website not found")

    def __repr__(self) -> str:
        return str(f'Link: {self.link}, Image: {self.image}, Title: {self.title}, Date: {self.date}, Author: {self.author}, Credit: {self.credit}, Description: {self.description}')

    def image_scrape(self) -> None:
        self.scrape_image()
        self.scrape_title()
        self.scrape_date()
        self.scrape_author()
        self.scrape_credit()
        self.scrape_description()
        
    def scrape_image(self) -> None:
        tag = self.html_text.find('img', class_='attachment-2048x2048 size-2048x2048')
        if tag and 'src' in tag.attrs.keys():
            self.image = tag['src']
        else:
            raise Exception("Cannot find image src")

    def scrape_title(self) -> None:
        title = self.html_text.find('h1').text
        if title:
            self.title = title
        else:
            raise Exception("Cannot find image title")

    def scrape_date(self) -> None:
        date = self.html_text.find('span', class_='heading-12 text-uppercase').text

        if date:
            self.date = date
        else:
            raise Exception("Cannot find image date")


    def scrape_author(self) -> None:
        author = self.html_text.find('h3', class_='hds-meta-heading heading-14').text

        if author:
            self.author = author
        else:
            raise Exception("Cannot find article author")

    def scrape_credit(self) -> None:
        credit = self.html_text.find('div', class_='hds-credits').text

        if credit:
            self.credit = credit
        else:
            raise Exception("Cannot find image credit")

    def scrape_description(self) -> None:
        description = ''

        bottom_credits = self.html_text.find('em')

        if bottom_credits:
            parent = bottom_credits.find_parent()
            descriptions = parent.find_all_previous('p',class_=False)
            descriptions.reverse()

            for p in descriptions:
                description += p.text

        else:
            time_tag = self.html_text.find('p')
            descriptions = time_tag.find_all_next('p')

            for p in descriptions:
                description += p.text
        
        if description != '':
            self.description = description
        else:
            raise Exception("Cannot determine image description")
        
    def to_list(self) -> list:
        return [self.link, self.image, self.date, self.author, self.credit, self.description]

def main():
    images = DailyImage.fetch_images("")
    DailyImage.scrape_list(images)
    df_daily = DailyImage.images_to_data(images)

    print(df_daily)

if __name__ == "__main__":
    main()