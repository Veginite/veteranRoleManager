import cloudscraper
from lxml import etree
from io import StringIO


def scrape_private_leagues(account_name: str) -> list:
    parser = etree.HTMLParser()
    url = 'https://www.pathofexile.com/account/view-profile/' + account_name + '/private-leagues'

    # error handling needs to be implemented here (404, 503)
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)

    html = page.content.decode('utf-8')
    tree = etree.parse(StringIO(html), parser=parser)

    root = tree.getroot()
    return root.findall('.//*[@class="custom-league-list"]/div')