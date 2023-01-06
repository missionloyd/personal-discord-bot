import requests
import json
from datetime import datetime, timedelta

def latest_heartbeat(bldgname):
  result = ''
  ts = ''
  ping = False

  for i in range(0,10):
    result += ":leaves: "
  result += "\n**Scheduled Heartbeat Stats:**\n"

  r = requests.get('https://uwyo-campus-heartbeat-api.herokuapp.com/api/latest', timeout=15)

  if r.status_code == 200:

    try:
      res = r.json()
      status = res['status']
      data = res['data']
    except:
      result += "Status: API Error\n"
      ping = True

    if status == 'ok' and len(data) > 0:
      for building in data:
        if building['bldgname'] == bldgname:

          ts = building['ts']
          now = datetime.now()
          date = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
          
          if not now - timedelta(hours=24) <= date <= now:
            ping = True

          result += ":school: " + building['bldgname'] + "\n"
          result += ":timer: " + str(date.strftime('%m/%d/%Y %H:%M:%S')) + "\n"
          result += ":bulb: " + str(round(building['present_elec_kwh'], 2)) + " (kWh)\n"
          result += ":fallen_leaf: " + str(round(building['present_co2_tons'], 2)) + " (Tons)\n"

  else:
    result += "Status: API Error\n"
    ping = True

  for i in range(0,10):
    result += ":leaves: "
  
  result += '\n==========================\n'

  return ping, result

# print(latest_heartbeat('Student Union'))