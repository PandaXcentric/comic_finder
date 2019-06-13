
from base_classes.base_selenium import BaseSelenium


class PageException(Exception):
    pass


class SeriesPage(BaseSelenium):
    url_root = 'https://atomicavenue.com/atomic'

    def __init__(self, url_to_scrape):
        self.cur_page = 1
        super(SeriesPage, self).__init__(url_to_scrape)

    def get_comic_issues(self):
        items = self.browser.find_elements_by_xpath("//tr[@class='griditem']")
        item_infos = []
        for item in items:
            cells = item.find_elements_by_xpath(".//td")
            info = [text.strip() for text in cells[1].text.split("\n")][1:]
            date_key, date_val = info[0].split(":")
            cover_key, cover_val = info[1].split(":")
            nm_key, nm_val = info[2].split(":")
            item_infos.append({
                "issue_url": cells[0].find_element_by_xpath(".//a").get_attribute('href'),
                date_key: date_val.strip(),
                cover_key: cover_val.strip(),
                nm_key: nm_val.strip(),
                "issue_availability": info[3],
                "extra_info": cells[2].text.strip(),
                "writer": cells[3].text,
                "artist": cells[4].text
            })

        return item_infos

    def _goto_page(self, page_num):
        pages = self.browser.find_elements_by_xpath("//td[@colspan=5]")[0].find_elements_by_xpath(".//a")
        if page_num < 1:
            self.cur_page = 1
            raise PageException("On First Page")
        elif page_num > int(pages[-1].text):
            self.cur_page -= 1
            raise PageException("On Last Page")

        for page in pages:
            if page.text == str(page_num):
                page.click()
                break

    def next_page(self):
        try:
            self.cur_page += 1
            self._goto_page(self.cur_page)
        except PageException as e:
            raise e

    def previous_page(self):
        try:
            self.cur_page -= 1
            self._goto_page(self.cur_page)
        except PageException as e:
            raise e
