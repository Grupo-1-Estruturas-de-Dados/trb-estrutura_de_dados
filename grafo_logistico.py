import heapq
import networkx as nx
import matplotlib.pyplot as plt


# Função para encontrar a menor rota logística
def alocar_caminhao(grafo, inicio, destino):
    distancias = {ponto: float('inf') for ponto in grafo}
    distancias[inicio] = 0
    caminho = {ponto: None for ponto in grafo}
    visitados = set()
    fila_prioridade = [(0, inicio)]

    while fila_prioridade:
        custo_atual, ponto_atual = heapq.heappop(fila_prioridade)

        if ponto_atual in visitados:
            continue

        visitados.add(ponto_atual)

        for vizinho, peso_aresta in grafo[ponto_atual].items():
            novo_custo = custo_atual + peso_aresta
            if novo_custo < distancias[vizinho]:
                distancias[vizinho] = novo_custo
                caminho[vizinho] = ponto_atual
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))

    rota = []
    ponto_atual = destino
    while ponto_atual is not None:
        rota.append(ponto_atual)
        ponto_atual = caminho[ponto_atual]

    rota.reverse()

    return distancias, rota


# Exemplo de grafo baseado no projeto
# Cada ponto representa uma localização (depósito ou destino de entrega)
# Pesos são distâncias ou custos logísticos
grafo = {
    'Depósito A': {'Local 1': 100, 'Local 2': 200},
    'Local 1': {'Depósito A': 100, 'Local 3': 150},
    'Local 2': {'Depósito A': 200, 'Local 4': 300},
    'Local 3': {'Local 1': 150, 'Local 5': 120},
    'Local 4': {'Local 2': 300, 'Local 5': 100},
    'Local 5': {'Local 3': 120, 'Local 4': 100},
}

inicio = 'Depósito A'
destino = 'Local 5'
distancias, rota = alocar_caminhao(grafo, inicio, destino)

print(f"Distância mínima de {inicio} a {destino}: {distancias[destino]} km")
print(f"Melhor rota de {inicio} a {destino}: {' -> '.join(rota)}")


# Visualizando o grafo e a rota otimizada
def desenhar_grafo(grafo, rota):
    G = nx.Graph()

    # Adicionar arestas ao grafo
    for ponto, conexoes in grafo.items():
        for vizinho, peso in conexoes.items():
            G.add_edge(ponto, vizinho, weight=peso)

    pos = nx.spring_layout(G, seed=42)  # Layout do grafo
    pesos = nx.get_edge_attributes(G, 'weight')

    # Desenhar o grafo completo
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=pesos, font_size=8)

    # Destacar a rota otimizada
    rota_edges = [(rota[i], rota[i + 1]) for i in range(len(rota) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=rota_edges, edge_color='red', width=2)

    plt.title("Rota Logística Otimizada")
    plt.show()


# Chamar a função de desenho
desenhar_grafo(grafo, rota)
