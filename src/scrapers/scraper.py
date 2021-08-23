from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


class Scrapper(ABC):
    def __init__(self, base_url, items_url):
        self.base_url = base_url
        self.items_url = items_url

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def parse_page_and_add_infos(self, soup_response, item_infos):
        pass

    @staticmethod
    def get_soap_response(url):
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError(response.text)
        soup_response = BeautifulSoup(response.text, "html.parser")
        return soup_response
