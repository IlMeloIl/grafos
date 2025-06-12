from pyvis.network import Network

def dfs_path(grafo, inicio, fim):
    stack = [(inicio, [inicio])]  # A pilha armazena (nó_atual, caminho_até_aqui)
    visitado = set()

    while stack:
        (vertice, caminho) = stack.pop()
        
        if vertice not in visitado:
            if vertice == fim:
                return caminho
            
            visitado.add(vertice)
            
            for vizinho in grafo.get(vertice, []):
                if vizinho not in visitado:
                    stack.append((vizinho, caminho + [vizinho]))
    
    return None # Nenhum caminho encontrado

def visualizar_labirinto_pyvis(grafo, caminho=None, filename="labirinto.html", titulo="Labirinto"):
    nt = Network(height="800px", width="100%", notebook=True, heading=titulo, directed=False)

    # Conjuntos para busca rápida de nós e arestas do caminho
    nos_caminho = set(caminho) if caminho else set()
    arestas_caminho = set()
    if caminho and len(caminho) > 1:
        for i in range(len(caminho) - 1):
            aresta = tuple(sorted((caminho[i], caminho[i+1])))
            arestas_caminho.add(aresta)

    # Adiciona todos os nós ao grafo
    for no in grafo:
        cor_no = '#cccccc'
        tamanho_no = 15
        
        if no in nos_caminho:
            cor_no = '#e63946'  # Vermelho para nós no caminho
            tamanho_no = 25
        
        # Destaques especiais para início e fim
        if caminho and no == caminho[0]:
            cor_no = '#52b788' # Verde para o início
            nt.add_node(no, label=no, color=cor_no, size=30, title=f"INÍCIO: {no}")
        elif caminho and no == caminho[-1]:
            cor_no = '#9b5de5' # Roxo para o fim
            nt.add_node(no, label=no, color=cor_no, size=30, title=f"FIM: {no}")
        else:
            nt.add_node(no, label=no, color=cor_no, size=tamanho_no, title=f"Ponto: {no}")

    # Adiciona todas as arestas
    arestas_adicionadas = set()
    for no, vizinhos in grafo.items():
        for vizinho in vizinhos:
            aresta = tuple(sorted((no, vizinho)))
            if aresta not in arestas_adicionadas:
                cor_aresta = '#cccccc'
                largura_aresta = 2

                if aresta in arestas_caminho:
                    cor_aresta = '#e63946' # Vermelho para arestas do caminho
                    largura_aresta = 5
                
                nt.add_edge(aresta[0], aresta[1], color=cor_aresta, width=largura_aresta)
                arestas_adicionadas.add(aresta)

    nt.save_graph(filename)
    print(f"Grafo interativo salvo em: '{filename}'")

def main():
    
    labirinto = {
        'A': ['1', '4'], '1': ['A', '6'], '2': ['3', '7'], '3': ['2'], '4': ['A', '5', '9'],
        '5': ['4', '19'], '6': ['1', '7'], '7': ['2', '6', '8'], '8': ['7', '15'],
        '9': ['4', '10', '29'], '10': ['9', '16'], '11': ['12'], '12': ['11', '13', '17'],
        '13': ['12'], '14': ['15'], '15': ['8', '14', '21'], '16': ['10', '17'],
        '17': ['12', '16'], '18': ['19', '24'], '19': ['5', '18', '20'], '20': ['19', '27'],
        '21': ['15'], '22': ['23'], '23': ['22', '32'], '24': ['18', '25'], '25': ['24', '34'],
        '26': ['27', '40'], '27': ['20', '26', '28'], '28': ['27', '46'], '29': ['9', '30'],
        '30': ['29', '51'], '31': ['32', '47'], '32': ['23', '31'], '33': ['34', '38'],
        '34': ['25', '33'], '35': ['45'], '36': ['57'], '37': ['38', '41'], '38': ['33', '37'],
        '39': ['40', '43'], '40': ['26', '39'], '41': ['37', '42'], '42': ['41'],
        '43': ['39', '44'], '44': ['43', '49'], '45': ['35', '46'], '46': ['28', '45'],
        '47': ['31', '48', '52'], '48': ['47', '54'], '49': ['44', '50'], '50': ['49', 'B'],
        '51': ['30', '52', '58'], '52': ['47', '51', '59'], '53': ['54', '60'],
        '54': ['48', '53'], '55': ['56', '61'], '56': ['55'], 'B': ['50', '63'],
        '57': ['36', '58'], '58': ['51', '57'], '59': ['52'], '60': ['53', '61'],
        '61': ['55', '60'], '62': ['63'], '63': ['B', '62']
    }
    
    no_inicio = 'A'
    no_fim = 'B'

    print("=" * 60)
    print("RESOLVENDO O LABIRINTO (Q3) COM DFS E PYVIS")
    print("=" * 60)

    print(f"\n1. Gerando visualização do labirinto completo...")
    visualizar_labirinto_pyvis(
        labirinto, 
        caminho=None, 
        filename="Q3_labirinto_completo.html", 
        titulo="Labirinto Completo (Antes da Solucao)"
    )

    print(f"\n2. Procurando caminho de '{no_inicio}' para '{no_fim}' usando DFS...")
    caminho_solucao = dfs_path(labirinto, no_inicio, no_fim)

    if caminho_solucao:
        print(f"Caminho encontrado!")
        print("   Rota: " + " -> ".join(caminho_solucao))
        
        print(f"\n3. Gerando visualização do labirinto com a solução destacada...")
        visualizar_labirinto_pyvis(
            labirinto, 
            caminho=caminho_solucao, 
            filename="Q3_labirinto_solucao.html", 
            titulo="Solucao do Labirinto (DFS)"
        )
    else:
        print(f"Não foi possível encontrar um caminho de '{no_inicio}' para '{no_fim}'.")

    print("\n" + "=" * 60)
    print("Execução concluída. Abra os arquivos .html gerados no seu navegador.")
    print("=" * 60)

if __name__ == "__main__":
    main()