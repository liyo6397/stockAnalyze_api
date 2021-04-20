import unittest
import scrape, utils
import model
import numpy as np
import matplotlib.pyplot as plt
import predict
import pymongo
import json

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

        print(data)



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
        token = "GME"
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

        max_std_stock = predict.predict_sp500_state()

        print("The Stock with maximum volatility: ", max_std_stock)

    def test_Preposs(self):

        #NOV, PCAR, PAYC, PSX
        token = 'PCAR'
        num_states = 2
        process = utils.PreProcess(token)
        training_data = process.pack_data()
        last_r, last_c = process.EM_var()

        mus, next_state, sigma = model.hidden_info(training_data, num_states)

        prices = model.Euler_Maruyama(last_c, last_r, mus[next_state], sigma)

        print("State: ", mus)
        print(f"From {min(prices)} to {max(prices)} with volitility: {np.std(prices)}")

    def test_next_day_price(self):

        token = "UI"
        min_price, max_price, std, last_c = predict.next_day_price(token)

        print(f"Compaired to close price from last day {last_c}")
        print(f"From {min_price} to {max_price} ")
        print(f"Volitility: {std}")



    def test_timezone(self):

        result = utils.timezone_adjust()

        print(result)

    def test_get_symbols(self):

        results = utils.get_all_tokens()

        print(results[:5])

    def test_pymongo(self):

        utils.create_MongoDB('all_tokens')

    def test_import_MongoDB(self):

        client = pymongo.MongoClient()
        db = client.stock_database

        print(db['all_tokens'])

    def test_show_similar_tokens(self):

        token='aa'
        token = token.upper()

        results = scrape.show_similiar_tokens(token)
        parsed = json.loads(results)

        print(json.dumps(parsed, indent=4))

    def test_hist_summary(self):

        token='ACY'
        results = scrape.get_hist_summary(token)



        print(json.dumps(results))



















