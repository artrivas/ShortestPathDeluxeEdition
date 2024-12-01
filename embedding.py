import numpy as np
from graph_tool.all import Graph, shortest_distance
from sklearn.manifold import MDS

# 1. Crear el grafo pequeño de ejemplo
g = Graph(directed=False)  # Crear grafo no dirigido
vertices = {}  # Mapeo de IDs a vértices
edges = [
    (1, 2, 10), (2, 3, 20), (3, 4, 15), (4, 1, 25)  # (start_node, end_node, weight)
]  # Grafo de ejemplo

# Añadir vértices y aristas al grafo
weights = g.new_edge_property("double")  # Crear propiedad de peso
for u, v, weight in edges:
    if u not in vertices:
        vertices[u] = g.add_vertex()
    if v not in vertices:
        vertices[v] = g.add_vertex()
    edge = g.add_edge(vertices[u], vertices[v])
    weights[edge] = weight  # Asignar peso a la arista

# 2. Calcular distancias más cortas (reales) entre todos los nodos
distances = shortest_distance(g, weights=weights)  # Matriz de distancias reales

# 3. Obtener embeddings con MDS
d = 3  # Dimensiones del embedding
dist_matrix = np.array(distances.get_2d_array(range(len(vertices))))  # Matriz de distancias reales
mds = MDS(n_components=d, dissimilarity="precomputed", random_state=42)
embeddings = mds.fit_transform(dist_matrix)  # Embeddings en \mathbb{R}^d

# 4. Cálculo de distancias y errores
def calculate_errors(embeddings, dist_matrix, vs, vt):
    # Distancia estimada (L1 en espacio de embedding)
    estimated_distance = np.sum(np.abs(embeddings[vs] - embeddings[vt]))  # Distancia L1

    # Distancia real en el grafo
    real_distance = dist_matrix[vs, vt]

    # Cálculo del error absoluto y relativo
    abs_error = np.abs(estimated_distance - real_distance)
    rel_error = abs_error / real_distance if real_distance != 0 else float('inf')

    return estimated_distance, real_distance, abs_error, rel_error

# Elegir dos nodos para comparar (usaremos índices)
vs, vt = 0, 1  # Comparar los nodos 0 (ID 1) y 1 (ID 2)

# Calcular métricas
estimated, real, abs_err, rel_err = calculate_errors(embeddings, dist_matrix, vs, vt)

# Imprimir resultados
print(f"Embedding del nodo {vs}: {embeddings[vs]}, nodo {vt}: {embeddings[vt]}")
print(f"Distancia estimada (L1): {estimated}")
print(f"Distancia real: {real}")
print(f"Error absoluto: {abs_err}")
print(f"Error relativo: {rel_err:.2%}")

