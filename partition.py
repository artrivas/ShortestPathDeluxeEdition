from graph_tool.all import Graph, graph_draw
import numpy as np
import random
from collections import deque
import heapq

class Frontier:
    def __init__(self):
        self.heap = []
        self.seen = dict()
        self.REMOVED = '<removed>'

    def add_or_update(self, vertex, gain):
        if vertex in self.seen:
            self.remove(vertex)
        entry = [-gain, vertex]
        self.seen[vertex] = entry
        heapq.heappush(self.heap, entry)

    def remove(self, vertex):
        entry = self.seen.pop(vertex)
        entry[-1] = self.REMOVED

    def pop_max(self):
        while self.heap:
            gain, vertex = heapq.heappop(self.heap)
            if vertex != self.REMOVED:
                del self.seen[vertex] #Checkear que hace esta funcion
                return vertex 
        raise KeyError('Frontera sin elementos')
    def is_empty(self):
        return not bool(self.seen)
    
def update_gain(graph,v, partition):
    external = 0.0
    internal = 0.0
    for edge in v.all_edges():
        u = edge.target() if edge.source() == v else edge.source()
        weight = graph.ep["weight"][edge]
        if partition[u] == 2: #Si v es el nodo en el cual se debe insertar, entonces porque u deberia ser parte del growing time
            internal += weight
        else:
            external += weight
    return external - internal

def bfs(graph, start,mode):
    if mode: #partition the graph by the start node
        graph1 = Graph(directed=False)
        graph2 = Graph(graph,directed=False)
    partition = dict() #[vertex, partition] -> 0: candidate | 1: rest | 2: growing part
    queue = Frontier()
    queue.add_or_update(start)
    cnt = 0 # vertex that are in the growing part
    edgeCut = 0.0 # the cost of that edge cut
    for v in graph.all_vertices():
        partition[v] = 1
    while not queue.is_empty() and cnt <= graph.num_vertices()//2:
        node = queue.pop_max()
        partition[node] = 2
        cnt+=1
        if mode:
            graph1.add_vertex(node) #checkear si es correcto añadirlo de esa manera
            graph2.remove_vertex(node) #checkear si es correcto | pq deberia primero remover las aristas y despues el vertice, no?
        for neigh in node.all_neighbors():
            edgeCut-= graph.ep["weight"][graph.edge(node,neigh)] if parition[neigh] == 2 else -graph.ep["weight"][graph.edge(node,neigh)]
            if partition[neigh] == 1:
                partition[neigh] = 0
                queue.add_or_update(neigh,update_gain(graph,neigh,partition))
            elif partition[neigh] == 2:
                graph1.add_edge(graph.edge(node,neigh)) #faltaria añadirle el atributo weight
                graph2.remove_edge(graph.edge(node,neigh))
    if mode:
        return [graph1, graph2]
    #calculates edge-cut of the graph
    return edgeCut


def parition(graph): #It uses greedy graph growing algorithm
    minEdgeCut = float('inf')
    #Escoger 4 vertices aleatorios
    for i in range(4):
        random_index = random.randint(0,graph.num_vertices()-1)
        start = graph.vertex(random_index)
        cost = bfs(graph,start,False)
        if cost < minEdgeCut:
            cost = minEdgeCut
            rStart = start
    return bfs(graph,rStart,True)


