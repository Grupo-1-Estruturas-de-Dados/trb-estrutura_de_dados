import json

def load_trucks_data(path):
    try:
        with open(path, 'r') as file:
            trucks = json.load(file)
        return trucks
    except FileNotFoundError:
        print(f'Erro: O arquivo {path} não foi encontrado.')
        return []
    except json.JSONDecodeError:
        print(f'Erro: O arquivo {path} não é um JSON válido.')
        return []

def allocate_trucks_for_orders(orders, trucks):

    allocations = []

    for order in orders:
        order_weight = order["required_weight"]
        order_hours = order["required_hours"]

        # Seleciona caminhões que atendem aos critérios de peso e horas de operação
        eligible_trucks = [
            truck for truck in trucks
            if truck["max_capacity_weight"] >= order_weight and truck["max_operation_hour"] >= order_hours
        ]

        # Ordena caminhões elegíveis pelo custo por hora para otimizar o custo total
        eligible_trucks.sort(key=lambda t: t["cost_per_hour"])

        if eligible_trucks:
            # Seleciona o caminhão de menor custo que atende aos requisitos
            selected_truck = eligible_trucks[0]
            allocations.append({
                "order_id": order["id"],
                "truck_id": selected_truck["id"],
                "allocated_truck": selected_truck
            })
        else:
            print(f"Nenhum caminhão disponível para o pedido {order['id']} com peso {order_weight}kg e duração {order_hours}h")

    return allocations

trucks = load_trucks_data("trucks.json")

# Exemplo de dados dos pedidos
orders_data = [
    {"id": 1, "required_weight": 200, "required_hours": 10},
    {"id": 2, "required_weight": 320, "required_hours": 15},
    {"id": 3, "required_weight": 180, "required_hours": 8},
    {"id": 4, "required_weight": 450, "required_hours": 12},
    {"id": 5, "required_weight": 150, "required_hours": 20},
]

# Alocar caminhões para os pedidos
allocations = allocate_trucks_for_orders(orders_data, trucks)

# Exibindo alocações
for allocation in allocations:
    print(f"Pedido {allocation['order_id']} -> Caminhão {allocation['truck_id']} (Custo/hora: {allocation['allocated_truck']['cost_per_hour']})")
