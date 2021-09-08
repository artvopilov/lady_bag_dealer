from .scraper import Scrapper


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'application/json'
}


class FarfetchScrapper(Scrapper):
    def __init__(self, base_url, items_url, discount, sort, pages_limit):
        super().__init__(base_url, items_url, HEADERS, pages_limit)
        self.discount = discount
        self.sort = sort
        self.first_page_item_names = []

    def get_current_page_url(self, page_number):
        url = '{}?page={}'.format(self.items_url, page_number)
        if self.discount:
            url += '&discount=' + self.discount
        if self.sort:
            url += '&sort=' + self.sort
        return url

    def parse_page_and_add_infos(self, soup_response, item_infos, page_number):
        items_list = soup_response.find('ul', attrs={'data-testid': 'product-card-list'})
        items = items_list.find_all('li', attrs={'data-testid': 'productCard'})
        if len(items) == 0:
            return False

        page_item_names = []
        current_page_item_infos = []
        for item in items:
            information = item.find('div', attrs={'data-testid': 'information'})

            brand = information.find('p', attrs={'itemprop': 'brand'})
            name = brand.find(text=True, recursive=False).strip()

            prices = item.find('div', attrs={'itemprop': 'offers'})
            price = float(''.join(filter(str.isdigit, prices.find('span', attrs={'data-testid': 'price'}).text)))
            old_price = float(''.join(filter(str.isdigit, prices.find('span', attrs={'data-testid': 'initialPrice'}).text)))
            link = self.base_url + item.find('a', attrs={'itemprop': 'itemListElement'}).attrs['href']

            item_info = {
                'name': name,
                'old_price': old_price,
                'price': price,
                'link': link}
            current_page_item_infos.append(item_info)

            if page_number == 1:
                self.first_page_item_names.append(name)
            page_item_names.append(name)

        if page_number != 1 and self.first_page_item_names == page_item_names:
            return False

        item_infos.extend(current_page_item_infos)
        return True
