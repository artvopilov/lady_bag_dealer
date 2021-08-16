from scrapers.scraper import Scrapper


LAMODA_BASE_URL = 'https://www.lamoda.ru'
LAMODA_ITEMS_URL = 'https://www.lamoda.ru/c/563/bags-sumki-chehli'
LAMODA_BRANDS = '1123%2C1861%2C6477%2C5584%2C23219%2C5181%2C1887%2C23839%2C2829%2C25690%2C3795%2C32138%2C25812%2C24641%2C4489%2C6202%2C29528%2C25411'


if __name__ == '__main__':
    print('Started')

    lamoda_scrapper = Scrapper(LAMODA_BASE_URL, LAMODA_ITEMS_URL)
    items_on_sale = lamoda_scrapper.parse(LAMODA_BRANDS)

    for item in items_on_sale:
        print(item)
