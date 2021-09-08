from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


class Scrapper(ABC):
    def __init__(self, base_url, items_url, headers, pages_limit):
        self.base_url = base_url
        self.items_url = items_url
        self.pages_limit = pages_limit
        self.headers = headers

    def parse(self):
        item_infos = []

        page_number = 1
        has_items = True

        while True:
            url = self.get_current_page_url(page_number)
            print('Url: {}'.format(url))

            soup_response = self.get_soap_response(url, self.headers)
            has_items = self.parse_page_and_add_infos(soup_response, item_infos, page_number)
            print('Item infos size: {}'.format(len(item_infos)))

            if not has_items:
                break

            page_number += 1
            if self.pages_limit and page_number > self.pages_limit:
                break

        return item_infos

    @abstractmethod
    def get_current_page_url(self, page_number):
        pass

    @abstractmethod
    def parse_page_and_add_infos(self, soup_response, item_infos, page_number):
        pass

    @staticmethod
    def get_soap_response(url, headers):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise ConnectionError(response.text)
        soup_response = BeautifulSoup(response.text, "html.parser")
        return soup_response
