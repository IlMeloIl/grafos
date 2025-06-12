import heapq
from pyvis.network import Network

def construir_grafo(cidades, matriz_distancias):
    grafo = {}
    num_cidades = len(cidades)
    for i in range(num_cidades):
        cidade_origem = cidades[i]
        grafo[cidade_origem] = {}
        for j in range(num_cidades):
            if i != j:
                cidade_destino = cidades[j]
                distancia = matriz_distancias[i][j]
                if distancia > 0:
                    grafo[cidade_origem][cidade_destino] = distancia
    return grafo

def dijkstra(grafo, inicio):
    distancias_minimas = {no: float('infinity') for no in grafo}
    distancias_minimas[inicio] = 0
    predecessores = {no: None for no in grafo}
    fila_prioridade = [(0, inicio)]
    
    while fila_prioridade:
        distancia_atual, no_atual = heapq.heappop(fila_prioridade)
        
        if distancia_atual > distancias_minimas[no_atual]:
            continue
            
        for vizinho, peso in grafo[no_atual].items():
            distancia = distancia_atual + peso
            
            if distancia < distancias_minimas[vizinho]:
                distancias_minimas[vizinho] = distancia
                predecessores[vizinho] = no_atual
                heapq.heappush(fila_prioridade, (distancia, vizinho))
                
    return distancias_minimas, predecessores

def visualizar_mapa_pyvis(grafo, caminho=None, filename="mapa.html", titulo="Mapa de Cidades"):
    nt = Network(height="800px", width="100%", notebook=True, heading=titulo)

    nos_caminho = set(caminho) if caminho else set()
    arestas_caminho = set()
    if caminho and len(caminho) > 1:
        for i in range(len(caminho) - 1):
            aresta = tuple(sorted((caminho[i], caminho[i+1])))
            arestas_caminho.add(aresta)

    for cidade in grafo:
        cor_no, tamanho_no = ('#1f78b4', 15)
        if cidade in nos_caminho:
            cor_no, tamanho_no = ('#e63946', 25)
        
        if caminho and cidade == caminho[0]:
            cor_no, tamanho_no = ('#52b788', 30)
            nt.add_node(cidade, label=cidade, color=cor_no, size=tamanho_no, title=f"INÍCIO: {cidade}")
        elif caminho and cidade == caminho[-1]:
            cor_no, tamanho_no = ('#9b5de5', 30)
            nt.add_node(cidade, label=cidade, color=cor_no, size=tamanho_no, title=f"FIM: {cidade}")
        else:
            nt.add_node(cidade, label=cidade, color=cor_no, size=tamanho_no)

    arestas_adicionadas = set()
    for cidade_origem, vizinhos in grafo.items():
        for cidade_destino, distancia in vizinhos.items():
            aresta = tuple(sorted((cidade_origem, cidade_destino)))
            if aresta not in arestas_adicionadas:
                cor_aresta, largura_aresta = ('lightgray', 2)
                if aresta in arestas_caminho:
                    cor_aresta, largura_aresta = ('#e63946', 5)
                nt.add_edge(aresta[0], aresta[1], label=str(distancia), title=f"Distância: {distancia} km", color=cor_aresta, width=largura_aresta)
                arestas_adicionadas.add(aresta)

    options = """
    var options = {
      "configure": {
        "enabled": true,
        "filter": "physics"
      },
      "physics": {
        "stabilization": {
          "enabled": true,
          "iterations": 1000,
          "fit": true
        },
        "barnesHut": {
          "gravitationalConstant": -80000,
          "centralGravity": 0.3,
          "springLength": 250,
          "springConstant": 0.04,
          "damping": 0.09,
          "avoidOverlap": 0.5
        }
      }
    }
    """
    nt.set_options(options)
    
    nt.save_graph(filename)
    print(f"Mapa interativo e estabilizado salvo em: '{filename}'")

