import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('MINER')

def check_ping(message):
  if(message.find(':sleeping:') == -1):
    return 'slient', message
  else:
    return 'ping', message


def eth_to_usd(eth):
  URL='https://api.coinbase.com/v2/prices/ETC-USD/spot'
  result = ''

  response_API = requests.get(URL)

  if(str(response_API) == "<Response [200]>"):
    res = json.loads(response_API.text)
    amount = res['data']['amount']
    result = float(amount) * float(eth)
    result = str(round(result, 2))

  else:
    result = '\nExchange API Failure\n'

  return result


def genesis_status():
  URL = 'https://api-etc.ethermine.org/miner/' + TOKEN + '/dashboard'
  result = ''

  response_API = requests.get(URL)

  if(str(response_API) == "<Response [200]>"):
    res = json.loads(response_API.text)

    if(res['status'] == 'OK'):
      currentStats = res['data']['currentStatistics']

      worker = "Genesis"
      status = currentStats['activeWorkers']
      time = currentStats['time']
      lastSeen = currentStats['lastSeen']
      reportedHashrate = currentStats['reportedHashrate']
      currentHashrate = currentStats['currentHashrate']
      validShares = currentStats['validShares']
      invalidShares = currentStats['invalidShares']
      staleShares = currentStats['staleShares']
      unpaid = currentStats['unpaid']

      if(str(round(reportedHashrate * (10 ** -6), 1)) == '0.0'):
        status = ":sleeping: :sleeping: :sleeping: "
      else:
        status = ":money_with_wings: :money_with_wings: :money_with_wings: "

      for i in range(0,10):
        result += ":pick: "

      result += "\n**Scheduled " + worker + " Stats:**\n"
      result += "Status: " + status + "\n"
      result += "Active Test: " + str(currentStats['activeWorkers']) + "\n"
      result += "Time Stamp: " + str(datetime.fromtimestamp(time).strftime("%m/%d/%Y, %H:%M:%S")) + "\n"
      result += "Last Seen: " + str(datetime.fromtimestamp(lastSeen).strftime("%m/%d/%Y, %H:%M:%S")) + "\n"
      result += "Reported Hashrate: " + str(round(reportedHashrate * (10 ** -6), 1)) + " MH/S" + "\n"
      result += "**Current Hashrate: " + str(round(currentHashrate * (10 ** -6), 1)) + " MH/S" + "**\n"
      result += "Valid Shares: " + str(validShares) + "\n"
      result += "Invalid Shares: " + str(invalidShares) + "\n"
      result += "Stale Shares: " + str(staleShares) + "\n"
      result += "Unpaid Balance: " + str(round((unpaid * (10 ** -18)), 5)) + " ETC\n" 
      result += "**Unpaid Balance: $" + eth_to_usd(str((unpaid * (10 ** -18)))) + " USD**\n" 

      for i in range(0,10):
        result += ":pick: "
    
      return '\n' + result + '\n==========================\n'  

    else:
      return '\nEthermine Fetch Failed\n'
  else:
    return '\nEthermine Fetch Failed\n'
