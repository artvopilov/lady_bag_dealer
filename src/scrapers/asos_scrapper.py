from .scraper import Scrapper


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.163 Safari/537.36',
    'accept': '*/*'
}


class AsosScrapper(Scrapper):
    def __init__(self, base_url, items_url):
        super().__init__(base_url, items_url, HEADERS, None)

    def get_current_page_url(self, page_number):
        url = '{}&page={}'.format(self.items_url, page_number)
        return url

    def parse_page_and_add_infos(self, soup_response, item_infos, page_number):
        items_list = soup_response.find('div', attrs={'data-auto-id': 'productList'})
        items = items_list.find_all('article', attrs={'data-auto-id': 'productTile'})
        if len(items) == 0:
            return False

        for item in items:
            brand = item.find('div', attrs={'data-auto-id': 'productTileDescription'})
            name = brand.find('p').find(text=True, recursive=False).strip()

            product_price = item.find('span', attrs={'data-auto-id': 'productTileSaleAmount'})
            if not product_price:
                continue
            price = float(''.join(filter(str.isdigit, product_price.text.split(',')[0])))

            old_price_info = item.find('span', attrs={'data-auto-id': 'productTilePrice'}).find_all('span')
            if len(old_price_info) < 2:
                continue
            old_price = float(''.join(filter(str.isdigit, old_price_info[1].text.split(',')[0])))

            link = item.find('a').attrs['href']

            item_info = {
                'name': name,
                'old_price': old_price,
                'price': price,
                'link': link}
            item_infos.append(item_info)

        products_progress_bar = soup_response\
            .find('p', attrs={'data-auto-id': 'productsProgressBar'})\
            .find(text=True, recursive=False).strip().split(' ')
        products_progress_bar_pages = list(filter(lambda x: x.isdigit(), products_progress_bar))
        print(products_progress_bar_pages)
        if products_progress_bar_pages[0] == products_progress_bar_pages[1]:
            return False

        return True
