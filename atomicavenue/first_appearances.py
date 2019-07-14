
from base_classes.base_selenium import BaseSelenium


class FirstAppearances(BaseSelenium):
    url_root = "https://atomicavenue.com/atomic/"

    def __init__(self, index_letter=None):
        self.cur_page = 1

        if index_letter is None:
            index_letter = "A"
        self.index_letter = index_letter

        super(FirstAppearances, self).__init__("{}/{}".format(
            self.url_root, "FirstAppearances.aspx?indexLetter={}".format(index_letter)
        ))

    def get_first_appearances(self):
        characters = []
        page_count = len(self.browser.find_elements_by_xpath(
            "//tr[@id='ctl00_ContentPlaceHolder1_IssuesGrid_pager_-4']//td//*"
        ))
        for i in range(1, page_count + 1):
            if i != self.cur_page:
                page = self.browser.find_elements_by_xpath(
                    "//tr[@id='ctl00_ContentPlaceHolder1_IssuesGrid_pager_-4']//td//*"
                )[i - 1]
                self.cur_page = i
                page.click()

            items = self.browser.find_elements_by_xpath("//tr[@class='griditem']")
            for item in items:
                info = item.find_element_by_xpath(".//a")
                characters.append({
                    "name": info.text,
                    "link": info.get_attribute("href")
                })

        return characters
    
    def change_letter(self, new_index_letter="A"):
        """
        :param new_index_letter:  A-Z or #
        :return:
        """
        self.index_letter = new_index_letter
        ele = self.browser.find_element_by_xpath(
            "//a[@class='LetterBrowse'][contains(text(), '{}')]".format(new_index_letter)
        )
        ele.click()

