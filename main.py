import os
import json
import time
from api import get_route_distance
from dotenv import load_dotenv

# Função para ler o arquivo json e converter em um dicionário
def get_json_data(path):
  try:
    with open(path, 'r') as file:
      # Checa se o arquivo está vazio
      if file.readable() and file.seek(0, 2) == 0:
        return {}
      
      file.seek(0)
      data = json.load(file)
      return {obj["id"]: obj for obj in data}
  except FileNotFoundError:
    print(f'Erro: O arquivo {path} não foi encontrado.')
    return {}
  except json.JSONDecodeError:
    print(f'Erro: O arquivo {path} não é um JSON válido.')
    return {}
  except Exception as e:
    print(f'Ocorreu um erro: {e}')
    return {}


# Funcao para salvar dados no json
def add_data_json(path, data):
  with open(path, 'w') as file:
    json.dump(data,file, indent=4)


# Definindo rota mais próxima para para cada entrega
def define_closest_distance():
  existing_routes = get_json_data(ALL_ROUTES_PATH)
  result = []
  for item in existing_routes.values():
    min_route = min(item["routes"], key=lambda x: x["distance_km"])
    result.append({
      "id": item["id"],
      "order_id": item["order_id"],
      "destination": item["destination"],
      "routes": [min_route]
    })
  return result


# Calcular rota mais proxima entre o CD e o local de entrega do pedido
def calculate_distance():
  print('\nCALCULANDO DISTÂNCIAS...\n')

  distribution_centers = get_json_data(CD_PATH)
  orders = get_json_data(ORDER_PATH)
  existing_routes = get_json_data(ALL_ROUTES_PATH) or {}

  # Inicializa routes_list com as rotas já existentes
  routes_list = list(existing_routes.values())
  closest_route_list = []
  order_id_counter = 1

  # Cria um conjunto com as rotas já calculadas para acesso rápido
  calculated_routes = set(
    (int(route.get('order_id')), int(r.get('distribution_center_id')))
    for route in existing_routes.values()
    for r in route['routes']
  )

  for order in orders.values():
    destination = f'{order.get("destination")}, {order.get("destination_state_code")}'
    
    routes_dict = {
      "id": order_id_counter,
      "order_id": order.get("id"),
      "destination": order.get("destination"),
      "routes": []
    }

    for cd in distribution_centers.values():
      origin = f'{cd.get("cd_name")}, {cd.get("state_code")}'
        
      # Verifica se a rota já foi calculada
      if (int(order.get("id")), int(cd.get("id"))) in calculated_routes:
        print('Rota já calculada para:', order.get("id"), cd.get("id"))
        continue  # Pula para o próximo centro de distribuição

      # Calcula distância e duração para novas rotas
      distance, duration = get_route_distance(origin, destination)

      route = {
        "distribution_center_id": cd.get("id"),
        "distribution_center": cd.get("cd_name"),
        "distance_km": distance,
        "duration_seconds": duration
      }

      routes_dict["routes"].append(route)

    # Adiciona o dicionário de rotas ao routes_list se tiver novas rotas
    if routes_dict["routes"]:
      routes_list.append(routes_dict)

    order_id_counter += 1 

  # Salva os dados de rotas atualizados sem sobrescrever o arquivo original
  add_data_json(ALL_ROUTES_PATH, routes_list)

  # Definindo a menor rota por entrega-cd
  closest_route_list = define_closest_distance()
  add_data_json(CLOSEST_ROUTES, closest_route_list)


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
