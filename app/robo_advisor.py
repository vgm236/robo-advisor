# app/robo_advisor.py
### IMPORTS AND FORMATS

import requests
import json
import csv

import datetime

import os

from dotenv import load_dotenv

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

import numpy as np

import pandas as pd

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

### INPUTS (get data)

load_dotenv() #loads contents of the .env file into the script's environment

## Asking user for the stock (corrected if error)

stock_symbol = input("Please input a stock symbol (Example MSFT): ")


## Requesting data as a string (json)

api_key = os.environ.get("ALPHAVANTAGE_API_KEY") 

symbol = stock_symbol 

request_url =  f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)

## Defining CSV file

file_name = "prices_" + stock_symbol + ".csv"

save_path = os.path.join(os.path.dirname(__file__), "..", "data", file_name)

## Transforming the string into dictionary


parsed_response = json.loads(response.text)

## Correcting if does not exist
## Defining "Meta Data" variables

try:
    description =  parsed_response["Meta Data"]["1. Information"]
except:
    print("-------------------------")
    print("\n")
    print('Incorrect stock symbol. Please try again')
    print("\n")
    print("-------------------------")
    exit()


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

selected_symbol = stock_symbol

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

## 30-days average (closing, highs and lows)

window_average = 30

close_prices = []

for date_list in dates:
    close_price = tsd[date_list]["4. close"]
    close_prices.append(float(close_price))

#close_prices

close_prices_pand = pd.Series(close_prices)
average_close_prices = (close_prices_pand.rolling(window=window_average).mean())

most_recent_close = average_close_prices[window_average-1]

#high_prices

high_prices_pand = pd.Series(high_prices)
average_high_prices = (high_prices_pand.rolling(window=window_average).mean())

most_recent_high = average_high_prices[window_average-1]

#low_prices

low_prices_pand = pd.Series(low_prices)
average_low_prices = (low_prices_pand.rolling(window=window_average).mean())

most_recent_low = average_low_prices[window_average-1]

## Recommendation definition and printing

# One simple example algorithm would be (in pseudocode): 
# If the stock's latest closing price is less than 20% 
# above its recent low, "Buy", else "Don't Buy".

if close_prices[0] > most_recent_close:
    print("\n")
    print("RECOMMENDATION: BUY!") 
    print("\n")
    print("-------------------------") #Logic defined by you
    print("\n")
    print("RECOMMENDATION REASON: Current price is higher than the last 30 days") #Logic defined by you
    print("\n")
    print("-------------------------")
else:
    print("-------------------------")
    print("\n")
    print("RECOMMENDATION: DON'T BUY!")
    print("\n")
    print("-------------------------")

## Writing data into csv

# Writing data

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

print("WRITING DATA INTO CSV FILE: " + save_path)

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



# PLOTTING CHART

y = close_prices 
x = dates 

#sorting in the correct order

x.reverse()
y.reverse()

# break charts into two

fig, ax = plt.subplots() # enables us to further customize the figure and/or the axes

# CHART GENERATION

plt.plot(x, y) 

plt.title("HISTORICAL CLOSING PRICES " + "(" + stock_symbol + ")") # AXIS TITLES
plt.ylabel('Price in USD') # AXIS TITLES     
plt.xlabel("Dates") # AXIS TITLES
#editing number of ticks in the axis (https://stackoverflow.com/questions/6682784/reducing-number-of-plot-ticks/6682846#6682846)
ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    
plt.tight_layout() # ensures all areas of the chart are visible by default (fixes labels getting cut off)
plt.show()

# Final message

print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")



exit()
