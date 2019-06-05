
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class BaseSelenium:
    """
    For selenium classes, actions will mutate the the state of the browser.
    Going to the next page for example moves the browser to the next page.
    """

    def __init__(self, url_to_scrape):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.get(url_to_scrape)

        self.action = ActionChains(self.browser)

    def __del__(self):
        self.browser.close()
