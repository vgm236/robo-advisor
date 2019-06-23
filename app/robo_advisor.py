# app/robo_advisor.py

#load_dotenv()
#SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
#MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

### IMPORTS AND FORMATS

import requests
import json
import datetime

def to_usd(my_price):
    return "${0:,.2f}".format(my_price)

### INPUTS (get data)

# Requesting data as a string (json)

request_url =  "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

# Transforming the string into dictionary

parsed_response = json.loads(response.text)

# Defining "Meta Data" variables

description =  parsed_response["Meta Data"]["1. Information"]

ticker =  parsed_response["Meta Data"]["2. Symbol"]

last_refreshed =  parsed_response["Meta Data"]["3. Last Refreshed"]

output_size =  parsed_response["Meta Data"]["4. Output Size"]

time =  parsed_response["Meta Data"]["5. Time Zone"]

# Defining "Time Series" variables

tsd = parsed_response["Time Series (Daily)"]


# Days selection

date_keys = tsd.keys() #transforming days into list - step 1
dates = list(date_keys) #transforming days into list - step 2 (this is weird, but that's how Python works)

latest_day =  dates[0] # select the last day

latest_close = tsd[latest_day]["4. close"]


# Print introduction (with symbol)

print("-------------------------")
print("SELECTED SYMBOL: MSFT")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")

# Print date and time
now = datetime.datetime.now()
print("REQUEST AT:" + now.strftime("%Y-%m-%d %I:%M %p"))
print("-------------------------")

# When date was refreshed
print(f"LATEST DAY: {last_refreshed}") #formatted

print("LATEST CLOSE: " + to_usd(float(latest_close)))



print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


# OUTPUTS



exit()