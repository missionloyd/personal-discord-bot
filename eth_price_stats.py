import requests
import json
from datetime import datetime
from datetime import timedelta

current_price = ''
current_date = ''
current_gas = ''
current_gas_eth = ''
historical_date = ''
historical_price = ''
price_diff_dec = ''
price_diff_perc = ''
time_ago = '24H'
coin = 'ETH'
result = 'API Failure'
errors = False

def eth_price_stats():

  current_dict = {
    'current_price_url': 'https://api.coinbase.com/v2/prices/ETH-USD/spot', 
    'current_date_url': 'https://api.coinbase.com/v2/time',
    'current_gas_url': 'https://api.gasprice.io/v1/estimates',
  }

  historical_dict = {
    'historical_price_url': 'https://api.coinbase.com/v2/prices/ETH-USD/spot?date=', #YYYY-MM-DD
  }

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

    elif(url == 'current_gas_url' and res['error'] == None):
      current_gas = res['result']
      current_gas_eth = current_gas['ethPrice']

    else:
      errors = True

  if(errors == False):
    for url in historical_dict:
      res = fetch_url_res(historical_dict[url] + historical_date)

      if(res == 'API Failure'):
        errors = True
        break

      if(url == 'historical_price_url'):
        historical_price = res['data']['amount']
        price_diff_dec, price_diff_perc = diff(float(current_price), float(historical_price))

  if(errors == False):
    result = ''

    if(float(price_diff_dec) > float(0)):
      result = outputView('green')

    else:
      result = outputView('red')

  return '\n' + result + '\n==========================\n'
# print('\n' + result + '\n==========================\n')

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

def gwei2USD(feeCap):
  num = feeCap * current_gas_eth * 0.000000001 * 21000
  return '$' + str(round(num, 2))

def outputView(option):
  output = ''
  borderIcon = ''
  arrowIcon = ''

  if(option == 'green'):
    borderIcon = ":green_circle: "
    arrowIcon = "arrow_up_small:  +"
  else:
    borderIcon = ":red_circle: "
    arrowIcon = "arrow_down_small:  "

  for i in range(0,10):
    output += borderIcon

  output += '\n**Scheduled ' + coin + ' Stats:**\n'
  output += ':purple_circle: $' + current_price + ' (' + time_ago + ')\n'
  output += arrowIcon + price_diff_dec + ' (' + price_diff_perc + '%)\n'
  output += ':fuelpump: ' + str(round(current_gas['instant']['feeCap'], 2)) + ', ' + str(round(current_gas['fast']['feeCap'], 2)) + ', ' + str(round(current_gas['eco']['feeCap'], 2)) + '\n'
  output += ':battery: ' + gwei2USD(current_gas['instant']['feeCap']) + ', ' + gwei2USD(current_gas['fast']['feeCap']) + ', ' + gwei2USD(current_gas['eco']['feeCap']) + '\n'

  for i in range(0,10):
    output += borderIcon

  return output

