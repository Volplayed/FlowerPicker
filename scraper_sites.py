from bs4 import BeautifulSoup
import requests
import re
import json
from scraper_base import ScraperBase

#url constants

FLOWERS_UA_URL = 'https://flowers.ua/en'


#flowers.ua
class FlowerUaScraper(ScraperBase):
    """
    Scraper for flowers.ua
    """
    
    def __init__(self):
        super().__init__(FLOWERS_UA_URL)
        self.site_name = 'flowers.ua'
        self.categories_to_scrape = [
            'vip',
            'tsvety-lyubimoy',
            'den-rozhdeniya',
            'bukety-tsvetov',
            'sezonnye-zvety',
            'cvety_v_korobke',
            'korziny-tsvetov',
            'rozy',
            'hrizantemy',
            'alstromerii',
            'sbornyy-buket',
            'peonies',
            'hydrangeas',
            'carnations',
            'orhidei',
            'rozy-kustovye',
            'eustomy',
            ]
    
    def scrape_site(self):
        """
        Scrape the site
        """
        print(f"Scraping {self.site_name}")
        #scrape each category
        for category in self.categories_to_scrape:
            print(f"Scraping category {category}")
            category_url = f"{self.site_base_url}/{category}"

            response = requests.get(category_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            #scrape each item in the category
            for item in soup.find_all('div', class_='item'):
                try:
                    item_url = item.find('a')['href']
                    if self.check_scraped(item_url):
                        print(f"Already scraped {item_url}")
                        continue
                    item_response = requests.get(item_url)
                    item_soup = BeautifulSoup(item_response.text, 'html.parser')
                    
                    print(f"Scraping {item_url}")

                    #get the item data
                    item_data = {}
                    item_data['url'] = item_url

                    image_div = item_soup.find('div', attrs={'data-id': 'gallery-image-1'})
                    if not image_div:
                        image_img = item_soup.find('img', attrs={"itemprop": "image"})
                        item_data['picture_url'] = image_img['src']
                    else:
                        image_img = image_div.find('img')
                        if image_img:
                            item_data['picture_url'] = image_img['src']
                        else:
                            item_data['picture_url'] = image_div['data-src']

                    item_data['name'] = item_soup.find('h1', id='product-title').text
                    
                    flowers_span = item_soup.find('span', id='productComposition')

                    #check if composition is found
                    if not flowers_span:
                        print("Composition not found")
                        continue

                    item_data['flowers'] = flowers_span.text


                    price_div = item_soup.find_all('div', class_='price')
                    item_data['price'] = price_div[0].find('div', class_='new').text

                    #add the item data to the CSV
                    self.add_line_to_csv(item_data)

                    #mark the item as scraped
                    self.mark_scraped(item_url)

                    print(f"Scraped {item_url}")
                except:
                    print(f"Error scraping {item_url}")
                    continue

