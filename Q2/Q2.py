import csv
import heapq
from collections import defaultdict
from pyvis.network import Network

def ler_matriz_csv(arquivo):
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            leitor = csv.reader(f)
            linhas = list(leitor)

        if not linhas:
            return [], None

        # Detecta se a primeira linha é um cabeçalho de nomes de vértices
        if linhas[0][0] == '':
            nomes_vertices = linhas[0][1:]
            matriz_dados = [linha[1:] for linha in linhas[1:]]
        else:
            nomes_vertices = [str(i) for i in range(len(linhas))]
            matriz_dados = linhas

        matriz = []
        for linha in matriz_dados:
            linha_numerica = [float(val) if val else 0 for val in linha]
            matriz.append(linha_numerica)

        return matriz, nomes_vertices
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo}' não foi encontrado.")
        return None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None, None

def prim(matriz):
    if not matriz:
        return []

    n = len(matriz)
    grafo = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if matriz[i][j] > 0:
                grafo[i].append((j, matriz[i][j]))

    visitado = [False] * n
    mst = []
    heap = [(0, 0, -1)]

    while heap:
        peso, u, pai = heapq.heappop(heap)
        if visitado[u]:
            continue

        visitado[u] = True
        if pai != -1:
            mst.append((pai, u, peso))

        for v, peso_aresta in grafo[u]:
            if not visitado[v]:
                heapq.heappush(heap, (peso_aresta, v, u))

    return mst

def visualizar_mst_pyvis(matriz, mst_edges, nomes_vertices, filename="mst_interativa.html"):
    n = len(matriz)
    nt = Network(height="800px", width="100%", notebook=True, heading="Arvore Geradora de Custo Minimo (MST)")

    # Cria um conjunto de arestas da MST para busca rápida
    mst_set = set()
    for u, v, _ in mst_edges:
        mst_set.add(tuple(sorted((u, v))))

    # Adiciona os nós
    for i, nome in enumerate(nomes_vertices):
        nt.add_node(i, label=nome, title=f"Vértice {nome}")

    # Adiciona todas as arestas do grafo original, diferenciando as da MST
    for i in range(n):
        for j in range(i + 1, n):
            peso = matriz[i][j]
            if peso > 0:
                is_in_mst = tuple(sorted((i, j))) in mst_set

                if is_in_mst:
                    # Aresta pertence à MST: destaque
                    nt.add_edge(i, j, value=peso, title=f"Peso: {peso} (MST)", color='black', label=str(peso))
                else:
                    # Aresta não pertence à MST: sutil
                    nt.add_edge(i, j, value=peso, title=f"Peso: {peso}", color='white')

    nt.save_graph(filename)
    print(f"\nGrafo interativo com MST destacada salvo em: '{filename}'")

def exibir_mst_console(mst, nomes_vertices):
    print("\n" + "="*50)
    print("ÁRVORE GERADORA DE CUSTO MÍNIMO (MST) - RESULTADOS")
    print("="*50)

    if not mst:
        print("Nenhuma árvore geradora pôde ser encontrada (o grafo pode estar vazio ou desconectado).")
        return

    total_cost = 0
    for u, v, peso in sorted(mst, key=lambda x: x[2]):
        print(f"Aresta: {nomes_vertices[u]:<5} -- {nomes_vertices[v]:<5} | Custo: {peso}")
        total_cost += peso

    print(f"\nCusto Total da MST: {total_cost}")
    print("="*50)

def main():
    csv_filename= input("Digite o caminho para o arquivo CSV: ")
    print(f"Tentando ler o grafo do arquivo: '{csv_filename}'")

    matriz, nomes_vertices = ler_matriz_csv(csv_filename)

    if matriz is None:
        print("\nExecução interrompida devido a erro na leitura do arquivo.")
        return

    mst = prim(matriz)
    exibir_mst_console(mst, nomes_vertices)
    visualizar_mst_pyvis(matriz, mst, nomes_vertices, filename="Q2_mst_interativa.html")

if __name__ == "__main__":
    main()
