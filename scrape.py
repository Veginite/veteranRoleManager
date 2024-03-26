import cloudscraper
import requests
from requests import Response
from lxml import etree
from io import StringIO


def scrape_private_leagues(account_name: str) -> list:
    parser = etree.HTMLParser()
    url = 'https://www.pathofexile.com/account/view-profile/' + account_name + '/private-leagues'

    scraper = cloudscraper.create_scraper()
    page: Response
    try:
        page = scraper.get(url)
    except requests.exceptions.RequestException as e:
        print(e)
        return []

    html = page.content.decode('utf-8')
    tree = etree.parse(StringIO(html), parser=parser)

    root = tree.getroot()
    return root.findall('.//*[@class="custom-league-list"]/div')