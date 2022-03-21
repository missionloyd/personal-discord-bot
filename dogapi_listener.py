import os
import json

def dogapi():
  res = list(os.popen("curl -s -H 'Accept: application/json' 'https://api.thedogapi.com/v1/images/search'"))

  return str(json.loads(res[0])[0]['url']) + '\n'

