import os
import requests_cache
from datetime import datetime, timedelta
from dotenv import load_dotenv
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

load_dotenv()

# ==================== Settings (override in .env if you like) ====================
ORIGIN_CITY_IATA = os.getenv("ORIGIN_CITY_IATA", "LHR")        # London Heathrow
DAYS_UNTIL_DEPARTURE = int(os.getenv("DAYS_UNTIL_DEPARTURE", "30"))
TRIP_LENGTH_DAYS = int(os.getenv("TRIP_LENGTH_DAYS", "14"))


def current_lowest_price(destination):
    """Sheet value may be blank or text; treat anything non-numeric as 'no price yet'."""
    value = destination.get("lowestPrice")
    return value if isinstance(value, (int, float)) else float("inf")


def main():
    # ==================== Conserve requests and preserve your free plan ====================
    requests_cache.install_cache(
        "flight_cache",
        urls_expire_after={
            "*.sheety.co*": requests_cache.DO_NOT_CACHE,
            "*": 3600,
        }
    )

    # ==================== Talk to Sheety ====================
    data_manager = DataManager()
    sheet_data = data_manager.get_destination_data()

    # ==================== Set the dates ====================
    depart_date = datetime.now() + timedelta(days=DAYS_UNTIL_DEPARTURE)
    return_date = depart_date + timedelta(days=TRIP_LENGTH_DAYS)

    flight_search = FlightSearch()
    notifier = NotificationManager()

    # ==================== Search all the destinations ====================
    for destination in sheet_data:
        city = destination["city"]
        print(f"Getting flights for {city}...")
        flights = flight_search.check_flights(
            ORIGIN_CITY_IATA,
            destination["iataCode"],
            from_time=depart_date,
            to_time=return_date,
        )
        cheapest_flight = find_cheapest_flight(flights, return_date=return_date.strftime("%Y-%m-%d"))
        print(f"{city}: GBP {cheapest_flight.price}")

        if cheapest_flight.price == "N/A":
            continue

        previous_price = current_lowest_price(destination)
        if cheapest_flight.price < previous_price:
            print(f"Lower price flight found to {city}!")
            data_manager.update_lowest_price(destination["id"], cheapest_flight.price)
            notifier.send_deal_alert(city, cheapest_flight, previous_price)


if __name__ == "__main__":
    main()