def main():
    
    cidades = [
        "Caminha", "V. Castelo", "Leixões", "Aveiro", "F. da Foz", "Nazaré",
        "Peniche", "Cascais", "Lisboa", "Sesimbra", "Setúbal", "Sines",
        "Baleeira", "Lagos", "Portimão", "Vilamoura", "C. Sta. Maria", 
        "Tavira", "VRS. António"
    ]

    matriz_distancias = [
        [0, 12, 43, 75, 105, 138, 156, 201, 206, 221, 223, 249, 302, 315, 322, 342, 356, 373, 384],
        [12, 0, 31, 63, 93, 126, 144, 189, 194, 209, 221, 237, 290, 303, 310, 330, 344, 361, 372],
        [43, 31, 0, 32, 63, 96, 116, 160, 172, 181, 193, 209, 262, 275, 282, 302, 316, 333, 344],
        [75, 63, 32, 0, 31, 64, 85, 129, 141, 150, 162, 178, 231, 244, 251, 271, 285, 302, 313],
        [105, 93, 63, 31, 0, 34, 56, 100, 112, 121, 133, 149, 202, 215, 222, 242, 256, 273, 284],
        [138, 126, 96, 64, 34, 0, 23, 65, 79, 88, 100, 116, 169, 181, 189, 209, 223, 240, 251],
        [156, 144, 116, 85, 56, 23, 0, 45, 57, 66, 78, 94, 147, 160, 167, 187, 201, 218, 229],
        [201, 189, 160, 129, 100, 65, 45, 0, 5, 26, 35, 49, 112, 123, 133, 154, 166, 174, 191],
        [206, 194, 172, 141, 112, 79, 57, 5, 0, 23, 32, 47, 111, 122, 132, 153, 165, 173, 190],
        [221, 209, 181, 150, 121, 88, 66, 26, 23, 0, 10, 32, 92, 107, 112, 130, 142, 158, 170],
        [223, 221, 193, 162, 133, 100, 78, 35, 32, 10, 0, 33, 95, 109, 115, 133, 145, 161, 172],
        [249, 237, 209, 178, 149, 116, 94, 49, 47, 32, 33, 0, 63, 77, 83, 101, 113, 129, 141],
        [302, 290, 262, 231, 202, 169, 147, 112, 111, 92, 95, 63, 0, 14, 20, 39, 50, 66, 76],
        [315, 303, 275, 244, 215, 181, 160, 123, 122, 107, 109, 77, 14, 0, 7, 26, 40, 56, 66],
        [322, 310, 282, 251, 222, 189, 167, 133, 132, 112, 115, 83, 20, 7, 0, 20, 33, 49, 59],
        [342, 330, 302, 271, 242, 209, 187, 154, 153, 130, 133, 101, 39, 26, 20, 0, 15, 31, 41],
        [356, 344, 316, 285, 256, 223, 201, 166, 165, 142, 145, 113, 50, 40, 33, 15, 0, 16, 26],
        [373, 361, 333, 302, 273, 240, 218, 174, 173, 158, 161, 129, 66, 56, 49, 31, 16, 0, 11],
        [384, 372, 344, 313, 284, 251, 229, 191, 190, 170, 172, 141, 76, 66, 59, 41, 26, 11, 0]
    ]
    
    grafo = construir_grafo(cidades, matriz_distancias)
    cidade_inicio = 'Leixões'
    cidade_fim = 'Tavira'

    print("=" * 60)
    print("ENCONTRANDO A MELHOR ROTA (Q4) COM DIJKSTRA E PYVIS")
    print("=" * 60)

    print("\n1. Gerando visualização do mapa completo de Portugal...")
    visualizar_mapa_pyvis(
        grafo, 
        caminho=None, 
        filename="Q4_mapa_completo.html", 
        titulo="Mapa de Estradas de Portugal (Antes da Rota)"
    )

    print(f"\n2. Calculando a melhor rota de '{cidade_inicio}' para '{cidade_fim}'...")
    distancias_minimas, predecessores = dijkstra(grafo, cidade_inicio)
    
    caminho = []
    no_atual = cidade_fim
    if predecessores.get(no_atual) is None and no_atual != cidade_inicio:
        print(f"Não foi possível encontrar uma rota de '{cidade_inicio}' para '{cidade_fim}'.")
    else:
        while no_atual is not None:
            caminho.append(no_atual)
            no_atual = predecessores[no_atual]
        caminho.reverse()

        print("Rota encontrada!")
        print(f"   Distância total: {distancias_minimas[cidade_fim]} km")
        print("   Caminho: " + " -> ".join(caminho))
        
        print("\n3. Gerando visualização do mapa com a rota destacada...")
        visualizar_mapa_pyvis(
            grafo, 
            caminho=caminho, 
            filename="Q4_rota_solucao.html", 
            titulo=f"Melhor Rota: {cidade_inicio} para {cidade_fim}"
        )

    print("\n" + "=" * 60)
    print("Execução concluída. Abra os arquivos .html gerados no seu navegador.")
    print("=" * 60)

if __name__ == "__main__":
    main()