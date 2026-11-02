# Flight Deals Finder

A Python script that watches flight prices from London to a list of destinations kept in a Google Sheet. When it finds a fare cheaper than the lowest price recorded so far, it updates the sheet and sends you an email alert.

## How it works

1. Reads your destinations and their lowest known prices from a Google Sheet through [Sheety](https://sheety.co).
2. Searches Google Flights through [SerpAPI](https://serpapi.com) for a return trip to each destination (by default leaving in 30 days and returning 14 days later).
3. Picks the cheapest flight for each destination.
4. If that fare beats the price in the sheet, it writes the new price to the sheet and emails you the details.

Flight search results are cached locally for an hour with `requests-cache`, so running the script again soon after doesn't use up more of your SerpAPI searches.

Example output:

```
Getting flights for Paris...
Paris: GBP 100
Getting flights for Frankfurt...
Frankfurt: GBP 149
Getting flights for Tokyo...
Tokyo: GBP 682
```

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Entry point: runs the search and compares prices |
| `data_manager.py` | Reads and updates the Google Sheet through Sheety |
| `flight_search.py` | Calls the SerpAPI Google Flights search |
| `flight_data.py` | Finds the cheapest flight in a search result |
| `notification_manager.py` | Sends email alerts over SMTP |

## Setup

### 1. Install the dependencies

Requires Python 3.9 or newer.

```bash
pip install -r requirements.txt
```

### 2. Prepare the Google Sheet

Create a sheet named `prices` with these columns:

| city | iataCode | lowestPrice |
|---|---|---|
| Paris | CDG | 54 |
| Frankfurt | FRA | 42 |
| Tokyo | TYO | 485 |

Connect the sheet to [Sheety](https://sheety.co), turn on the GET and PUT methods, and set up Basic authentication.

### 3. Get the API keys

- **SerpAPI:** sign up at [serpapi.com](https://serpapi.com) and copy your API key. The free plan has a limited number of searches per month, and each run uses one search per destination.
- **Email:** for Gmail, create an [App Password](https://myaccount.google.com/apppasswords). Your normal Gmail password won't work.

### 4. Configure your environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `SHEETY_USERNAME` | Yes | Sheety Basic auth username |
| `SHEETY_PASSWORD` | Yes | Sheety Basic auth password |
| `SHEETY_PRICES_ENDPOINT` | Yes | Your Sheety endpoint, e.g. `https://api.sheety.co/<id>/<project>/prices` |
| `SERPAPI_API_KEY` | Yes | Your SerpAPI key |
| `EMAIL_ADDRESS` | Yes | Address that sends the alerts |
| `EMAIL_PASSWORD` | Yes | Password or App Password for that address |
| `ALERT_TO_EMAIL` | No | Where to send alerts (defaults to `EMAIL_ADDRESS`) |
| `SMTP_HOST` / `SMTP_PORT` | No | Mail server (defaults to `smtp.gmail.com` / `587`) |
| `ORIGIN_CITY_IATA` | No | Departure airport (defaults to `LHR`) |
| `DAYS_UNTIL_DEPARTURE` | No | Days from today until departure (defaults to `30`) |
| `TRIP_LENGTH_DAYS` | No | Length of the trip in days (defaults to `14`) |

`.env` is listed in `.gitignore`, so your keys stay out of the repository.

## Usage

```bash
python main.py
```

To check for deals regularly, run the script on a schedule with Windows Task Scheduler or cron.

To force a fresh search within the hour, delete `flight_cache.sqlite`.

## Built with

- [requests](https://requests.readthedocs.io/)
- [requests-cache](https://requests-cache.readthedocs.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [Sheety](https://sheety.co) and [SerpAPI Google Flights](https://serpapi.com/google-flights-api)
