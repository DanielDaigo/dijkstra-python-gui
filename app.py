import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import random
from typing import List, Tuple, Dict, Optional

# --- Classe Grafo (Reutilizada) ---
class Grafo:
    """
    Implementação de um Grafo não direcionado ponderado com suporte ao Algoritmo de Dijkstra.
    """

    def __init__(self):
        self.adj_list: Dict[int, List[Tuple[int, int]]] = {}

    def adicionar_vertice(self, vertice: int) -> None:
        if vertice not in self.adj_list:
            self.adj_list[vertice] = []

    def adicionar_aresta(self, u: int, v: int, peso: int) -> None:
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)
        self.adj_list[u].append((v, peso))
        self.adj_list[v].append((u, peso))

    def gerar_grafo_aleatorio(self, num_vertices: int, probabilidade_conexao: float = 0.5) -> None:
        self.adj_list.clear()
        vertices = list(range(num_vertices))
        for v in vertices:
            self.adicionar_vertice(v)

        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if random.random() < probabilidade_conexao:
                    peso = random.randint(1, 50)
                    self.adicionar_aresta(vertices[i], vertices[j], peso)

    def dijkstra(self, origem: int, destino: int) -> Tuple[List[int], float]:
        if origem not in self.adj_list or destino not in self.adj_list:
            return [], float('inf')

        distancias = {v: float('inf') for v in self.adj_list}
        distancias[origem] = 0
        predecessores: Dict[int, Optional[int]] = {v: None for v in self.adj_list}
        pq = [(0, origem)]
        
        while pq:
            distancia_atual, u = heapq.heappop(pq)
            
            if u == destino:
                break
            
            if distancia_atual > distancias[u]:
                continue
            
            for vizinho, peso in self.adj_list[u]:
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    predecessores[vizinho] = u
                    heapq.heappush(pq, (nova_distancia, vizinho))
        
        caminho = []
        atual = destino
        if distancias[destino] == float('inf'):
            return [], float('inf')
            
        while atual is not None:
            caminho.append(atual)
            atual = predecessores[atual]
        
        return caminho[::-1], distancias[destino]

