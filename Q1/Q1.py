import networkx as nx
from pyvis.network import Network

def algoritmo_guloso_coloracao(grafo, ordenacao=None):
    if ordenacao is None:
        ordenacao = sorted(grafo.keys())

    cores = {}
    for vertice in ordenacao:
        cores_vizinhos = {cores.get(vizinho) for vizinho in grafo[vertice] if vizinho in cores}
        cor = 1
        while cor in cores_vizinhos:
            cor += 1
        cores[vertice] = cor
    return cores

def visualizar_grafo_pyvis(grafo_dict, cores=None, filename="grafo_interativo.html", titulo="Grafo Interativo"):
    # Cria um grafo NetworkX
    G = nx.Graph()
    for vertice, vizinhos in grafo_dict.items():
        for vizinho in vizinhos:
            G.add_edge(vertice, vizinho)

    # Cria um objeto Network do Pyvis
    nt = Network(height="800px", width="100%", notebook=True, heading=titulo)
    nt.from_nx(G)

    cores_visuais = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

    if cores:
        # Aplica as cores aos nós se a coloração for fornecida
        for node in nt.nodes:
            node_id = int(node['id'])
            cor_numerica = cores.get(node_id, 0)
            node['color'] = cores_visuais[(cor_numerica - 1) % len(cores_visuais)]
            node['title'] = f"Vértice {node_id}\nCor: {cor_numerica}"
            node['label'] = str(node_id)
    else:
        # Colore todos os nós de cinza se nenhuma coloração for fornecida
        for node in nt.nodes:
            node_id = int(node['id'])
            node['color'] = 'lightgray'
            node['title'] = f"Vértice {node['id']}"
            node['label'] = str(node_id)

    nt.save_graph(filename)
    print(f"Grafo interativo salvo em: '{filename}'")

def imprimir_resultado_coloracao(grafo, cores, nome_estrategia=""):
    if nome_estrategia:
        print(f"\n{'='*50}")
        print(f"COLORAÇÃO USANDO ORDENAÇÃO {nome_estrategia.upper()}")
        print(f"{'='*50}")

    print("\nAtribuição de cores:")
    print("-" * 20)
    for vertice in sorted(cores.keys()):
        print(f"Vértice {vertice:2d} : Cor {cores[vertice]}")

    num_cores = max(cores.values())
    print(f"\nNúmero de cores necessárias: {num_cores}")

    valido = all(cores[v] != cores[vizinho] for v, vizinhos in grafo.items() for vizinho in vizinhos)
    if valido:
        print("A coloração é VÁLIDA!")
    else:
        print("A coloração é INVÁLIDA!")

def main():
    grafo = {
        8: [10, 9, 0], 10: [8, 11, 3], 9: [8, 4, 11], 11: [10, 7, 9],
        0: [8, 1, 3, 4], 3: [10, 2, 7, 0], 4: [9, 0, 5, 7], 7: [11, 4, 6, 3],
        1: [0, 12, 2, 5], 2: [1, 3, 14, 6], 5: [1, 4, 13, 6], 6: [7, 5, 15, 2],
        12: [1, 13, 14], 13: [12, 15, 5], 14: [12, 2, 15], 15: [14, 13, 6]
    }

    print("=" * 60)
    print("ANÁLISE DE COLORAÇÃO DE GRAFOS COM PYVIS")
    print("=" * 60)

    print("\n1. Gerando grafo inicial interativo...")
    visualizar_grafo_pyvis(grafo, 
                           filename="Q1_grafo_inicial_interativo.html", 
                           titulo="Grafo Inicial - Sem Coloracao (Interativo)")

    cores_natural = algoritmo_guloso_coloracao(grafo)
    imprimir_resultado_coloracao(grafo, cores_natural, "natural")

    print("\n2. Gerando grafo final interativo (colorido)...")
    visualizar_grafo_pyvis(grafo, cores=cores_natural, 
                           filename="Q1_grafo_final_colorido_interativo.html", 
                           titulo="Grafo Final - Coloracao Aplicada (Interativo)")

    print("\n" + "="*60)
    print("Execução concluída. Abra os arquivos .html gerados em seu navegador.")
    print("="*60)

if __name__ == "__main__":
    main()
