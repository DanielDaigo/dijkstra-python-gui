# Documentação Técnica do Projeto: Visualizador do Algoritmo de Dijkstra

**Disciplina:** Estrutura de Dados Avançada  
**Projeto:** Implementação e Visualização do Algoritmo de Dijkstra  
**Data:** 25 de Novembro de 2025

---

## 1. Metodologia Ágil Aplicada (Scrum)

Para o desenvolvimento deste projeto, adotou-se o framework ágil **Scrum**, visando garantir entregas incrementais, flexibilidade a mudanças e foco na qualidade do código. O ciclo de vida do desenvolvimento foi dividido em **Sprints de 1 semana**, permitindo validações constantes das funcionalidades implementadas.

### Rituais Realizados

- **Sprint Planning:** No início de cada ciclo, foram definidas as metas e selecionados os itens do Product Backlog para o Sprint Backlog.
- **Daily Meetings:** Reuniões diárias curtas (stand-ups) para alinhar o progresso, identificar impedimentos técnicos (ex: integração do Matplotlib com Tkinter) e planejar as atividades do dia.
- **Sprint Review:** Ao final de cada semana, o incremento de software funcional foi validado para garantir que os requisitos técnicos (geração de grafos, cálculo de rotas) estavam sendo atendidos.

### Artefatos Ágeis

#### 1.1 Product Backlog (Histórias de Usuário)

| ID   | Prioridade | História de Usuário                                                           | Critérios de Aceitação                                                           |
| :--- | :--------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| US01 | Alta       | Como usuário, quero uma estrutura de dados que represente um grafo ponderado. | Classe `Grafo` implementada com lista de adjacência; suporte a pesos.            |
| US02 | Alta       | Como usuário, quero calcular o caminho mais curto entre dois pontos.          | Algoritmo de Dijkstra implementado corretamente; retorno da distância e caminho. |
| US03 | Média      | Como usuário, quero visualizar o grafo graficamente.                          | Plotagem de nós e arestas usando bibliotecas gráficas.                           |
| US04 | Média      | Como usuário, quero interagir com o sistema através de uma interface visual.  | Janela com botões e campos de entrada para origem/destino.                       |
| US05 | Baixa      | Como usuário, quero ver o caminho mínimo destacado visualmente.               | Nós e arestas do caminho resultante devem ter cor diferente (vermelho).          |

#### 1.2 Sprint Backlog (Tarefas Técnicas)

| Sprint       | Item do Backlog   | Tarefas Técnicas Executadas                                                                                                                                                                                                |
| :----------- | :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sprint 1** | US01, US02        | - Criação da classe `Grafo`.<br>- Implementação do método `adicionar_vertice` e `adicionar_aresta`.<br>- Implementação da lógica de randomização de grafos.<br>- Codificação do Algoritmo de Dijkstra usando `heapq`.      |
| **Sprint 2** | US03, US04        | - Configuração do ambiente `Tkinter`.<br>- Integração da biblioteca `NetworkX` para layout dos nós.<br>- Integração do `Matplotlib` (`FigureCanvasTkAgg`) na janela Tkinter.<br>- Criação dos inputs e botões de controle. |
| **Sprint 3** | US05, Refinamento | - Lógica de coloração condicional de arestas e nós.<br>- Tratamento de exceções (grafos desconexos, inputs inválidos).<br>- Refatoração e limpeza de código.<br>- Documentação final.                                      |

#### 1.3 Incremento do Produto

Ao final do ciclo de desenvolvimento, o produto entregue consiste em uma aplicação Desktop robusta, capaz de gerar cenários aleatórios de grafos e resolver problemas de caminho mínimo em tempo real, com feedback visual imediato para o usuário.

---

## 2. Evolução do Projeto e Protótipos

O desenvolvimento seguiu uma abordagem iterativa e incremental, evoluindo de uma lógica puramente matemática para uma aplicação visual completa.

### Fase 1: Backend e Lógica (Console)

Nesta fase inicial, o foco foi exclusivamente na correção algorítmica. A classe `Grafo` foi desenvolvida e testada via terminal. O objetivo era garantir que a estrutura de dados (lista de adjacência) e o algoritmo de Dijkstra (fila de prioridade) estivessem retornando os valores matematicamente corretos antes de qualquer implementação visual.

### Fase 2: Integração GUI Básica (Wireframe Funcional)

A segunda fase consistiu na construção do esqueleto da interface gráfica. Foi realizada a integração entre o `Tkinter` (container da janela) e o `Matplotlib` (motor de renderização). Nesta etapa, o grafo era desenhado em cinza, sem distinção de caminhos, e os controles de usuário eram limitados, servindo apenas para validar a plotagem dos nós nas coordenadas corretas geradas pelo `spring_layout`.

### Fase 3: Versão Final (Interatividade e UX)

A versão final incorporou a lógica de negócios à interface visual. Foram implementados:

1.  **Feedback Visual:** O caminho calculado pelo Dijkstra agora é destacado em vermelho (nós e arestas).
2.  **Robustez:** Adição de blocos `try/except` para prevenir falhas em casos de grafos desconexos ou entradas não numéricas.
3.  **Usabilidade:** Melhoria na disposição dos elementos e limpeza visual do gráfico (remoção de eixos).

---

## 3. Cronograma Detalhado

O projeto foi executado ao longo de 3 semanas, seguindo o planejamento das Sprints.

| Semana / Sprint | Período Estimado | Atividades Realizadas                                                                                                                                                                                                           | Status       |
| :-------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------- |
| **Semana 01**   | 10/11 - 14/11    | - Definição da arquitetura do projeto.<br>- Implementação da classe `Grafo`.<br>- Testes unitários manuais do algoritmo de Dijkstra.<br>- Implementação do gerador de grafos aleatórios.                                        | ✅ Concluído |
| **Semana 02**   | 17/11 - 21/11    | - Desenvolvimento da interface base em `Tkinter`.<br>- Estudo e implementação da integração `NetworkX` + `Matplotlib`.<br>- Criação do layout da janela (Frame de controle vs. Área de plotagem).                               | ✅ Concluído |
| **Semana 03**   | 24/11 - 27/11    | - Conexão entre o botão "Calcular" e a lógica do Dijkstra.<br>- Implementação da renderização condicional (destaque de caminho).<br>- Tratamento de erros e validação de inputs.<br>- Escrita da documentação técnica e README. | ✅ Concluído |

---

**Conclusão Técnica:**
O projeto atingiu todos os requisitos funcionais e não funcionais propostos. A escolha da linguagem Python, aliada às bibliotecas `NetworkX` e `Matplotlib`, provou-se eficiente para a prototipagem rápida e visualização de estruturas de dados complexas, enquanto o uso de metodologias ágeis garantiu um desenvolvimento organizado e livre de débitos técnicos críticos.
