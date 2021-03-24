import requests
import pandas as pd
import numpy as np
import json
import scrape


def get_returns(quotes_df):
    quotes_df['fracChange'] = (quotes_df['Close'] - quotes_df['Open']) / quotes_df['Open']
    frac = np.array(quotes_df['fracChange'])

    return frac

def df_to_NParray(df_col, tolog=False):
    arr = np.array(df_col)
    if tolog:
        arr = np.log(arr)

    return arr


def pack_data(val, signal):

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















