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
    for edge in v.all_edges():
        u = edge.target() if edge.source() == v else edge.source()
        weight = graph.ep["weight"][edge]
        if partition[u] == 2: #Si v es el nodo en el cual se debe insertar, entonces porque u deberia ser parte del growing part
            internal += weight
        else:
            external += weight
    return external - internal

def bfs(graph, start,mode):
    vertices = graph.get_vertices()
    if mode: #partition the graph by the start node
        graph1 = Graph(graph,directed=False)
        graph2 = Graph(graph,directed=False)
    partition = dict() #[vertex, partition] -> 0: candidate | 1: rest | 2: growing part
    for v in vertices:
        partition[v] = 1
    queue = Frontier()
    queue.add_or_update(start,update_gain(graph,start,partition))
    cnt = 0 # vertex that are in the growing part
    edgeCut = 0.0 # the cost of that edge cut
    
    while not queue.is_empty() and cnt < graph.num_vertices()//2:
        node = queue.pop_max()
        partition[node] = 2
        cnt+=1

        for edge in node.all_edges():
            neigh = edge.target() if edge.source() == node else edge.source()
            weight = graph.ep["weight"][edge]
            edgeCut-= weight if partition[neigh] == 2 else -weight #optimizar para que no use graph.edge(node,neigh)
            if partition[neigh] == 1:
                partition[neigh] = 0
                queue.add_or_update(neigh,update_gain(graph,neigh,partition))
            
            
    if mode:
        print(vertices)
        for v in sorted(vertices, reverse=True):
            if partition[v] == 2: 
                graph2.remove_vertex(graph2.vertex(v))
            else:  
                graph1.remove_vertex(graph1.vertex(v))
        return [graph1, graph2]
    #calculates edge-cut of the graph
    return edgeCut


def bipartition(graph): #It uses greedy graph growing algorithm
    minEdgeCut = float('inf')
    k = 4 #Escoger 4 vertices aleatorios | Propuesto por el paper
    for i in range(k):
        random_index = random.randint(0,graph.num_vertices()-1)
        start = graph.vertex(random_index)
        cost = bfs(graph,start,False)
        if cost < minEdgeCut:
            cost = minEdgeCut
            rStart = start
    return bfs(graph,rStart,True)

#testing
# Initialize the original graph

g = Graph(directed=False)

# Add the initial 4 vertices
vertices = [g.add_vertex() for _ in range(4)]
vertex_labels = g.new_vertex_property("string")
vertex_labels[vertices[0]] = "A"
vertex_labels[vertices[1]] = "B"
vertex_labels[vertices[2]] = "C"
vertex_labels[vertices[3]] = "D"

# Add the initial edges
edges = [
    g.add_edge(vertices[0], vertices[1]),
    g.add_edge(vertices[1], vertices[2]),
    g.add_edge(vertices[2], vertices[3]),
    g.add_edge(vertices[3], vertices[0]),
    g.add_edge(vertices[0], vertices[2]),
]

# Assign weights to the initial edges
edge_weights = g.new_edge_property("double")
edge_weights[edges[0]] = 1.9
edge_weights[edges[1]] = 2.0
edge_weights[edges[2]] = 2.5
edge_weights[edges[3]] = 1.0
edge_weights[edges[4]] = 3.0

# Expand to 20 vertices
for i in range(4, 20):
    new_vertex = g.add_vertex()
    vertices.append(new_vertex)
    vertex_labels[new_vertex] = f"V{i}"

# Ensure all vertices are connected (spanning tree first)
for i in range(4, 20):
    # Connect each new vertex to an existing random vertex
    target = vertices[random.randint(0, i - 1)]
    edge = g.add_edge(vertices[i], target)
    edge_weights[edge] = round(random.uniform(1.0, 10.0), 1)

# Add additional random edges to make the graph more dense
while len(list(g.edges())) < 50:  # Add up to a total of 50 edges
    u, v = random.sample(vertices, 2)
    if not g.edge(u, v):
        edge = g.add_edge(u, v)
        edge_weights[edge] = round(random.uniform(1.0, 10.0), 1)

# Assign vertex labels and edge weights
g.vp["name"] = vertex_labels
g.ep["weight"] = edge_weights

g1,g2 = bipartition(g)
print(g1.num_vertices(), g2.num_vertices())
# Draw the graph
graph_draw(
    g1,
    vertex_text=g1.vp["name"],  # Show vertex labels
    edge_text=g1.ep["weight"],  # Show edge weights
    output_size=(800, 800)
)