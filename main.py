import json
from api import get_route_distance

ORDER_PATH = '/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/order.json'
CD_PATH = '/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/distribution_center.json'

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
  

# Calcular rota mais proxima entre o CD e o local de entrega do pedido
def calculate_route():
  print('\nCALCULANDO ROTAS MAIS PRÓXIMAS...\n')
  
  distribution_centers = get_json_data(CD_PATH)
  orders = get_json_data(ORDER_PATH)
  
  routes_list = []

  for order in orders.values():
    print('ORDER')
    destination = f'{order.get("destination")}, { order.get("destination_state_code")}'
    print(destination)
    
    for cd in distribution_centers.values():
      print('CD')
      origin = f'{cd.get("cd_name")}, { cd.get("state_code")}'
      print(origin)

      distance, duration = get_route_distance(origin, destination)

      routes_dict = {
        "order_id": order.get("id"),
        "destination": order.get("destination"),
        "distribution_center": cd.get("cd_name"),
        "distance_km": distance,
        "duration_seconds": duration
      }

      routes_list.append(routes_dict)
  
  print(routes_list)


def main():
  print('*' * 20)
  print(f'INICIANDO ALGORITMO')
  print('*' * 20)

  calculate_route()


if __name__ == "__main__":
  main()
