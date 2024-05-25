
ALREADY_SCRAPED_FILENAME = 'data\\scraped.txt'
RESULTS_FILENAME = 'data\\result.csv'

class ScraperBase:
    """
    Base class for scrapers

    site_base_url (str): The base URL of the site to scrape
    current_url (str): The URL currently being scraped
    site_name (str): The name of the site being scraped
    categories_to_scrape (list): The categories to scrape
    """

    def __init__(self, site_base_url):
        self.site_base_url = site_base_url
        self.current_url = None
        self.site_name = ""
        self.categories_to_scrape = []
    
    @staticmethod 
    def check_scraped(url):
        """
        Check if a URL has already been scraped
        """
        with open(ALREADY_SCRAPED_FILENAME, 'r') as f:
            return url in f.read()

    @staticmethod
    def mark_scraped(url):
        """
        Mark a URL as scraped
        """
        with open(ALREADY_SCRAPED_FILENAME, 'a') as f:
            f.write(url + '\n')
    
    def add_line_to_csv(self, data: dict, filename=RESULTS_FILENAME):
        """
        Add a line of data to a CSV file
        """
        data_string = f"{self.site_name}|{data['url'].strip()}|{data['picture_url'].strip()}|{data['name'].strip()}|{data['flowers'].strip()}|{data['price'].strip()}"
        with open(filename, 'a') as f:
            f.write(data_string + '\n')


    