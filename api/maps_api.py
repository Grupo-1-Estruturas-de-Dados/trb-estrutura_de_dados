import requests
import os
from requests.exceptions import HTTPError
from dotenv import load_dotenv

def get_route_distance(origin, destination):
  # Carregar as variáveis do arquivo .env
  load_dotenv()

  # Obter a chave de API
  api_key = 'AIzaSyASrRdd0pScL4yKmyBHl7vgiP2_LHo7vos'

  url = "https://maps.googleapis.com/maps/api/directions/json"
  params = {
    'origin': origin,
    'destination': destination,
    'key': api_key
  }

  try:
    response = requests.get(url, params=params)
    data = response.json()

    if data['routes']:
      distance = data['routes'][0]['legs'][0]['distance']['text'].split()[0]
      distance = distance.replace(',', '')
      duration = data['routes'][0]['legs'][0]['duration']['value']
      return int(distance), duration
    else:
        print('Não foi possível encontrar uma rota.')
  except HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
  except Exception as err:
      print(f"Other error occurred: {err}") 
