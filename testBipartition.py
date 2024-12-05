#testing
"""g = load_graph("california_graph.gt")
g1,g2 = bipartition(g)

print(g.num_vertices(),g1.num_vertices(), g2.num_vertices())"""


# Crear un grafo dirigido
g = Graph(directed=False)

nodos = 20
# Añadir 20 vértices
vertices = [g.add_vertex() for _ in range(nodos)]

# Añadir pesos a las aristas
weights = g.new_edge_property("int")

# Crear un grafo completo: conectar todos los pares de vértices
for i in range(nodos):
    for j in range(i + 1, nodos):  # Evitar duplicar aristas en un grafo no dirigido
        edge = g.add_edge(vertices[i], vertices[j])
        weights[edge] = random.uniform(1, 10)  # Asignar un peso aleatorio entre 1 y 10

# Asignar los pesos al grafo
g.edge_properties["weight"] = weights

# Imprimir información del grafo
print(f"El grafo tiene {g.num_vertices()} vértices y {g.num_edges()} aristas.")

# Exportar o visualizar el grafo
g1,g2 = bipartition(g)
#print(g1.num_vertices(),g2.num_vertices())
graph_draw(g1, edge_text=g1.ep["weight"], vertex_text=g1.vp["partition"],output_size=(800,800))
