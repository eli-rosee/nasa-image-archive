# imports
from bs4 import BeautifulSoup
import requests
import numpy as np
from datetime import datetime
import re

# Class is built to contain each nasa image along with its characteristics
class NasaImage:

    # defining class static variables
    link = "https://www.nasa.gov/image-of-the-day/"
    index_list = np.array(['Link', 'Src', 'Date', 'Author', 'Credit', 'Description'])
    months = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    # initiates all vars to 0 and fetches daily image repo html text
    def __init__(self, link):

        self.link = link
        self.src = ''
        self.title = ''
        self.date = None
        self.author = ''
        self.credit = ''
        self.description = ''

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
        self.scrape_title()
        self.scrape_src()
        self.scrape_date()
        self.scrape_author()
        self.scrape_credit()
        self.scrape_description()

        self.date_conversion()

    # scrapes the title of the NasaImage ob
    def scrape_title(self) -> None:
        title = self.html_text.find('h1').text
        if title:
            self.title = title
        else:
            raise Exception(f'Cannot find image title for image: {self.link}')
                
    # scrapes the src of the NasaImage ob
    def scrape_src(self) -> None:
        tag = self.html_text.find('img', class_='attachment-2048x2048 size-2048x2048')
        if tag and 'src' in tag.attrs.keys():
            self.src = tag['src']
        else:
            raise Exception(f'Cannot find image src for image: {self.link}')
        
    # scrapes the date of the NasaImage ob
    def scrape_date(self) -> None:
        date = self.html_text.find('span', class_='heading-12 text-uppercase').text

        if date:
            self.date = date
        else:
            raise Exception(f'Cannot find image date for image: {self.link}')

    # scrapes the author of the NasaImage ob
    def scrape_author(self) -> None:
        authors = self.html_text.find_all('h3', class_='hds-meta-heading heading-14')
        first_run = True

        if authors:
            for author in authors:
                if not first_run:
                    self.author += chr(10)
                self.author += author.text
                first_run = False
        else:
            raise Exception(f'Cannot find article author for image: {self.link}')
            
    # scrapes the credit of the NasaImage ob
    def scrape_credit(self) -> None:

        credit = self.html_text.find_all(string=re.compile(r'[C|c]redit:'))
        credit = self.html_text.find_all('em')

        first_run = True
        colon = False
        last_line = ''

        if credit:
            for line in credit:
                text = line.text.strip()
                if last_line:
                    if last_line[-1] == ':':
                        self.credit += ' '
                        colon = True
                if (not first_run and text and not colon):
                    self.credit += chr(10)

                self.credit += text
                first_run = False
                if text:
                    colon = False
                last_line = text
    
        else:
            credit = self.html_text.find_all('div', class_='hds-credits')

            if credit:
                self.credit += "Image credit: "
                for line in credit:
                    self.credit += line.text.strip()
            else:
                raise Exception(f'Cannot find image credit for image: {self.link}')
        
    # scrapes the description of the NasaImage ob
    def scrape_description(self) -> None:
        description = ''

        time_tag = self.html_text.find('p')
        paragraphs = time_tag.find_all_next('p')
        new_paragraph = False

        for p in paragraphs:
            if new_paragraph:
                description += chr(10)
                new_paragraph = False
            try:
                if not p.find('em'):
                    p['class']
            except Exception as e:
                try:
                    a_text = p.a.text
                    if not a_text == p.text:
                        if not p.text[0:10] == 'Learn more':
                            description += p.text
                            new_paragraph = True
                except Exception as e:
                    description += p.text
                    new_paragraph = True

        if description != '':
            self.description = description
        else:
            raise Exception('Cannot determine image description for image: {self.link}')
        
        print(self.description + '\n\n')
        
    def to_tuple(self) -> tuple:
        return (self.link, self.src, self.title, self.date, self.author, self.credit, self.description)

    def date_conversion(self) -> None:
        if not self.date:
            raise Exception('Trying to convert a NoneType Date for image: {self.link}')
        
        l = self.date.split()

        day = int(l[1].replace(",", ""))
        year = int(l[2])
        month = NasaImage.months[l[0]]

        date_ob = datetime(year, month, day)
        self.date = date_ob.strftime('%F')

if __name__ == '__main__':
    img = NasaImage('https://www.nasa.gov/image-article/nasas-spacex-crew-10-launch/')
    img.image_scrape()
