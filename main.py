import os
import json
import time
from api import get_route_distance
from dotenv import load_dotenv

# Função para ler o arquivo json e converter em um dicionário
def get_json_data(path):
  try:
    with open(path, 'r') as file:
      data = json.load(file)
      return {obj["id"]: obj for obj in data}
  except FileNotFoundError:
    print(f'Erro: O arquivo {path} não foi encontrado.')
  except json.JSONDecodeError:
    print('Erro: O arquivo não é um JSON válido.')
  except Exception as e:
    print(f'Ocorreu um erro: {e}')


# Funcao para salvar dados no json
def add_data_json(path, data):
  with open(path, 'w') as file:
    json.dump(data,file, indent=4)


# Definindo rota mais próxima para para cada entrega
def get_closest_route():
  print('\nDEFININDO ROTAS MAIS PRÓXIMAS...\n')

  existing_routes = get_json_data(ALL_ROUTES_PATH)

  for route in existing_routes.values():
    print(route)


# Calcular rota mais proxima entre o CD e o local de entrega do pedido
def calculate_distance():
  print('\nCALCULANDO DISTÂNCIAS...\n')
  
  distribution_centers = get_json_data(CD_PATH)
  orders = get_json_data(ORDER_PATH)
  existing_routes = get_json_data(ALL_ROUTES_PATH)

  routes_list = []

  for order in orders.values():
    destination = f'{order.get("destination")}, { order.get("destination_state_code")}'
    
    for cd in distribution_centers.values():
      origin = f'{cd.get("cd_name")}, { cd.get("state_code")}'

      # Verifica se a distancia da rota ja foi calculada, para economizar na chamada da api
      if any(route for route in existing_routes.values() if 
        int(route['order_id']) == int(order.get("id")) and 
        int(route['distribution_center_id']) == int(cd.get("id"))):
        print(f"Rota já existe para o pedido {order.get('id')} e centro de distribuição {cd.get('cd_name')}...")
        continue

      distance, duration = get_route_distance(origin, destination)
      
      route_id = f"{order.get('id')}_{cd.get('cd_name')}"
      routes_dict = {
        "id": route_id,
        "order_id": order.get("id"),
        "destination": order.get("destination"),
        "distribution_center_id": cd.get("id"),
        "distribution_center": cd.get("cd_name"),
        "distance_km": distance,
        "duration_seconds": duration
      }

      routes_list.append(routes_dict)
      add_data_json(ALL_ROUTES_PATH, routes_list)
  
  get_closest_route()


def main():
  start_time = time.time()
  print('*' * 20)
  print(f'INICIANDO ALGORITMO')
  print('*' * 20)

  calculate_distance()

  end_time = time.time()
  execution_time = (end_time - start_time) / 60
  print(f"Tempo de execução: {execution_time:.2f} minutos")


if __name__ == "__main__":
  load_dotenv()

  # Lendo base de dados
  ORDER_PATH = os.getenv('ORDER_PATH')
  CD_PATH = os.getenv('CD_PATH')
  ALL_ROUTES_PATH = os.getenv('ALL_ROUTES_PATH')
  CLOSEST_ROUTES = os.getenv('CLOSEST_ROUTES')

  main()
