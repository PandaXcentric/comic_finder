
from comicspriceguide.base_cpg_selenium import BaseCPGSelenium


class SearchComics(BaseCPGSelenium):
    url_root = 'https://comicspriceguide.com/'

    def __init__(self):
        super(SearchComics, self).__init__(self.url_root)

    def search_issues(self, title, issue_num=None):
        search_input = self.browser.find_element_by_id("txtTitle")
        search_input.click()
        search_issue = self.browser.find_element_by_id("txtIssue")

        search_input.send_keys(title)

        if issue_num is not None:
            search_issue.send_keys(str(issue_num))

        self.browser.find_element_by_id("btnMSearch").click()

        if issue_num is None:
            return self.get_comic_series()

        return self.get_comic_issues()


