import requests
import pandas as pd
import numpy as np
import json
import scrape

class PreProcess:

    def __init__(self, token, period="1mo"):

        self.data = scrape.get_json_data(token, period)
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

def get_training_data(token):

    data = scrape.get_json_data(token)
    quotes = scrape.parse_quote(data)
    returns = get_returns(quotes)
    vol_df = quotes['Volume']
    volume = df_to_NParray(vol_df, tolog=True)

    return returns, volume

def df_toFile(tokens, states):

    df = pd.DataFrame({"Token": tokens,
        "State": states})

    df.to_csv('results/states.csv', index=False)



















