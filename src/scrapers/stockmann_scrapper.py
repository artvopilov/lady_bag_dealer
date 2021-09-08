from .scraper import Scrapper


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

    def parse_page_and_add_infos(self, soup_response, item_infos, page_number):
        items = soup_response.find_all('div', class_='catalog-item js-catalog-item')
        if len(items) == 0:
            return False

        for item in items:
            brand = item.find('a', class_='catalog-item__name')
            name = brand.find('span').find(text=True, recursive=False).strip()

            prices = item.find('a', class_='catalog-item__prices').find_all('span')
            if len(prices) < 2:
                continue

            price = float(''.join(filter(str.isdigit, prices[0].text)))
            old_price = float(''.join(filter(str.isdigit, prices[1].text)))

            link = self.base_url + brand.attrs['href']

            item_info = {
                'name': name,
                'old_price': old_price,
                'price': price,
                'link': link}
            item_infos.append(item_info)

        return True
