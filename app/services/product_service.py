import re
import requests
from bs4 import BeautifulSoup


class Website:
    """Class to model a website url HTML data"""

    def __init__(self, url: str) -> None:
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self) -> BeautifulSoup:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",  # Do Not Track Request Header
            "Connection": "keep-alive",
        }
        res = requests.get(self.url, headers=headers)
        return BeautifulSoup(res.text, "html.parser")


class WebProductData:
    """Class to model the product data given a website object"""

    def __init__(self, website_object: Website) -> None:
        self.web_obj = website_object
        self.product_title = ""
        self.product_price = ""
        self.errors = []
        self.scrap_product_data()

    def scrap_product_data(self) -> None:
        self._get_product_title()
        self._get_product_price()

    def is_valid_price_format(self, price: str) -> bool:
        """Check if given price has a valid format '0,00€', '23,65 €', '10.99$', etc."""
        if not price:
            return False
        pattern = r"^\d+[\.,]?\d*\s?[€$]$"
        return bool(re.match(pattern, price.strip()))

    def _get_prices_from_string(self, price_str: str) -> list:
        """Get a list of prices from a string"""
        prices_str = re.findall(r"\d+,\d{2}", price_str)
        prices = [float(price.replace(",", ".")) for price in prices_str]
        # discard 0.00 prices
        prices = [price for price in prices if price > 0]
        return prices

    def get_float_price_list(self) -> list:
        return self._get_prices_from_string(self.product_price)

    def _get_product_title(self) -> None:
        try:
            self.product_title = self.web_obj.soup.find(
                "span", id="productTitle"
            ).text.strip()
        except Exception as e:
            self.errors.append({"attr": "product_title", "error": e})

    def _get_product_price(self) -> None:
        """get product price"""

        # get default price
        price = self._get_default_product_price(self.web_obj.soup)
        if self.is_valid_price_format(price):
            self.product_price = price

        # get price in book product
        if not self.product_price:
            prices = self._get_book_product_price(self.web_obj.soup)
            valid_prices = set()
            for price in prices:
                if self.is_valid_price_format(price):
                    valid_prices.add(price)
            self.product_price = " | ".join(valid_prices)

        # no prices found
        if not self.product_price:
            self.errors.append({"attr": "product_price", "error": "No price found"})

    def _get_default_product_price(self, soup: BeautifulSoup) -> str:
        price = ""
        try:
            price = soup.find("span", class_="a-offscreen").text.strip()

        except Exception:
            pass

        return price

    def _get_book_product_price(self, soup: BeautifulSoup) -> list:
        # book products can have multiple prices (kindle, printed, etc.)
        prices = []
        try:
            price_elements = soup.find_all(
                "span", class_="a-color-price"
            ) + soup.find_all("span", class_="a-size-base a-color-secondary")

            # concatenate all the price elements
            prices = [p.get_text(strip=True) for p in price_elements]
        except Exception:
            pass

        return prices
