from .scraper import Scrapper
from entities.bag import Bag


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'application/json'
}


class StockmannScrapper(Scrapper):
    def __init__(self, base_url, items_url):
        super().__init__(base_url, items_url, HEADERS, None)

    def get_current_page_url(self, page_number):
        url = '{}/?page_list={}'.format(self.items_url, page_number)
        return url

    def parse_page_and_add_infos(self, soup_response, bags, page_number):
        items = soup_response.find_all(lambda tag: tag.name == 'div' and 'data-product-id' in tag.attrs)
        if len(items) == 0:
            return False

        for item in items:
            name_info = item.find('a', class_='catalog-item__name')
            brand = name_info.find('span').find(text=True, recursive=False).strip().lower()
            model = name_info.find('h2').find(text=True, recursive=False).strip().lower()

            prices = item.find('a', class_='catalog-item__prices').find_all('span')
            if len(prices) < 2:
                continue
            price = float(''.join(filter(str.isdigit, prices[0].text)))
            origin_price = float(''.join(filter(str.isdigit, prices[1].text)))

            image_url = self.base_url + item.attrs['data-src']
            url = self.base_url + name_info.attrs['href']

            bag = Bag(brand, model, None, price, origin_price, image_url, url)
            bags.append(bag)

        return True
