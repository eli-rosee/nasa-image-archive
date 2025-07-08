# imports
from bs4 import BeautifulSoup
import requests
import numpy as np

# Class is built to contain each nasa image along with its characteristics
class NasaImage:

    # defining class static variables
    link = "https://www.nasa.gov/image-of-the-day/"
    index_list = np.array(['Link', 'Image', 'Date', 'Author', 'Credit', 'Description'])

    # initiates all vars to 0 and fetches daily image repo html text
    def __init__(self, link=""):
        if link:
            self.link = link
        else:
            self.link = NasaImage.link
        
        self.src = None
        self.title = None
        self.date = None
        self.author = None
        self.credit = None
        self.description = None

        req = requests.get(self.link)

        if req.status_code == 200:
            self.html_text = BeautifulSoup(req.text, 'lxml')
        else:
            raise Exception(f'Image website not found: {self.link}')

    # defines the debugging printing verison for a NasaImage ob
    def __repr__(self) -> str:
        return str(f'Link: {self.link}, Src: {self.src}, Title: {self.title}, Date: {self.date}, Author: {self.author}, Credit: {self.credit}, Description: {self.description}')

    # calls all of the scraping functions to retrieve all data on a NasaImage ob
    def image_scrape(self) -> None:
        self.scrape_src()
        self.scrape_title()
        self.scrape_date()
        self.scrape_author()
        self.scrape_credit()
        self.scrape_description()

    # scrapes the src of the NasaImage ob
    def scrape_src(self) -> None:
        tag = self.html_text.find('img', class_='attachment-2048x2048 size-2048x2048')
        if tag and 'src' in tag.attrs.keys():
            self.src = tag['src']
        else:
            raise Exception("Cannot find image src")

    # scrapes the title of the NasaImage ob
    def scrape_title(self) -> None:
        title = self.html_text.find('h1').text
        if title:
            self.title = title
        else:
            raise Exception("Cannot find image title")

    # scrapes the date of the NasaImage ob
    def scrape_date(self) -> None:
        date = self.html_text.find('span', class_='heading-12 text-uppercase').text

        if date:
            self.date = date
        else:
            raise Exception("Cannot find image date")

    # scrapes the author of the NasaImage ob
    def scrape_author(self) -> None:
        author = self.html_text.find('h3', class_='hds-meta-heading heading-14').text

        if author:
            self.author = author
        else:
            raise Exception("Cannot find article author")
    
    # scrapes the credit of the NasaImage ob
    def scrape_credit(self) -> None:
        credit = self.html_text.find('div', class_='hds-credits').text

        if credit:
            self.credit = credit
        else:
            raise Exception("Cannot find image credit")

    # scrapes the description of the NasaImage ob
    def scrape_description(self) -> None:
        description = ''

        time_tag = self.html_text.find('p')
        descriptions = time_tag.find_all_next('p')

        for p in descriptions:
            description += p.text
        
        if description != '':
            self.description = description
        else:
            raise Exception("Cannot determine image description")
        
    def to_list(self) -> list:
        return [self.link, self.src, self.date, self.author, self.credit, self.description]
