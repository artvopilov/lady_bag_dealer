from .scraper import Scrapper
from entities.bag import Bag


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'application/json'
}


class FarfetchScrapper(Scrapper):
    def __init__(self, base_url, items_url, discount, sort, pages_limit):
        super().__init__(base_url, items_url, HEADERS, pages_limit)
        self.discount = discount
        self.sort = sort
        self.first_page_bag_brands = []

    def get_current_page_url(self, page_number):
        url = '{}?page={}'.format(self.items_url, page_number)
        if self.discount:
            url += '&discount=' + self.discount
        if self.sort:
            url += '&sort=' + self.sort
        return url

    def parse_page_and_add_infos(self, soup_response, bags, page_number):
        items = soup_response.find_all('div', attrs={'data-testid': 'productCard'})
        if len(items) == 0:
            return False

        page_bag_brands = []
        current_page_bags = []
        for item in items:
            information = item.find('div', attrs={'data-testid': 'information'})
            brand = information.find('p', attrs={'itemprop': 'brand'}).find(text=True, recursive=False).strip().lower()
            model = information.find('p', attrs={'itemprop': 'name'}).find(text=True, recursive=False).strip().lower()

            prices = item.find('div', attrs={'itemprop': 'offers'})
            price = float(''.join(filter(
                str.isdigit,
                prices.find('p', attrs={'data-component': 'PriceFinal'}).text)))
            origin_price = float(''.join(filter(
                str.isdigit,
                prices.find('p', attrs={'data-component': 'PriceOriginal'}).text)))

            image_info = item.find('img', attrs={'data-component': 'ProductCardImagePrimary'})
            image_url = image_info.attrs['src'] if 'src' in image_info.attrs else None
            url = self.base_url + item.attrs['itemid']

            bag = Bag(brand, model, None, price, origin_price, image_url, url)
            current_page_bags.append(bag)

            if page_number == 1:
                self.first_page_bag_brands.append(brand)
            page_bag_brands.append(brand)

        if page_number != 1 and self.first_page_bag_brands == page_bag_brands:
            return False

        bags.extend(current_page_bags)
        return True
