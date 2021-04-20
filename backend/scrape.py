import urllib.request, json , time, os, difflib, itertools
import pandas as pd
from multiprocessing.dummy import Pool
from datetime import datetime
import requests
import utils
from dotenv import load_dotenv
import os



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

def show_similiar_tokens(token):

    df = utils.get_all_tokens()
    token = token.upper()

    # similar token
    token = str(token)

    end = len(token)
    df['index'] = df['displaySymbol'].str.find(token, start=0,end=end)

    df.similar_results = df[["displaySymbol","description"]][df['index'] != -1]

    return df.similar_results.to_json()


def get_histPrice_json_data(token, period="1mo", interval="1d"):


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

    if not utils.timezone_adjust():
        quotes = quotes[:-1]

    return quotes

def get_allSymbols():

    load_dotenv()


    token = os.getenv('FINNHUB_API_KEY')
    base_url = 'https://finnhub.io/api/v1/stock/symbol?'
    params = {'exchange': 'US', 'token': token}

    r = requests.get(base_url, params)

    return r.json()

def get_hist_summary(symbol):
    load_dotenv()

    token = os.getenv('FINNHUB_API_KEY')
    base_url = 'https://finnhub.io/api/v1/stock/metric?'

    params = {'symbol': symbol, 'token': token, 'metric':'price'}

    r = requests.get(base_url, params)

    return r.json()















