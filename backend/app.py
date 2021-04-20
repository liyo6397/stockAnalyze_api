from flask import request, Flask, render_template, url_for, redirect, jsonify
import utils, scrape
import predict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/success/<token>')
def success(token):
   return 'welcome %s' % token

def get_obv(token):
   data = scrape.get_json_data(token)
   quotes = scrape.parse_quote(data)

   return utils.obv_value(quotes)

def get_price(token):

   min_price, max_price, std, last_c = predict.next_day_price(token)

   return min_price, max_price, std, last_c

@app.route('/info/<token>')
def info(token=None):

    min_price, max_price, std, last_c = get_price(token)

    return jsonify(min_price=min_price, max_price=max_price, std=std, last_c=last_c)


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['tk']
      return redirect(url_for('info',token = user))
   else:
      user = request.args.get('tk')
      return redirect(url_for('success',token = user))

@app.route('/search', methods =['POST'])
def search():

   req = request.get_json()
   token = req['tk']

   return redirect(url_for('info', token=token))




if __name__ == '__main__':
   app.run(debug = True)
        

