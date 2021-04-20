import requests
import pandas as pd
import numpy as np
import json
import scrape
import pytz
import datetime
import pymongo

class PreProcess:

    def __init__(self, token, period="1mo"):


        self.data = scrape.get_histPrice_json_data(token, period)
        self.quotes_df = scrape.parse_quote(self.data)
        self.returns = self.get_returns()
        self.volume = self.quotes_df['Volume']


    def get_returns(self):
        self.quotes_df['fracChange'] = (self.quotes_df['Close'] - self.quotes_df['Open']) / self.quotes_df['Open']
        frac = np.array(self.quotes_df['fracChange'])

        return frac

    def EM_var(self):

        last_return = self.returns[-1]
        last_close_v = df_to_NParray(self.quotes_df['Close'], tolog=False)[-1]

        return last_return, last_close_v



    def pack_data(self):

        val = self.returns
        signal = df_to_NParray(self.volume, tolog=True)

        return np.column_stack([val, signal])


def get_means(returns, pred_states, num_states):


    return_states = {}
    mus = np.zeros(num_states)

    for i, state in enumerate(pred_states):
        if state not in return_states:
            return_states[state] = [returns[i]]
        else:
            return_states[state].append(returns[i])

    for key in return_states:
        N = len(return_states[key])
        cumulative = sum(return_states[key])

        mus[key] = cumulative / N

    return mus, return_states

def df_to_NParray(df_col, tolog=False):
    arr = np.array(df_col)
    if tolog:
        arr = np.log(arr)

    return arr

def obv_value(data_frame):

    obv = 0

    close = np.array(data_frame['Close'])
    vol = np.array(data_frame['Volume'])
    N = len(close)

    obvs = []

    for i in range(1,N):
        if close[i] > close[i-1]:
            obv += vol[i]
        elif close[i] < close[i-1]:
            obv -= vol[i]
        else:
            obv = 0

        obvs.append(obv)

    return obvs

def get_sp500_tokens():

    df = pd.read_csv('data/sp500_tokens.csv')

    return df['Symbol'].astype(str).values.tolist()

def df_toFile(tokens, states):

    df = pd.DataFrame({"Token": tokens,
        "State": states})

    df.to_csv('results/states.csv', index=False)

def timezone_adjust():
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    eastern = pytz.timezone('US/Eastern')
    local_dt = utc_now.astimezone(eastern)
    east_dt = local_dt.strftime('%Y-%m-%d %H:%M:%S')

    open_time = str(datetime.date.today())+' '+'08:00:00'
    close_time = str(datetime.date.today()) + ' ' + '16:00:00'

    if east_dt < open_time or east_dt > close_time:
        return True
    else:
        return False

def write_json_file(results, destination_folder, file_name):

    with open(destination_folder+'/'+file_name, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def create_MongoDB(collection_name):

    client = pymongo.MongoClient()
    db = client['stock_database']
    collection = db[str(collection_name)]

    json_results = scrape.get_allSymbols()
    #write_json_file()



    result = collection.insert_many(json_results)

    print(result.inserted_ids)

def get_all_tokens():

    df = pd.read_json('data/stockSymbols.json', orient='records')

    return df['symbol'].astype(str).values.tolist()


































