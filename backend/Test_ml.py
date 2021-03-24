import unittest
import scrape, utils
import model as hmmModel
import numpy as np
import matplotlib.pyplot as plt
import predict

class Test_scrape(unittest.TestCase):

    def test_check_internet(self):

        scrape.check_internet()

    def test_get_historical_data(self):
        token = "AAPL"
        data = scrape.get_json_data(token)


        print(data['chart']['result'][0]['indicators']['adjclose'])
        print(data['chart']['result'][0]['indicators']['quote'][0]["close"])

    def test_parse_quote(self):
        token = "AAPL"
        data = scrape.get_json_data(token)

        quotes = scrape.parse_quote(data)

        print(quotes)

    def test_obv(self):
        token = "AAPL"
        data = scrape.get_json_data(token)

        quotes = scrape.parse_quote(data)

        obvs = utils.obv_value(quotes)

        print(obvs)

    def test_model(self):
        # test model before deploy on server
        token = "UWMC"
        data = scrape.get_json_data(token)

        quotes = scrape.parse_quote(data)

        returns = utils.get_returns(quotes)
        vol_df = quotes['Volume']
        volume = utils.df_to_NParray(vol_df,tolog=True)

        num_states = 2
        train_data = utils.pack_data(returns, volume)
        model = hmmModel.train_hmm_model(train_data, num_states)
        past_states = model.predict(train_data)

        state_prob, next_state, = hmmModel.next_hidden_states(model, train_data)
        mus, return_states = utils.get_means(returns, past_states, num_states)

        close_v = utils.df_to_NParray(quotes['Close'],tolog=False)[-1]
        print(close_v)
        last_return = returns[-1]

        sigma = np.std(return_states[next_state])



        prices = hmmModel.Euler_Maruyama(close_v, last_return, mus[next_state], sigma)

        print("State: ", mus)
        print(f"From {min(prices)} to {max(prices)} with volitility: {np.std(prices)}")

    def test_sp_500_tokens(self):

        tokens = utils.get_sp500_tokens()
        data = scrape.get_json_data(tokens[0])

        print("tokens: ",tokens)
        print(data)

    def test_sp500_state(self):

        rise, decrease = predict.predict_sp500_state()

        print("Rising Stock: ", rise)
        print("Lower Performace Stock:", decrease)












