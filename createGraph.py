import pandas as pd
from graph_tool.all import Graph

# Carga los datos
nodes_file = "./CaliforniaNodesCoordinates.txt"
edges_file = "./CaliforniaEdges.txt"

nodes_df = pd.read_csv(nodes_file, sep=" ", header=None, names=["id", "longitude", "latitude"])
edges_df = pd.read_csv(edges_file, sep=" ", header=None, names=["edge_id", "source", "target", "weight"])

# Crear el grafo
graph = Graph(directed=False)

# Agregar vértices
graph.vertex_properties["longitude"] = graph.new_vertex_property("float")
graph.vertex_properties["latitude"] = graph.new_vertex_property("float")

# Diccionario para mapear IDs de nodos al índice de vértices
node_map = {}
for _, row in nodes_df.iterrows():
    v = graph.add_vertex()
    node_map[row["id"]] = int(v)
    graph.vertex_properties["longitude"][v] = row["longitude"]
    graph.vertex_properties["latitude"][v] = row["latitude"]

# Agregar aristas
graph.edge_properties["weight"] = graph.new_edge_property("float")
for _, row in edges_df.iterrows():
    e = graph.add_edge(node_map[row["source"]], node_map[row["target"]])
    graph.edge_properties["weight"][e] = row["weight"]

# Visualización básica
print("Número de nodos:", graph.num_vertices())
print("Número de aristas:", graph.num_edges())

# Opcional: guardar el grafo
graph.save("california_graph.gt")