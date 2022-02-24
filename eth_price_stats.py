import requests
import json
from datetime import datetime
from datetime import timedelta

def fetch_url_res(url):
  response_API = requests.get(url)
  res = json.loads(response_API.text)

  if(str(response_API) == "<Response [200]>"):
    return res

  return 'API Failure'

def diff(curr, prev):
  dec = str(round(curr - prev, 2))
  perc = str(round((((abs(prev - curr))/((prev + curr) / 2)) * 100), 2))
  return dec, perc

def eth_price_stats():

  current_dict = {
    'current_price_url': 'https://api.coinbase.com/v2/prices/ETH-USD/spot', 
    'current_date_url': 'https://api.coinbase.com/v2/time',
  }

  historical_dict = {
    'historical_price_url': 'https://api.coinbase.com/v2/prices/ETH-USD/spot?date=', #YYYY-MM-DD
  }

  current_price = ''
  current_date = ''
  historical_date = ''
  historical_price = ''
  price_diff_dec = ''
  price_diff_perc = ''
  time_ago = '24H'
  coin = 'ETH'
  result = 'API Failure'
  errors = False

  for url in current_dict:
    res = fetch_url_res(current_dict[url])

    if(res == 'API Failure'):
      errors = True
      break

    if(url == 'current_price_url'):
      current_price = res['data']['amount']

    elif(url == 'current_date_url'):
      current_date = res['data']['iso']
      historical_date = datetime.strptime(current_date, '%Y-%m-%dT%H:%M:%S%z') - timedelta(days=1)
      historical_date = str(historical_date)

  if(errors == False):
    for url in historical_dict:
      res = fetch_url_res(historical_dict[url] + historical_date)

      if(res == 'API Failure'):
        errors = True
        break

      if(url == 'historical_price_url'):
        historical_price = res['data']['amount']
        price_diff_dec, price_diff_perc = diff(float(current_price), float(historical_price))

  if(errors ==False):
    result = ''

    if(float(price_diff_dec) > float(0)):

      for i in range(0,10):
        result += ":green_circle: "

      result += '\n**Scheduled ' + coin + ' Stats:**'
      result += '\n:purple_circle: $' + current_price + ' (' + time_ago + ')'
      result += '\n:arrow_up_small:  +' + price_diff_dec + ' (' + price_diff_perc + '%)\n'

      for i in range(0,10):
        result += ":green_circle: "

    else:

      for i in range(0,10):
        result += ":red_circle: "

      result += '\n**Scheduled ' + coin + ' Stats:**'
      result += '\n:purple_circle: $' + current_price + ' (' + time_ago + ')'
      result += '\n:arrow_down_small:  ' + price_diff_dec + ' (' + price_diff_perc + '%)\n'
      
      for i in range(0,10):
        result += ":red_circle: " 


  return '\n' + result + '\n==========================\n'
