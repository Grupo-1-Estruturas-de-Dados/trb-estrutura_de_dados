import os
import json
import time
from api import get_route_distance  # Importa a função para obter distância de rotas
from dotenv import load_dotenv  # Para carregar variáveis de ambiente de um arquivo .env

# Caminhos dos arquivos JSON utilizados no processo
ORDER_PATH='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/order.json'
CD_PATH='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/distribution_center.json'
ALL_ROUTES_PATH='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/all_routes.json'
CLOSEST_ROUTES='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/closest_routes.json'
TRUCKS_PATH='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/trucks.json'
TRUCK_ALLOCATIONS_PATH='/home/guilhermedelrio/Workspace/trb-estrutura_de_dados/data/truck_allocations.json'

# Função para ler dados de um arquivo JSON
def get_json_data(path):
    try:
        with open(path, 'r') as file:
            # Checa se o arquivo está vazio
            if file.readable() and file.seek(0, 2) == 0:
                return {}

            file.seek(0)
            data = json.load(file)  # Carrega o conteúdo do arquivo JSON
            return {obj["id"]: obj for obj in data}  # Retorna um dicionário usando "id" como chave
    except FileNotFoundError:
        print(f'Erro: O arquivo {path} não foi encontrado.')  # Caso o arquivo não seja encontrado
        return {}
    except json.JSONDecodeError:
        print(f'Erro: O arquivo {path} não é um JSON válido.')  # Caso o arquivo tenha erro de formatação JSON
        return {}
    except Exception as e:
        print(f'Ocorreu um erro: {e}')  # Para capturar outros tipos de erro
        return {}

# Função para salvar dados no formato JSON
def add_data_json(path, data):
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)  # Salva o dicionário de dados no arquivo JSON com indentação de 4 espaços

# Função para alocar caminhões para as entregas
def allocate_trucks(orders, trucks):
    print('\nALOCANDO CAMINHÕES PARA AS ENTREGAS...\n')
    allocation = []  # Lista que irá armazenar as alocações de caminhões
    allocated_trucks = set()  # Conjunto para rastrear caminhões já alocados

    # Para cada pedido, tenta alocar um caminhão adequado
    for order in orders.values():
        order_weight = order.get("order_weight")  # Obtém o peso do pedido
        allocated = False  # Flag para verificar se foi alocado

        # Verifica os caminhões disponíveis e sua capacidade
        for truck in trucks.values():
            if truck["id"] not in allocated_trucks and truck["max_capacity_weight"] >= order_weight and truck["max_operation_hour"] >= 1:
                allocation.append({
                    "order_id": order["id"],
                    "truck_id": truck["id"],
                    "allocated_weight": order_weight,
                    "cost": truck["cost_per_hour"]
                })
                truck["max_operation_hour"] -= 1  # Atualiza a hora de operação disponível do caminhão
                allocated_trucks.add(truck["id"])  # Marca o caminhão como alocado
                allocated = True
                break

        if not allocated:
            print(f'Pedido {order["id"]} não pôde ser alocado a um caminhão devido a limitações de capacidade ou operação.')

    add_data_json(TRUCK_ALLOCATIONS_PATH, allocation)  # Salva as alocações de caminhões no arquivo

# Função para definir a rota mais próxima para cada pedido
def define_closest_distance():
    print('\nCALCULANDO ROTA MAIS PROXIMA DE ENTREGA...\n')

    # Carrega as rotas existentes
    existing_routes = get_json_data(ALL_ROUTES_PATH)
    result = []

    # Para cada item de rota, encontra a rota com a menor distância
    for item in existing_routes.values():
        min_route = min(item["routes"], key=lambda x: x["distance_km"])  # Encontra a menor distância
        result.append({
            "id": item["id"],
            "order_id": item["order_id"],
            "destination": item["destination"],
            "routes": [min_route]  # Adiciona a rota mais próxima
        })

    add_data_json(CLOSEST_ROUTES, result)  # Salva as rotas mais próximas no arquivo

# Função para calcular as distâncias entre os centros de distribuição e os destinos dos pedidos
def calculate_distance():
    print('\nCALCULANDO DISTÂNCIAS...\n')

    # Carrega os dados de centros de distribuição, pedidos e rotas existentes
    distribution_centers = get_json_data(CD_PATH)
    orders = get_json_data(ORDER_PATH)
    existing_routes = get_json_data(ALL_ROUTES_PATH) or {}

    # Inicializa a lista de rotas com as rotas já existentes
    routes_list = list(existing_routes.values())
    order_id_counter = 1

    # Cria um conjunto com as rotas já calculadas para evitar duplicação
    calculated_routes = set(
        (int(route.get('order_id')), int(r.get('distribution_center_id')))
        for route in existing_routes.values()
        for r in route['routes']
    )

    # Para cada pedido, calcula as rotas
    for order in orders.values():
        destination = f'{order.get("destination")}, {order.get("destination_state_code")}'  # Destino completo

        routes_dict = {
            "id": order_id_counter,
            "order_id": order.get("id"),
            "destination": order.get("destination"),
            "routes": []
        }

        # Para cada centro de distribuição, calcula a distância e duração
        for cd in distribution_centers.values():
            origin = f'{cd.get("cd_name")}, {cd.get("state_code")}'  # Origem do centro de distribuição

            # Verifica se a rota já foi calculada para esse pedido e centro de distribuição
            if (int(order.get("id")), int(cd.get("id"))) in calculated_routes:
                print(f'Rota já calculada para o pedido {order.get("id")} e CD {cd.get("id")}')
                continue  # Pula para o próximo centro de distribuição

            # Calcula a distância e a duração usando a função externa
            distance, duration = get_route_distance(origin, destination)

            route = {
                "distribution_center_id": cd.get("id"),
                "distribution_center": cd.get("cd_name"),
                "distance_km": distance,
                "duration_seconds": duration
            }

            routes_dict["routes"].append(route)

        # Adiciona o dicionário de rotas à lista se houver novas rotas
        if routes_dict["routes"]:
            routes_list.append(routes_dict)

        order_id_counter += 1

    # Salva os dados de rotas atualizados no arquivo
    add_data_json(ALL_ROUTES_PATH, routes_list)

# Função principal que orquestra o processo
def main():
    start_time = time.time()  # Marca o tempo de início
    print('*' * 20)
    print('INICIANDO ALGORITMO')
    print('*' * 20)

    # Passo 1: Calcular as distâncias entre os CDs e os pedidos
    calculate_distance()

    # Passo 2: Definir a rota mais próxima para cada entrega
    define_closest_distance()

    # Passo 3: Carregar os dados de caminhões e pedidos
    trucks = get_json_data(TRUCKS_PATH)
    orders = get_json_data(ORDER_PATH)

    # Passo 4: Alocar caminhões para as entregas
    allocate_trucks(orders, trucks)

    # Tempo total de execução
    end_time = time.time()
    execution_time = (end_time - start_time) / 60
    print(f"Tempo de execução: {execution_time:.2f} minutos")

# Código para carregar as variáveis de ambiente e executar o programa
if __name__ == "__main__":
    # Executa a função principal
    main()
