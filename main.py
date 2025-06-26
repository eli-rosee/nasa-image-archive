# imports
from bs4 import BeautifulSoup
import requests
import numpy

class DailyImage:
    root = "https://www.nasa.gov/image-article/"

    def __init__(self, link: str):
        self.link = link
        self.image = None
        self.title = None
        self.date = None
        self.author = None
        self.credit = None
        self.description = None

    def __repr__(self) -> str:
        return str(f'Link: {self.link}, Image: {self.image}, Title: {self.title}, Date: {self.date}, Author: {self.author}, Credit: {self.credit}, Description: {self.description}')

    def image_scrape(self) -> None:
        req = requests.get(self.link)
        if req.status_code == 200:
            html_text = BeautifulSoup(req.text, 'lxml')
            self.title = html_text.find('h1').text
            self.date = html_text.find('span', 'heading-12 text-uppercase').text
            self.author = html_text.find('h3', 'hds-meta-heading heading-14').text
            self.credit = html_text.find('div', 'hds-credits').text
            self.description = ''

            bottom_credits = html_text.find('em')
            if bottom_credits:
                parent = bottom_credits.find_parent()
                descriptions = parent.find_all_previous('p',class_=False)
                descriptions.reverse()
                for p in descriptions:
                    self.description += p.text
            else:
                time_tag = html_text.find('p')
                descriptions = time_tag.find_all_next('p')

                for p in descriptions:
                    self.description += p.text

        else:
            raise Exception("Image website not found")

    def none_check(self) -> None:
        if not self.link:
            raise ValueError(f'No link found for {self.title}')
        # if not self.image:
        #     raise ValueError(f'No image found for {self.title}')
        if not self.title:
            raise ValueError(f'No title found for {self.link}')
        if not self.date:
            raise ValueError(f'No date found for {self.title}')
        if not self.author:
            raise ValueError(f'No author found for {self.title}')
        if not self.credit:
            raise ValueError(f'No credit found for {self.title}')
        if not self.description or self.description == '':
            raise ValueError(f'No description found for {self.title}')
        
    # def np_array(self) -> None:




def main():
    link_root = "https://www.nasa.gov/image-of-the-day/"
    req = requests.get(link_root)

    if(req.status_code == 200):
        html_text = BeautifulSoup(req.text, 'lxml')
        images = []
        for tag in html_text.find_all(class_='hds-gallery-item-link', href=True):
            image = DailyImage(tag['href'])
            image.image_scrape()
            images.append(image)

        for image in images:
            image.none_check()
        
    else:
        raise Exception("Nasa Website could not be found")

if __name__ == "__main__":
    main()