
from base_classes.base_scraper import BaseScraper


class FirstIssueException(Exception):
    pass

class LastIssueException(Exception):
    pass


class IssuePage(BaseScraper):
    url_root = 'https://comicspriceguide.com'

    def __init__(self, url_to_scrape):
        super(IssuePage, self).__init__(url_to_scrape)

    def get_current_for_sale(self):
        for_sale = []
        for index, child in enumerate(
            self.dom.find("div", {"id": "forsale"}).find("div", {"class": "col-12 row"}).children
        ):
            # for some reason only every other child is actual content, the rest are empty
            if index % 2 == 0:
                continue

            for_sale.append(
                {
                    'seller_profile': self.url_root + child.find("a", {"class": "contributor"}).get('href'),
                    'seller_name': child.find("div", {"class": "m-0 p-0"}).find("a").text,
                    'sale_link': self.url_root + child.find("div", {"class": "m-0 p-0"}).find_all("a")[0].get('href'),
                    'price': child.find_all("span")[0].text,
                    'quality_rating': child.find_all("span")[-1].text
                }
            )

        return for_sale

    def get_current_wanted_by(self):
        wanted_by = []
        for index, child in enumerate(
                self.dom.find("div", {"id": "wantedby"}).find("div", {"class": "col-12 row"}).children):
            if index % 2 == 0:
                continue

            wanted_by.append(
                {
                    'profile': self.url_root + child.find("a", {"class": "contributor"}).get('href'),
                    'name': child.find("div", {"class": "text-left"}).find_all("a")[0].text
                }
            )

        return wanted_by

    def get_issue_credits(self):
        contributors = {}
        for contributor in self.dom.find_all("div", {"class": "issue_row_item"}):
            contributors[contributor.find("div", {"class": "creator_type"}).text.strip()] = \
                [cont.strip() for cont in contributor.find("div", {"class": "fkCreator"}).text.split(',')]

        return contributors

    def get_story_summary(self):
        return self.dom.find("div", {"id": "storyblock-xkvv"}).text

    def next_issue(self):
        try:
            href = self.dom.select("div.float-right a.fkPrevNext")[0].get("href")
            return IssuePage(self.url_root + href)
        except Exception:
            raise LastIssueException("You're on the last issue of the series")

    def previous_issue(self):
        try:
            href = self.dom.select("div.float-left a.fkPrevNext")[0].get("href")
            return IssuePage(self.url_root + href)
        except Exception:
            raise FirstIssueException("You're on the first issue fo this  series")

