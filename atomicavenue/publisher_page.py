
from base_classes.base_scraper import BaseScraper


class PageException(Exception):
    pass


class PublisherPage(BaseScraper):
    url_root = 'https://atomicavenue.com'
    publisher_root = '/atomic/SearchTitles.aspx?XT=0&P='

    def __init__(self, publisher='Marvel'):
        self.publisher
        super(PublisherPage, self).__init__(self.publisher_root + publisher)

    def get_series_on_page(self):
        publisher_comics = []
        publisher_titles = self.dom.find_all("li", {"class": "titleSpreadTitle"})

        for title in publisher_titles:
            series_title = title.find("span", {"class": "titleHeader"})
            publisher_comics.append({
                "title": series_title.text,
                "series_link": self.url_root + series_title.find("a").get("href"),
                "publish_year": title.find("span", {"class": "publisherYears"}).text
            })

        return publisher_comics

    def next_page(self):
        next_uri = self.dom.find(
            "div", {"class": "right-graphic tightBottom"}
        ).find("a").get("href")
        if next_uri is None:
            raise PageException("you're on the last page")

        return PublisherPage("{}/atomic/".format(self.url_root, next_uri))

    def prev_page(self):
        prev_a = self.dom.find("div", {"id": "topNextPrev"}).find(
            "a", {"id": "ctl00_ContentPlaceHolder1_topPrevButton"}
        )
        if prev_a is None:
            raise PageException("you're on the first page")

        return PublisherPage("{}/atomic/{}".format(self.url_root, prev_a))

