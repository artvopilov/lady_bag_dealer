from bs4 import BeautifulSoup
import requests


class Scrapper:
    def __init__(self, base_url, items_url):
        self.base_url = base_url
        self.items_url = items_url

    def parse(self, brands):
        item_infos = []

        page_number = 1
        has_items = True

        while has_items:
            url = '{}/?page={}&is_sale=1'.format(self.items_url, page_number)
            if brands:
                url += '&brands=' + brands
            print('Url: {}'.format(url))

            soup_response = self.__get_soap_response(url)
            has_items = self.__parse_page_and_add_infos(soup_response, item_infos)
            print('Item infos size: {}'.format(len(item_infos)))

            page_number += 1

        item_infos.sort(key=lambda x: 1 - x['price'] / x['old_price'], reverse=True)
        return item_infos

    def __parse_page_and_add_infos(self, soup_response, item_infos):
        items = soup_response.find_all('a', class_='products-list-item__link link')
        if len(items) == 0:
            return False

        for item in items:
            brand = item.find('div', class_='products-list-item__brand')
            name = brand.find(text=True, recursive=False).strip()

            prices = item.find('span', class_='price').find_all('span')
            price = float(prices[-2].text.replace(' ', ''))

            if len(prices) < 3:
                # print('{} no discount, price: {}'.format(name, price))
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

    @staticmethod
    def __get_soap_response(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(response.text)
        soup_response = BeautifulSoup(response.text, "html.parser")
        return soup_response

    @staticmethod
    def __add_page_numbers(soup_response, page_numbers_queue):
        max_page_number = page_numbers_queue[-1] if len(page_numbers_queue) > 0 else -1
        page_numbers = soup_response.find('span', class_='paginator__pages').find_all('a')
        print('Page numbers size: {}'.format(len(page_numbers)))

        for page_number_str in page_numbers:
            page_number = int(page_number_str.text)
            if page_number > max_page_number:
                page_numbers_queue.append(page_number)
