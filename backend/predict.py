import unittest
import scrape, utils
import model
import numpy as np



def next_day_price(token, num_states=2):

    #Proprocess data
    process = utils.PreProcess(token)
    training_data = process.pack_data()
    last_r, last_c = process.EM_var()

    #training
    mus, next_state, sigma = model.hidden_info(training_data, num_states)

    #Measure price
    prices = model.Euler_Maruyama(last_c, last_r, mus[next_state], sigma)

    min_price = min(prices)
    max_price = max(prices)
    standard = np.std(prices)

    return min_price, max_price, standard, last_c


def predict_sp500_state():

    all_tokens = utils.get_sp500_tokens()

    states = []
    stds = {}
    tokens = []

    for token in all_tokens:

        min_price, max_price, std, last_c = next_day_price(str(token))
        stds[token] = std
        tokens.append(token)
        if min_price < last_c:
            states.append("rise")
        else:
            states.append("fall")


    utils.df_toFile(tokens, states)

    return max(stds, key=stds.get)




