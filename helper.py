from lxml import etree
from urllib.parse import urljoin
import requests
def check_isbn(word):
    """
    检查isbn是否合法
    :param word:
    :return:
    """
    isbn_or_key = "key"
    if len(word) == 13 and word.isdigit():
        isbn_or_key = "isbn"
    short_q = word.replace('-', '')
    if "-" in word and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = "isbn"
    return isbn_or_key


def get_search_result(url, proxies=None):
    res = requests.get(url, proxies=proxies)
    html = etree.HTML(res.text)
    search_results = html.xpath('//div[@class="resItemBox resItemBoxBooks exactMatch"]')
    data = []
    for result in search_results:
        title = result.xpath('.//h3/a/text()')[0]
        author = result.xpath('.//div[@class="authors"]/a/text()')[0]
        img = result.xpath(".//td[@class='itemCover']//img/@data-src")
        link = result.xpath('.//h3/a/@href')[0]
        link = urljoin(link, url)
        data.append({
            "title": title,
            "author": author,
            "img": img,
            "url": link
        })
    return data
