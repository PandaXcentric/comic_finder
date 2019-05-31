
from base_classes.base_scraper import BaseScraper


class IssuePage(BaseScraper):

    def __init__(self, url_to_scrape):
        super(IssuePage, self).__init__(url_to_scrape)

    def get_current_for_sale(self):
        pass

    def get_current_wanted_by(self):
        pass

    def get_issue_facts(self):
        pass

    def get_story_summary(self):
        pass

