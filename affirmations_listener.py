import os
import json

def affirmation():
  result = ''
  res1 = list(os.popen("curl -s -H 'Accept: application/json' 'https://www.affirmations.dev'"))
  res2 = list(os.popen("curl -s -H 'Accept: application/json' 'https://api.thedogapi.com/v1/images/search'"))

  result += ':green_heart: '
  result += json.loads(res1[0])['affirmation'] 
  result += ' :green_heart: \n'
  result += str(json.loads(res2[0])[0]['url']) + '\n'

# print(result)
  return result
