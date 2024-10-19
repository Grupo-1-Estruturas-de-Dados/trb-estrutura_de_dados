from api import get_route_distance

def main():
  print(f'INICIANDO ALGORITMO')

  # CD que sairá
  origin = 'São Paulo, SP'

  # Local da order
  destination = 'Rio de Janeiro, RJ'

  get_route_distance(origin, destination)



if __name__ == "__main__":
  main()