# --- Interface Gráfica (GUI) ---
class DijkstraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador do Algoritmo de Dijkstra")
        self.root.geometry("1000x700")

        self.grafo = Grafo()
        self.G_nx = None # Objeto grafo do NetworkX
        self.pos = None  # Posições dos nós para layout consistente

        # --- Frame de Controle (Esquerda) ---
        control_frame = ttk.Frame(root, padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Configuração do Grafo
        ttk.Label(control_frame, text="Configuração do Grafo", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        ttk.Label(control_frame, text="Número de Vértices:").pack(anchor=tk.W)
        self.entry_num_vertices = ttk.Entry(control_frame)
        self.entry_num_vertices.insert(0, "8")
        self.entry_num_vertices.pack(fill=tk.X, pady=(0, 10))

        self.btn_gerar = ttk.Button(control_frame, text="Gerar Novo Grafo", command=self.gerar_novo_grafo)
        self.btn_gerar.pack(fill=tk.X, pady=(0, 20))

        # Cálculo do Caminho
        ttk.Label(control_frame, text="Caminho Mínimo", font=("Arial", 12, "bold")).pack(pady=(0, 10))

        ttk.Label(control_frame, text="Nó de Partida:").pack(anchor=tk.W)
        self.entry_origem = ttk.Entry(control_frame)
        self.entry_origem.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(control_frame, text="Nó de Destino:").pack(anchor=tk.W)
        self.entry_destino = ttk.Entry(control_frame)
        self.entry_destino.pack(fill=tk.X, pady=(0, 10))

        self.btn_calcular = ttk.Button(control_frame, text="Calcular Caminho", command=self.calcular_caminho)
        self.btn_calcular.pack(fill=tk.X, pady=(0, 20))

        # Resultados
        ttk.Label(control_frame, text="Resultados", font=("Arial", 12, "bold")).pack(pady=(0, 10))
        self.lbl_distancia = ttk.Label(control_frame, text="Distância Total: -", font=("Arial", 11))
        self.lbl_distancia.pack(anchor=tk.W)
        
        self.lbl_caminho_texto = ttk.Label(control_frame, text="Caminho: -", wraplength=180)
        self.lbl_caminho_texto.pack(anchor=tk.W, pady=(5, 0))

        # --- Área de Desenho (Direita) ---
        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Inicializa a figura do Matplotlib
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Gera um grafo inicial
        self.gerar_novo_grafo()

    def gerar_novo_grafo(self):
        try:
            num_vertices = int(self.entry_num_vertices.get())
            if num_vertices < 2:
                raise ValueError("Mínimo de 2 vértices.")
        except ValueError:
            messagebox.showerror("Erro", "Número de vértices inválido.")
            return

        # Gera o grafo lógico
        self.grafo.gerar_grafo_aleatorio(num_vertices, probabilidade_conexao=0.4)

        # Converte para NetworkX para visualização
        self.G_nx = nx.Graph()
        for u, vizinhos in self.grafo.adj_list.items():
            self.G_nx.add_node(u)
            for v, peso in vizinhos:
                self.G_nx.add_edge(u, v, weight=peso)

        # Calcula o layout (posições fixas para este grafo)
        self.pos = nx.spring_layout(self.G_nx, seed=42)  # Seed para consistência visual se re-desenhar

        # Reseta labels
        self.lbl_distancia.config(text="Distância Total: -")
        self.lbl_caminho_texto.config(text="Caminho: -")
        
        # Define valores padrão para origem e destino
        self.entry_origem.delete(0, tk.END)
        self.entry_origem.insert(0, "0")
        self.entry_destino.delete(0, tk.END)
        self.entry_destino.insert(0, str(num_vertices - 1))

        self.desenhar_grafo()

    def calcular_caminho(self):
        origem_str = self.entry_origem.get().strip()
        destino_str = self.entry_destino.get().strip()

        if not origem_str or not destino_str:
            messagebox.showwarning("Aviso", "Por favor, preencha os campos de Origem e Destino.")
            return

        try:
            origem = int(origem_str)
            destino = int(destino_str)
        except ValueError:
            messagebox.showerror("Erro", "Origem e Destino devem ser números inteiros válidos.")
            return

        # Verifica se os vértices existem no grafo
        if origem not in self.grafo.adj_list:
             messagebox.showerror("Erro", f"O vértice de origem '{origem}' não existe no grafo.")
             return
        if destino not in self.grafo.adj_list:
             messagebox.showerror("Erro", f"O vértice de destino '{destino}' não existe no grafo.")
             return

        caminho, distancia = self.grafo.dijkstra(origem, destino)

        if distancia == float('inf'):
            self.lbl_distancia.config(text="Distância Total: Infinito")
            self.lbl_caminho_texto.config(text="Caminho: Não existe")
            messagebox.showinfo("Info", f"Não há caminho possível entre {origem} e {destino} (Grafo Desconexo).")
            self.desenhar_grafo() # Limpa destaque anterior
        else:
            self.lbl_distancia.config(text=f"Distância Total: {distancia}")
            self.lbl_caminho_texto.config(text=f"Caminho: {caminho}")
            self.desenhar_grafo(caminho_destaque=caminho)

    def desenhar_grafo(self, caminho_destaque=None):
        self.ax.clear() # Limpa o plot anterior

        # Desenha nós base
        nx.draw_networkx_nodes(self.G_nx, self.pos, ax=self.ax, node_color='lightgray', node_size=500)
        nx.draw_networkx_labels(self.G_nx, self.pos, ax=self.ax)

        # Desenha arestas base
        nx.draw_networkx_edges(self.G_nx, self.pos, ax=self.ax, edge_color='gray', width=1)

        # Desenha pesos das arestas
        edge_labels = nx.get_edge_attributes(self.G_nx, 'weight')
        nx.draw_networkx_edge_labels(self.G_nx, self.pos, edge_labels=edge_labels, ax=self.ax)

        # Destaque do caminho
        if caminho_destaque:
            # Destaca nós do caminho
            nx.draw_networkx_nodes(self.G_nx, self.pos, nodelist=caminho_destaque, ax=self.ax, node_color='red', node_size=500)
            
            # Cria lista de arestas do caminho
            arestas_caminho = []
            for i in range(len(caminho_destaque) - 1):
                u = caminho_destaque[i]
                v = caminho_destaque[i+1]
                arestas_caminho.append((u, v))
            
            # Destaca arestas do caminho
            nx.draw_networkx_edges(self.G_nx, self.pos, edgelist=arestas_caminho, ax=self.ax, edge_color='red', width=3)

        self.ax.set_title("Visualização do Grafo")
        self.ax.axis('off') # Remove eixos
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraGUI(root)
    root.mainloop()
