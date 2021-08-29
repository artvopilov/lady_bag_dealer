from .scraper import Scrapper


class FarfetchScrapper(Scrapper):
    def __init__(self, base_url, items_url, discount, sort, pages_limit):
        super().__init__(base_url, items_url, None, pages_limit)
        self.discount = discount
        self.sort = sort

    def get_current_page_url(self, page_number):
        url = '{}?page={}'.format(self.items_url, page_number)
        if self.discount:
            url += '&discount=' + self.discount
        if self.sort:
            url += '&sort=' + self.sort
        return url

    def parse_page_and_add_infos(self, soup_response, item_infos):
        items_list = soup_response.find('ul', attrs={'data-testid': 'product-card-list'})
        items = items_list.find_all('li', attrs={'data-testid': 'productCard'})
        if len(items) == 0:
            return False

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
            item_infos.append(item_info)

        return True
