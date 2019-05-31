
import requests
import traceback
from bs4 import BeautifulSoup

headers = {
    'Content-type': 'text/html',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}


class BaseScraper:

    def __init__(self, url_to_scrape):
        self.url_to_scrape = url_to_scrape
        self.dom = self.get_dom_from_url()

    def get_dom_from_url(self):
        try:
            resp = requests.get(self.url_to_scrape, headers=headers, timeout=2)
            soup = BeautifulSoup(resp.text, 'html')
        except Exception as e:
            traceback.print_exc()
            raise e

        return soup
