import cloudscraper
from lxml import etree
from io import StringIO
import math
import time


def scrape_private_leagues(account_name: str) -> list:
    parser = etree.HTMLParser()
    url = 'https://www.pathofexile.com/account/view-profile/' + account_name + '/private-leagues'

    # error handling needs to be implemented here (404, 503)
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)

    html = page.content.decode('utf-8')
    tree = etree.parse(StringIO(html), parser=parser)

    pagination_count = get_pagination_count(tree)

    leagues = tree.getroot().findall('.//*[@class="custom-league-list"]/div')
    for n in range(pagination_count - 1):
        p_url = url + '?page=' + str(n + 2)  # page number is counter index offset by 2
        page = scraper.get(p_url)
        html = page.content.decode('utf-8')
        tree = etree.parse(StringIO(html), parser=parser)
        leagues += tree.getroot().findall('.//*[@class="custom-league-list"]/div')
        time.sleep(0.25)  # delay the next https request to prevent a potential cloudflare bot flag

    return leagues


# used to scrape multiple private league pages
def get_pagination_count(tree: etree) -> int:
    root = tree.getroot()
    e = root.find('.//div[@class="total-count"]')
    return math.ceil(
        int(e.text.split(': ', 1)[1]) / 20)  # the amount of PL pages are the total PL count / 20 rounded up
