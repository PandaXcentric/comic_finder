
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class BaseSelenium:

    def __init__(self, url_to_scrape):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(url_to_scrape)

        self.action = ActionChains(self.browser)
