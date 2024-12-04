from graph_tool.all import Graph, graph_draw #Pesado cargar esta libreria :c
import random
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
    weights = graph.ep["weight"]
    for edge in v.all_edges():
        u = edge.target() if edge.source() == v else edge.source()
        weight = weights[edge]
        if partition[u] == 2: #Si v es el nodo en el cual se debe insertar, entonces porque u deberia ser parte del growing part
            internal += weight
        else:
            external += weight
    return external - internal

def bfs(graph, start):
    partition = graph.vp["partition"]
    partition.a = 1 #Inicializar todos los nodos que empiecen con el valor 1 (rest)
    queue = Frontier()
    queue.add_or_update(start,update_gain(graph,start,partition))
    cnt = 0 # vertex that are in the growing part
    edgeCut = 0.0 # the cost of that edge cut
    weights = graph.ep["weight"]
    while not queue.is_empty() and cnt < graph.num_vertices()//2:
        node = queue.pop_max()
        partition[node] = 2
        cnt+=1

        for edge in node.all_edges():
            neigh = edge.target() if edge.source() == node else edge.source()
            weight = weights[edge] 
            edgeCut-= weight if partition[neigh] == 2 else -weight #optimizar para que no use graph.edge(node,neigh)
            if partition[neigh] == 1:
                partition[neigh] = 0
                queue.add_or_update(neigh,update_gain(graph,neigh,partition))
    #calculates edge-cut of the graph
    return edgeCut


def bipartition(graph): #It uses greedy graph growing algorithm
    minEdgeCut = float('inf')
    k = 4 #Escoger 4 vertices aleatorios | Propuesto por el paper
    for i in range(k):
        random_index = random.randint(0,graph.num_vertices()-1)
        start = graph.vertex(random_index)
        cost = bfs(graph,start)
        if cost < minEdgeCut:
            cost = minEdgeCut
            rStart = start
    bfs(graph,rStart) #Just update the graph partition
    partition = graph.vp["partition"]
    for v in graph.get_vertices():
        if partition[v] == 1:
            partition[v] = 0
