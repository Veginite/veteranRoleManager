import cloudscraper
from lxml import etree
from io import StringIO
import math
import time
import requests


# further exceptions are available from the cloudscraper library, in relation to CloudFlare

def scrape_private_leagues(account_name: str) -> list:
    parser = etree.HTMLParser()
    url = 'https://www.pathofexile.com/account/view-profile/' + account_name + '/private-leagues'

    scraper = cloudscraper.create_scraper()
    page: requests.Response
    try:
        page = scraper.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return []

    html = page.content.decode('utf-8')
    tree = etree.parse(StringIO(html), parser=parser)

    # if an 'em' tag is present in the document the profile is set to private, abort
    if not is_profile_private(tree):

        pagination_count = get_pagination_count(tree)
        leagues = tree.getroot().findall('.//*[@class="custom-league-list"]/div')
        for n in range(pagination_count - 1):
            time.sleep(20)  # delay the next https request to prevent a potential cloudflare bot flag
            p_url = url + '?page=' + str(n + 2)  # page number is counter index offset by 2
            try:
                page = scraper.get(p_url)
            except requests.exceptions.RequestException as e:
                print(e)
                return []
            html = page.content.decode('utf-8')
            tree = etree.parse(StringIO(html), parser=parser)
            leagues += tree.getroot().findall('.//*[@class="custom-league-list"]/div')

        return leagues

    return []


# used to scrape multiple private league pages
def get_pagination_count(tree: etree) -> int:
    root = tree.getroot()
    e = root.find('.//div[@class="total-count"]')
    return math.ceil(
        int(e.text.split(': ', 1)[1]) / 20)  # the amount of PL pages are the total PL count / 20 rounded up


def is_profile_private(tree: etree) -> bool:
    root = tree.getroot()
    e = root.find('.//em')
    if e is not None:
        return True
    else:
        return False
