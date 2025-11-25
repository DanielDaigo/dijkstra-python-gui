import heapq
import random
from typing import List, Tuple, Dict, Optional

class Grafo:
    """
    Implementação de um Grafo não direcionado ponderado com suporte ao Algoritmo de Dijkstra.
    """

    def __init__(self):
        """
        Inicializa o grafo com uma lista de adjacência vazia.
        A estrutura é um dicionário onde a chave é o vértice e o valor é uma lista de tuplas (vizinho, peso).
        """
        self.adj_list: Dict[int, List[Tuple[int, int]]] = {}

    def adicionar_vertice(self, vertice: int) -> None:
        """
        Adiciona um vértice ao grafo se ele ainda não existir.
        """
        if vertice not in self.adj_list:
            self.adj_list[vertice] = []

    def adicionar_aresta(self, u: int, v: int, peso: int) -> None:
        """
        Adiciona uma aresta ponderada não direcionada entre os vértices u e v.
        
        Args:
            u (int): Primeiro vértice.
            v (int): Segundo vértice.
            peso (int): Peso da aresta (distância).
        """
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        
        # Adiciona a aresta em ambas as direções (grafo não direcionado)
        self.adj_list[u].append((v, peso))
        self.adj_list[v].append((u, peso))

    def gerar_grafo_aleatorio(self, num_vertices: int, probabilidade_conexao: float = 0.5) -> None:
        """
        Gera um grafo aleatório com o número especificado de vértices.
        
        Args:
            num_vertices (int): Número de vértices no grafo.
            probabilidade_conexao (float): Probabilidade (0.0 a 1.0) de existir uma aresta entre dois nós.
        """
        self.adj_list.clear()
        vertices = list(range(num_vertices))
        
        # Garante que todos os vértices existam no grafo, mesmo que isolados
        for v in vertices:
            self.adicionar_vertice(v)

        # Itera sobre todos os pares únicos de vértices
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.random() < probabilidade_conexao:
                    peso = random.randint(1, 50)
                    self.adicionar_aresta(vertices[i], vertices[j], peso)

    def dijkstra(self, origem: int, destino: int) -> Tuple[List[int], float]:
        """
        Executa o Algoritmo de Dijkstra para encontrar o caminho mais curto entre origem e destino.
        
        Args:
            origem (int): Vértice de partida.
            destino (int): Vértice de chegada.
            
        Returns:
            Tuple[List[int], float]: Uma tupla contendo a lista ordenada de vértices do caminho 
                                     e a distância total. Retorna ([], float('inf')) se não houver caminho.
        """
        if origem not in self.adj_list or destino not in self.adj_list:
            return [], float('inf')

        # Inicialização das distâncias com infinito
        distancias = {v: float('inf') for v in self.adj_list}
        distancias[origem] = 0
        
        # Dicionário para reconstruir o caminho (armazena o nó anterior no melhor caminho)
        predecessores: Dict[int, Optional[int]] = {v: None for v in self.adj_list}
        
        # Fila de prioridade (min-heap) armazenando tuplas (distância_acumulada, vértice_atual)
        pq = [(0, origem)]
        
        while pq:
            distancia_atual, u = heapq.heappop(pq)
            
            # Se chegamos ao destino, podemos parar (otimização)
            if u == destino:
                break
            
            # Se a distância retirada da fila for maior que a já conhecida, ignoramos (caminho obsoleto)
            if distancia_atual > distancias[u]:
                continue
            
            # Explora os vizinhos
            for vizinho, peso in self.adj_list[u]:
                nova_distancia = distancia_atual + peso
                
                # Relaxamento da aresta
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = u
                    heapq.heappush(pq, (nova_distancia, vizinho))
        
        # Reconstrução do caminho
        caminho = []
        atual = destino
        
        # Se a distância for infinita, não há caminho
        if distancias[destino] == float('inf'):
            return [], float('inf')
            
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
        
        # O caminho foi reconstruído de trás para frente, então invertemos
        return caminho[::-1], distancias[destino]

    def __str__(self) -> str:
        """
        Retorna uma representação em string da lista de adjacência para debug.
        """
        resultado = ["Lista de Adjacência:"]
        # Ordena as chaves para visualização consistente
        for vertice in sorted(self.adj_list.keys()):
            conexoes = [f"({v}, peso={p})" for v, p in self.adj_list[vertice]]
            resultado.append(f"  {vertice}: {', '.join(conexoes)}")
        return "\n".join(resultado)

# Exemplo de uso (se executado diretamente)
if __name__ == "__main__":
    grafo = Grafo()
    
    print("--- Gerando Grafo Aleatório ---")
    num_vertices = 6
    grafo.gerar_grafo_aleatorio(num_vertices, probabilidade_conexao=0.4)
    print(grafo)
    
    origem = 0
    destino = num_vertices - 1
    
    print(f"\n--- Executando Dijkstra de {origem} para {destino} ---")
    caminho, distancia = grafo.dijkstra(origem, destino)
    
    if caminho:
        print(f"Caminho encontrado: {caminho}")
        print(f"Distância total: {distancia}")
    else:
        print(f"Não existe caminho entre {origem} e {destino}.")
