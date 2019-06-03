
import re

from base_classes.base_selenium import BaseSelenium


class PublisherPage(BaseSelenium):
    url_root = 'https://comicspriceguide.com/publishers'
    common_publishers = [
        'Marvel', 'DC', 'Image', 'Dark Horse', 'IDW', 'Boom! Studios',
        'Tokyo', 'Pop', 'Titan', 'Dell', 'Fantagraphic', 'Books'
    ]

    def __init__(self, publisher='marvel'):
        pattern = re.compile('[\W_]+')
        publisher = pattern.sub(' ', publisher)
        super(PublisherPage, self).__init__('{}/{}'.format(
            self.url_root, publisher.lower().strip().replace(" ", "-", -1))
        )

    def get_comics(self):
        """
        This only gets the comics on the current page, you'll want to go through all the pages
        to get the full list for a publisher

        :return:
        """

        comic_infos = []

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

    def _click_action(self):
        self.action.click()
        self.action.perform()

    def next_page(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_class_name("repeater-next"), 1, 1)
        self._click_action()

    def previous_page(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_class_name("repeater-prev"), 1, 1)
        self._click_action()

    def popular_titles(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_id("poptitles-tab"), 4, 4)
        self._click_action()

    def new_titles(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_id("newtitles-tab"), 4, 4)
        self._click_action()

    def new_issues(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_id("newissues-tab"), 4, 4)
        self._click_action()

    def top_100(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_id("top100-tab"), 4, 4)
        self._click_action()

    def story_arcs(self):
        self.action.move_to_element_with_offset(self.browser.find_element_by_id("storyarc-tab"), 4, 4)
        self._click_action()

