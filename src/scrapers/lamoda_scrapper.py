from .scraper import Scrapper


class LamodaScrapper(Scrapper):
    def __init__(self, base_url, items_url, brands, is_sale):
        super().__init__(base_url, items_url)
        self.brands = brands
        self.is_sale = is_sale

    def parse(self):
        item_infos = []

        page_number = 1
        has_items = True

        while has_items:
            url = '{}/?page={}&is_sale={}'.format(self.items_url, page_number, self.is_sale)
            if self.brands:
                url += '&brands=' + self.brands
            print('Url: {}'.format(url))

            soup_response = self.get_soap_response(url)
            has_items = self.parse_page_and_add_infos(soup_response, item_infos)
            print('Item infos size: {}'.format(len(item_infos)))

            page_number += 1

        return item_infos

    def parse_page_and_add_infos(self, soup_response, item_infos):
        items = soup_response.find_all('a', class_='products-list-item__link link')
        if len(items) == 0:
            return False

        for item in items:
            brand = item.find('div', class_='products-list-item__brand')
            name = brand.find(text=True, recursive=False).strip()

            prices = item.find('span', class_='price').find_all('span')
            price = float(prices[-2].text.replace(' ', ''))

            if len(prices) < 3:
                continue

            old_price = float(prices[0].text.replace(' ', ''))
            link = self.base_url + item.attrs['href']

            item_info = {
                'name': name,
                'old_price': old_price,
                'price': price,
                'link': link}
            item_infos.append(item_info)

        return True
