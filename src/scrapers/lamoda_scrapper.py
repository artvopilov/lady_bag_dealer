from .scraper import Scrapper
from entities.bag import Bag


class LamodaScrapper(Scrapper):
    def __init__(self, base_url, items_url, brands, is_sale):
        super().__init__(base_url, items_url, None, None)
        self.brands = brands
        self.is_sale = is_sale

    def get_current_page_url(self, page_number):
        url = '{}/?page={}&is_sale={}'.format(self.items_url, page_number, self.is_sale)
        if self.brands:
            url += '&brands=' + self.brands
        return url

    def parse_page_and_add_infos(self, soup_response, bags, page_number):
        items = soup_response.find_all('a', class_='products-list-item__link link')
        if len(items) == 0:
            return False

        for item in items:
            item_info = item.find('div', attrs={'data-category': 'Сумки'})

            brand = item_info.attrs['data-brand'].lower()
            color = item_info.attrs['data-color-family'].lower()
            price = float(item_info.attrs['data-price'])
            origin_price = float(item_info.attrs['data-price-origin'])

            image_url_list = item_info.attrs['data-image'].split('/')
            image_url_list[3] = 'img600x866'
            image_url = 'https:' + '/'.join(image_url_list)

            url = self.base_url + item.attrs['href']

            bag = Bag(brand, None, color, price, origin_price, image_url, url)
            bags.append(bag)

        return True
