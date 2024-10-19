import requests
from requests.exceptions import HTTPError

API_KEY = 'xx'

def get_route_distance(origin, destination):
  url = "https://maps.googleapis.com/maps/api/directions/json"
  params = {
    'origin': origin,
    'destination': destination,
    'key': API_KEY
  }

  try:
    response = requests.get(url, params=params)
    data = response.json()

    if data['routes']:
      distance = data['routes'][0]['legs'][0]['distance']['text']
      return distance
    else:
        print('Não foi possível encontrar uma rota.')
  except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except Exception as err:
      print(f"Other error occurred: {err}") 
