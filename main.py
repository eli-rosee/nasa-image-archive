# imports
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

class DailyImage:
    link = "https://www.nasa.gov/image-of-the-day/"

    @staticmethod
    def index_list() -> np.array:
        return np.array(['Link', 'Image', 'Date', 'Author', 'Credit', 'Description'])

    @staticmethod
    def image_index() -> list:
        req = requests.get(DailyImage.link)
        images = []

        if(req.status_code == 200):
            html_text = BeautifulSoup(req.text, 'lxml')

            for tag in html_text.find_all(class_='hds-gallery-item-link', href=True):
                image = DailyImage(tag['href'])
                images.append(image)

        else:
            raise Exception("Nasa Website could not be found")
        
        return images

    @staticmethod
    def images_to_data(images) -> pd.DataFrame:
        data_list = []
        for image in images:
            image.attribute_check()
            data_list.append(image.to_list())
        
        np_data = np.array(data_list)
        return pd.DataFrame(data=np_data, index=np.arange(1, len(images) + 1), columns=DailyImage.index_list())

    @staticmethod
    def scrape_list(images) -> None:
        for image in images:
            image.image_scrape()

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
        self.image = self.html_text.find('img', 'attachment-2048x2048 size-2048x2048')['src']

    def scrape_title(self) -> None:
        self.title = self.html_text.find('h1').text

    def scrape_date(self) -> None:
        self.date = self.html_text.find('span', 'heading-12 text-uppercase').text

    def scrape_author(self) -> None:
        self.author = self.html_text.find('h3', 'hds-meta-heading heading-14').text

    def scrape_credit(self) -> None:
        self.credit = self.html_text.find('div', 'hds-credits').text

    def scrape_description(self) -> None:
        self.description = ''

        bottom_credits = self.html_text.find('em')

        if bottom_credits:
            parent = bottom_credits.find_parent()
            descriptions = parent.find_all_previous('p',class_=False)
            descriptions.reverse()

            for p in descriptions:
                self.description += p.text

        else:
            time_tag = self.html_text.find('p')
            descriptions = time_tag.find_all_next('p')

            for p in descriptions:
                self.description += p.text

    def attribute_check(self) -> None:
        self.check_link()
        self.check_image()
        self.check_title()
        self.check_date()
        self.check_author()
        self.check_credit()
        self.check_description()
    
    def check_link(self) -> None:
        if not self.link:
            raise ValueError(f'No link found for {self.title}')
        
    def check_image(self) -> None:
        if not self.image:
            raise ValueError(f'No image found for {self.title}')
        
    def check_title(self) -> None:
        if not self.title:
            raise ValueError(f'No title found for {self.link}')
        
    def check_date(self) -> None:
        if not self.date:
            raise ValueError(f'No date found for {self.title}')
        
    def check_author(self) -> None:
        if not self.author:
            raise ValueError(f'No author found for {self.title}')
        
    def check_credit(self) -> None:
        if not self.credit:
            raise ValueError(f'No credit found for {self.title}')

    def check_description(self) -> None:
        if not self.description or self.description == '':
            raise ValueError(f'No description found for {self.title}')
        
    def to_list(self) -> list:
        return [self.link, self.image, self.date, self.author, self.credit, self.description]

def main():
    images = DailyImage.image_index()
    DailyImage.scrape_list(images)
    df_daily = DailyImage.images_to_data(images)

    print(df_daily)

if __name__ == "__main__":
    main()