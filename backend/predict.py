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


def next_day_prices_old(token, num_states=2):

    #get data
    data = scrape.get_json_data(token)
    quotes = scrape.parse_quote(data)
    returns = utils.get_returns(quotes)
    vol_df = quotes['Volume']
    volume = utils.df_to_NParray(vol_df, tolog=True)
    train_data = utils.pack_data(returns, volume)

    #create model
    model = hmmModel.train_hmm_model(train_data, num_states)

    #predict states
    past_states = model.predict(train_data)
    state_prob, next_state, = hmmModel.next_hidden_states(model, train_data)
    mus, return_states = utils.get_means(returns, past_states, num_states)

    #predict price
    close_v = utils.df_to_NParray(quotes['Close'], tolog=False)[-1]
    last_return = returns[-1]
    sigma = np.std(return_states[next_state])
    prices = hmmModel.Euler_Maruyama(close_v, last_return, mus[next_state], sigma)



    min_price = min(prices)
    max_price = max(prices)
    std = np.std(prices)

    return min_price, max_price, std

def predict_sp500_state():

    all_tokens = utils.get_sp500_tokens()

    states = []
    stds = {}
    tokens = []

    for token in all_tokens:
        try:
            min_price, max_price, std, last_c = next_day_price(str(token))
            stds[token] = std
            tokens.append(token)
            if min_price < last_c:
                states.append("rise")
            else:
                states.append("fall")
        except:
            print("Failed token: ", token)
            print(scrape.get_json_data(token))


    utils.df_toFile(tokens, states)

    return max(stds, key=stds.get)




