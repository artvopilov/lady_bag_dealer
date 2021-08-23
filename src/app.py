from scrapers.lamoda_scrapper import LamodaScrapper
from scrapers.farfetch_scrapper import FarfetchScrapper


LAMODA_BASE_URL = 'https://www.lamoda.ru'
LAMODA_ITEMS_URL = 'https://www.lamoda.ru/c/563/bags-sumki-chehli'
LAMODA_BRANDS = '1123%2C1861%2C6477%2C5584%2C23219%2C5181%2C1887%2C23839%2C2829%2C25690%2C3795%2C32138%2C25812%2C24641%2C4489%2C6202%2C29528%2C25411'
LAMODA_IS_SALE = 1

FARFETCH_BASE_URL = 'https://www.farfetch.com'
FARFETCH_ITEMS_URL = 'https://www.farfetch.com/ru/shopping/women/bags-purses-1/items.aspx'
FARFETCH_DISCOUNT = '0-30|30-50|50-60|60-100'
FARFETCH_SORT = '5'
FARFETCH_PAGE_LIMIT = 30


if __name__ == '__main__':
    print('Started')

    items_on_sale = []

    lamoda_scrapper = LamodaScrapper(LAMODA_BASE_URL, LAMODA_ITEMS_URL, LAMODA_BRANDS, LAMODA_IS_SALE)
    lamoda_items_on_sale = lamoda_scrapper.parse()
    items_on_sale.extend(lamoda_items_on_sale)

    farfetch_scrapper = FarfetchScrapper(FARFETCH_BASE_URL, FARFETCH_ITEMS_URL, FARFETCH_DISCOUNT,
                                         FARFETCH_SORT, FARFETCH_PAGE_LIMIT)
    farfetch_items_on_sale = farfetch_scrapper.parse()
    items_on_sale.extend(farfetch_items_on_sale)

    items_on_sale.sort(key=lambda x: 1 - x['price'] / x['old_price'], reverse=True)
    for item in items_on_sale[:1000]:
        print(item)
