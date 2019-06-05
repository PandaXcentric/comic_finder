
from base_classes.base_selenium import BaseSelenium
import selenium.webdriver.support.ui as ui


class BaseCPGSelenium(BaseSelenium):

    def __init__(self, url_to_scrape):
        super(BaseCPGSelenium, self).__init__(url_to_scrape)

    def _click_action(self):
        self.action.click()
        self.action.perform()

    def next_page(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_class_name("repeater-next"), 1, 1)
        self._click_action()

    def previous_page(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_class_name("repeater-prev"), 1, 1)
        self._click_action()

    def _wait_for_comic_list(self):
        wait = ui.WebDriverWait(self.browser, 5)
        wait.until(
            lambda driver: len(driver.find_elements_by_xpath("//div[@class='repeater-viewport']//tbody//tr")) > 0
        )

    def get_comic_series(self):
        """
        This only gets the comics on the current page, you'll want to go through all the pages
        to get the full list for a publisher

        The links here will bring you to the series page

        :return:
        """

        comic_infos = []
        self._wait_for_comic_list()
        comics = self.browser.find_elements_by_xpath("//div[@class='repeater-viewport']//tbody//tr")

        for comic in comics:
            extra_info = comic.text.split("\n")[-1]
            comic_infos.append(
                {
                    'title': comic.find_element_by_xpath(".//a[@class='fkTitleLnk grid_title']").text,
                    'series_page': comic.find_element_by_xpath(".//a[@class='fkTitleLnk grid_title']").get_attribute(
                        'href'),
                    'publication_years': extra_info.split("|")[0],
                    'search_volume': extra_info.split("|")[-1]
                }
            )

        return comic_infos

    def get_comic_issues(self):
        """
        The links here will bring to the issues page

        :return:
        """
        comic_infos = []
        self._wait_for_comic_list()
        comics = self.browser.find_elements_by_xpath("//div[@class='repeater-viewport']//tbody//tr")

        for comic in comics:
            try:
                info = comic.find_element_by_class_name("grid_issue_info").find_element_by_xpath(
                    ".//span[@class='d-block isscomments']").text
            except:
                info = ""

            comic_infos.append(
                {
                    'title': comic.find_element_by_xpath(".//a[@class='grid_issue']").text,
                    'issue_page': comic.find_element_by_xpath(".//a[@class='grid_issue']").get_attribute('href'),
                    'issue_info': info
                }
            )

        return comic_infos

