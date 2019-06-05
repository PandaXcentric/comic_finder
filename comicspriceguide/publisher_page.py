
import re

from comicspriceguide.base_cpg_selenium import BaseCPGSelenium


class PublisherPage(BaseCPGSelenium):
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

