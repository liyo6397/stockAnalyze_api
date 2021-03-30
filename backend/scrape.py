import urllib.request, json , time, os, difflib, itertools
import pandas as pd
from multiprocessing.dummy import Pool
from datetime import datetime
import requests


try:
    import httplib
except:
    import http.client as httplib

key_stock_dict = {}
headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection":"keep-alive",
        "Host":"www.nasdaq.com",
        "Referer":"http://www.nasdaq.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
}

def check_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        # print("True")
        return True
    except:
        conn.close()
        # print("False")
        return False

def get_historic_price(query_url):

    while not check_internet():
        print("Could not connect, trying again in 5 seconds...")
        time.sleep(5)

    #stock_id = query_url.split("&period")[0].split("symbol=")[1]


    with urllib.request.urlopen(query_url) as url:
        parsed = json.loads(url.read().decode())

    Date = []
    for i in parsed['chart']['result'][0]['timestamp']:
        print(datetime.utcfromtimestamp(int(i)).strftime('%d-%m-%Y'))
        Date.append(datetime.utcfromtimestamp(int(i)).strftime('%d-%m-%Y'))

        if i == 10:
            break

def get_json_data(token, period="1mo", interval="1d"):

    base_url = f"https://query1.finance.yahoo.com/v8/finance/chart/{token}"
    params = {}
    params["range"]=period

    #Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    params["interval"]=interval
    params["events"] = "div,splits"

    data = requests.get(url=base_url, params=params)

    return data.json()

def parse_quote(data):

    timestamps = data['chart']['result'][0]["timestamp"]
    parse_data = data['chart']['result'][0]['indicators']['quote'][0]
    volumes = parse_data["volume"]
    opens = parse_data["open"]
    closes = parse_data["close"]
    lows = parse_data["low"]
    highs = parse_data["high"]

    adjclose = closes
    if "adjclose" in data['chart']['result'][0]['indicators']:
        adjclose = data['chart']['result'][0]['indicators']["adjclose"][0]["adjclose"]

    quotes = pd.DataFrame({"Open": opens,
                            "High": highs,
                            "Low": lows,
                            "Close": closes,
                            "Adj Close": adjclose,
                            "Volume": volumes})

    quotes.index = pd.to_datetime(timestamps, unit="s")
    quotes.sort_index(inplace=True)

    return quotes










