import requests

def unsplash():
  URL = 'https://source.unsplash.com/random'
  res = 'Unsplash Error'

  response_API = requests.get(URL)
  if(str(response_API) == "<Response [200]>"):
    res = response_API.url

  return res
