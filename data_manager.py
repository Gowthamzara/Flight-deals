import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

REQUEST_TIMEOUT = 30


class DataManager:

    def __init__(self):
        self._user = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        # e.g. https://api.sheety.co/<your_id>/flightDeals/prices
        self._endpoint = os.environ["SHEETY_PRICES_ENDPOINT"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=self._endpoint, auth=self._authorization, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        self.destination_data = response.json()["prices"]
        return self.destination_data

    # ==================== Update the price in the spreadsheet ====================

    def update_lowest_price(self, row_id, new_price):
        new_data = {
            "price": {
                "lowestPrice": new_price
            }
        }
        response = requests.put(
            url=f"{self._endpoint}/{row_id}",
            json=new_data,
            auth=self._authorization,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
