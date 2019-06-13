
from base_classes.base_scraper import BaseScraper


class IssuePage(BaseScraper):
    url_root = 'https://atomicavenue.com/atomic'

    def __init__(self, url_to_scrape):
        super(IssuePage, self).__init__(url_to_scrape)

    def get_current_for_sale(self):
        sellers = []
        condition = ""
        for row in self.dom.find("table").find_all("tr"):
            if row.get("class") and "conditionHeader" in row.get("class"):
                condition = row.text.strip()
            elif row.get("class") and "issueGridRow" in row.get("class"):
                seller = row.find("a")
                sellers.append({
                    "condition": condition,
                    "seller_name": seller.text.strip(),
                    "seller_link": seller.get("href"),
                    "price": row.find_all("td")[2].text,
                    "extra_info": row.find("td", {"class": "issueGridNotes"}).text
                })

        return sellers

    def get_issue_info(self):
        infos = self.dom.find("div", {"id": "issueDetails"}).find_all("p")
        publish_info = self.dom.find("span", {"id": "ctl00_ContentPlaceHolder1_lblNotes"}).find_all("a")[:2]

        info = {
            "extra_info": "",
            "publish_date": publish_info[1].text,
            "publish_date_url": publish_info[1].get("href"),
            "publisher": publish_info[0].text,
            "publisher_url": publish_info[0].get("href")
        }
        for cur_info in infos:
            if cur_info.find("label"):
                key, val = cur_info.text.split(":")
                info[key] = val.strip()
            else:
                info["extra_info"] += cur_info.text + "\n"

        return info

    def next_issue(self):
        split_url = self.url_to_scrape.split("/")

        cur_page = False
        for page in self.dom.find("select", {"id": "ctl00_ContentPlaceHolder1_cboJumpToIssue"}).find_all("option"):
            if cur_page:
                next_page = (page.get("value"), page.text)
                break
            if page.get("value") == split_url[-2]:
                cur_page = True

        next_page = "/".join(split_url[:-2] + [next_page[0], split_url[-1]])
        return IssuePage(next_page)

    def previous_issue(self):
        split_url = self.url_to_scrape.split("/")
        for page in self.dom.find("select", {"id": "ctl00_ContentPlaceHolder1_cboJumpToIssue"}).find_all("option"):
            if page.get("value") == split_url[-2]:
                break

            prev_page = (page.get("value"), page.text)

        prev_page = "/".join(split_url[:-2] + [prev_page[0], split_url[-1]])
        return IssuePage(prev_page)
