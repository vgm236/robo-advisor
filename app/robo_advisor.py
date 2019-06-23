# app/robo_advisor.py

#load_dotenv()
#SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY", "OOPS, please set env var called 'SENDGRID_API_KEY'")
#MY_ADDRESS = os.environ.get("MY_EMAIL_ADDRESS", "OOPS, please set env var called 'MY_EMAIL_ADDRESS'")

import requests
import json


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



print("-------------------------")
print("SELECTED SYMBOL: MSFT")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}") #formatted
print("LATEST CLOSE: $100,000.00")
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