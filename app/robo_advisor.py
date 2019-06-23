# app/robo_advisor.py

#load_dotenv()
#SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
#MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

### IMPORTS AND FORMATS

import requests
import json
import datetime
import csv
import os


def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

### INPUTS (get data)

## Requesting data as a string (json)

request_url =  "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

## Transforming the string into dictionary

parsed_response = json.loads(response.text)

## Defining "Meta Data" variables

description =  parsed_response["Meta Data"]["1. Information"]

ticker =  parsed_response["Meta Data"]["2. Symbol"]

last_refreshed =  parsed_response["Meta Data"]["3. Last Refreshed"]

output_size =  parsed_response["Meta Data"]["4. Output Size"]

time =  parsed_response["Meta Data"]["5. Time Zone"]

## Defining "Time Series" variables

tsd = parsed_response["Time Series (Daily)"]

# Days selection

date_keys = tsd.keys() #transforming days into list - step 1
dates = list(date_keys) #transforming days into list - step 2 (this is weird, but that's how Python works)

latest_day =  dates[0] # select the last day

latest_close = tsd[latest_day]["4. close"]

# High prices selection

high_prices = []

for date_list in dates: #for used to create a list
    high_price = tsd[date_list]["2. high"] #then select which factor of the list you want
    high_prices.append(float(high_price)) #finish defining a float of the list selected

recent_high = max(high_prices)

# Low prices selection

low_prices = []

for date_list in dates:
    low_price = tsd[date_list]["3. low"]
    low_prices.append(float(low_price))

recent_low = min(low_prices)

# OUTPUTS

## Print introduction (with symbol)

selected_symbol = "MSFT"

print("-------------------------")
print("SELECTED SYMBOL: " + selected_symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

## Print date and time
now = datetime.datetime.now()
print("REQUEST AT:" + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")

## When date was refreshed
print(f"LATEST DAY: {last_refreshed}") #formatted

print("LATEST CLOSE: " + to_usd(float(latest_close)))

## Highs and Lows printing

print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
print("-------------------------")

## Recommendation definition and printing

print("RECOMMENDATION: BUY!")  #Logic defined by you
print("RECOMMENDATION REASON: TODO") #Logic defined by you

## Writing data into csv

# Writing data

file_name = "prices_" + selected_symbol + ".csv"

save_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

print("-------------------------")
print("WRITING DATA INTO CSV FILE: " + save_path)

# Creating the data

with open(save_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers, lineterminator = '\n')
    writer.writeheader() #uses fieldname set above
    
    #adding dates
    for date in dates:
        daily_prices = tsd[date]  
    #assembling a dictionary
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]})


## Final message

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")






exit()