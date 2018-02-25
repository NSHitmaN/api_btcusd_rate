import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rate_project.settings")
import django
django.setup()

import time
import datetime
import requests
import simplejson
from rate_app.models import Record

def update_data():
    while True:
        bitstamp_url = "https://www.bitstamp.net/api/ticker/"
        bitstamp_response = requests.get(bitstamp_url)

        bitfinex_url = "https://api.bitfinex.com/v1/pubticker/BTCUSD"
        bitfinex_response = requests.get(bitfinex_url)

        if bitstamp_response.ok and bitfinex_response.ok:
            bitstamp_data = simplejson.loads(bitstamp_response.text)
            bitfinex_data = simplejson.loads(bitfinex_response.text)
            
            avg_bid = (float(bitstamp_data.get("bid")) + float(bitfinex_data.get("bid"))) / 2
            avg_ask = (float(bitstamp_data.get("ask")) + float(bitfinex_data.get("ask"))) / 2
            timestamp = int(time.time() * 1000)
            print(timestamp)
            record = {"avg_ask": avg_ask, "avg_bid": avg_bid, "timestamp": timestamp}
            print(record)
            r = Record()
            r.write_to_db(record)                    
        time.sleep(5)        
        
update_data()
