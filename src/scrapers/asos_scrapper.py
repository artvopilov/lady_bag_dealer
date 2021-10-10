from .scraper import Scrapper
from entities.bag import Bag


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Connection': 'keep-alive',
    # 'content-type': 'text/plain',
    # 'Content-Length': '480'
}


class AsosScrapper(Scrapper):
    def __init__(self, base_url, items_url):
        super().__init__(base_url, items_url, HEADERS, None)

    def get_current_page_url(self, page_number):
        url = '{}&page={}'.format(self.items_url, page_number)
        return url

    def parse_page_and_add_infos(self, soup_response, bags, page_number):
        items = soup_response.find_all('article', attrs={'data-auto-id': 'productTile'})
        if len(items) == 0:
            return False

        for item in items:
            item_info = item\
                .find('div', attrs={'data-auto-id': 'productTileDescription'})\
                .find('h2')\
                .find(text=True, recursive=False).strip().split(' ')

            brand = ' '.join(list(filter(lambda word: word[0].isupper(), item_info))).lower()
            color = item_info[0].lower()

            price_info = item.find('span', attrs={'data-auto-id': 'productTileSaleAmount'})
            if not price_info:
                continue
            price = float(''.join(filter(str.isdigit, price_info.text.split(',')[0])))

            origin_price_info = item.find('span', attrs={'data-auto-id': 'productTilePrice'}).find_all('span')
            if len(origin_price_info) < 2:
                continue
            origin_price = float(''.join(filter(str.isdigit, origin_price_info[1].text.split(',')[0])))

            image_info = item.find('img', attrs={'data-auto-id': 'productTileImage'})
            image_url = 'https:' + image_info.attrs['src'] if image_info else None
            url = item.find('a').attrs['href']

            bag = Bag(brand, None, color, price, origin_price, image_url, url)
            bags.append(bag)

        products_progress_bar = soup_response\
            .find('p', attrs={'data-auto-id': 'productsProgressBar'})\
            .find(text=True, recursive=False).strip().split(' ')
        products_progress_bar_pages = list(filter(lambda x: x.isdigit(), products_progress_bar))
        print(products_progress_bar_pages)
        if products_progress_bar_pages[0] == products_progress_bar_pages[1]:
            return False

        return True
