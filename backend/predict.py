import unittest
import scrape, utils
import model as hmmModel
import numpy as np





def next_day_prices(token):

    #get data
    data = scrape.get_json_data(token)
    quotes = scrape.parse_quote(data)
    returns = utils.get_returns(quotes)
    vol_df = quotes['Volume']
    volume = utils.df_to_NParray(vol_df, tolog=True)
    train_data = utils.pack_data(returns, volume)

    #create model
    num_states = 2
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

    tokens = utils.get_sp500_tokens()

    rising = []
    decrease = []

    for token in tokens:
        data = scrape.get_json_data(token)
        try:
            quotes = scrape.parse_quote(data)

            close_v = utils.df_to_NParray(quotes['Close'], tolog=False)[-1]
            min_price, max_price, std = next_day_prices(token)

            if min_price < close_v:
                decrease.append(token)
            else:
                rising.append(token)
        except:
            print("Failed token: ",token)

    return rising, decrease



