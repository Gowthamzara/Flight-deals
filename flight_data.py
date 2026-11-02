class FlightData:

    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, stops=0):
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.stops = stops


def find_cheapest_flight(data, return_date):
    """Return the cheapest FlightData from a SerpAPI Google Flights response."""
    if data is None:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    all_flights = data.get("best_flights", []) + data.get("other_flights", [])

    # Skip any itinerary that has no price (or no legs)
    priced_flights = [f for f in all_flights if "price" in f and f.get("flights")]
    if not priced_flights:
        print("No flight data")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A")

    cheapest = min(priced_flights, key=lambda f: f["price"])
    legs = cheapest["flights"]

    return FlightData(
        price=cheapest["price"],
        origin_airport=legs[0]["departure_airport"]["id"],
        destination_airport=legs[-1]["arrival_airport"]["id"],
        out_date=legs[0]["departure_airport"]["time"].split(" ")[0],
        return_date=return_date,
        stops=len(legs) - 1,
    )
