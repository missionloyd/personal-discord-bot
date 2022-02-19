import requests
import json

URL='https://api.coinbase.com/v2/prices/ETH-USD/spot'
result = ''
eth = '0.01372'

response_API = requests.get(URL)

if(str(response_API) == "<Response [200]>"):
  res = json.loads(response_API.text)
  amount = res['data']['amount']
  result = float(amount) * float(eth)

else:
  result = '\nExchange API Failure\n'

print(result)
