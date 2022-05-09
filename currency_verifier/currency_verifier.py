import sys
from dateutil import parser
import requests

# Taking the data from the command line arguments
currency_dated = sys.argv[1:]

# Checking for too much data 
if len(currency_dated) > 2:
    print("Zbyt dużo danych.")
    sys.exit(1)

# Asking for the currency if it was not entered
if not currency_dated:
    currency = input("Podaj walutę: ")

# Asking for the date if it was not entered
try:
    currency = currency_dated[0]
    date = currency_dated[1]
except IndexError:
    date = input("Podaj datę: ")
    
currency = currency.upper()

# Converting the date to a format accepted by the NBP's API
try:
    date_parser = parser.parse(date)
    date_no_time = date_parser.strftime("%Y-%m-%d")
except ValueError:
    print("Błędny format daty.")
    sys.exit(2)

url = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/{date_no_time}/?nformat=json"
resp = requests.get(url)

# Checking if there is data to work with in said day and if the currency exists
if resp.status_code == 404:
    print("Brak danych.")
    sys.exit(3)
if not resp.ok:
    print("Niespodziewana odpowiedź serwera.")
    sys.exit(4)

currency_info = resp.json()

# Assigning the value of asked currency
try:
    exchange_rate = currency_info["rates"][0]["mid"]
except (KeyError, ValueError):
    print("Niespodziewana odpowiedź serwera.")
    sys.exit(5)

print(f"1 {currency} = {exchange_rate} PLN w dniu {date_no_time}")