import numpy as np
from graph_tool.all import shortest_distance
from sklearn.manifold import MDS
from hiearchical import *
import gc


def generate_hierarchical_embeddings(hierarchy, embedding_dim=3, chunk_size=500):
    """
    Generate hierarchical embeddings for a partitioned graph with memory optimization.

    Args:
        hierarchy: Dictionary representing the graph hierarchy.
        embedding_dim: Dimension of the embedding space.
        chunk_size: Number of nodes to process in a single chunk.

    Returns:
        global_embeddings: Dictionary mapping vertex IDs to their global embeddings.
    """
    global_embeddings = {}

    for graph_id, data in hierarchy.items():
        subgraph = data["graph"]
        level = data["level"]

        # Get all vertices from the subgraph
        all_vertices = list(subgraph.vertices())  # These are graph-tool vertex objects

        # Process vertices in chunks
        for start in range(0, len(all_vertices), chunk_size):
            end = min(start + chunk_size, len(all_vertices))
            chunk_vertices = all_vertices[start:end]  # Actual vertex objects

            # Calculate pairwise shortest distances for the chunk
            dist_matrix = np.zeros((len(chunk_vertices), len(chunk_vertices)))
            for i, v_start in enumerate(chunk_vertices):
                distances = shortest_distance(subgraph, source=v_start)
                dist_matrix[i] = [distances[v_end] for v_end in chunk_vertices]

            # Generate local embeddings with MDS
            mds = MDS(n_components=embedding_dim, dissimilarity="precomputed", random_state=42)
            local_embeddings = mds.fit_transform(dist_matrix)

            # Map local embeddings to global embeddings
            for i, v in enumerate(chunk_vertices):
                vertex_id = int(v)  # Ensure this matches the external ID

                # Initialize global embedding if not already present
                if vertex_id not in global_embeddings:
                    global_embeddings[vertex_id] = np.zeros(embedding_dim)

                # Add the local embedding to the global embedding
                global_embeddings[vertex_id] += local_embeddings[i]

            # Free memory
            del dist_matrix, local_embeddings
            gc.collect()

    return global_embeddings



# Example: Calculate errors for the hierarchical embeddings
def calculate_errors_hierarchy(global_embeddings, dist_matrix, vs, vt):
    """
    Calculate errors between global embeddings and true distances.

    Args:
        global_embeddings: Dictionary of vertex embeddings.
        dist_matrix: Real distance matrix.
        vs: Source vertex index.
        vt: Target vertex index.

    Returns:
        Tuple containing estimated distance, real distance, absolute error, and relative error.
    """
    # Distancia estimada (L1 en espacio de embedding)
    estimated_distance = np.sum(np.abs(global_embeddings[vs] - global_embeddings[vt]))

    # Distancia real en el grafo
    real_distance = dist_matrix[vs, vt]

    # Cálculo del error absoluto y relativo
    abs_error = np.abs(estimated_distance - real_distance)
    rel_error = abs_error / real_distance if real_distance != 0 else float("inf")

    return estimated_distance, real_distance, abs_error, rel_error



# Loaded Graph
graph = load_graph("california_graph.gt")
hierarchy = hierarchical_partition(graph, max_levels=4, vertex_size_threshold=10)
print("Graph Loaded")
hierarchical_partitions = hierarchy  # Hierarchy created from the partition code
embedding_dim = 3  # Dimensionality of the embeddings

# Generate embeddings for the hierarchical model
global_embeddings = generate_hierarchical_embeddings(hierarchical_partitions, embedding_dim)
print("Embeddings Generated")

# Convert global embeddings into a matrix for training
num_vertices = max(global_embeddings.keys()) + 1
embedding_matrix = np.zeros((num_vertices, embedding_dim))
for vertex_id, embedding in global_embeddings.items():
    embedding_matrix[vertex_id] = embedding

# Save the embedding matrix
np.save("hierarchical_vertex_embeddings.npy", embedding_matrix)
print("Matrix Saved")
# Example: Calculate errors for two vertices
example_subgraph = list(hierarchical_partitions.values())[0]["graph"]  # Use the first partitioned subgraph
distances = shortest_distance(example_subgraph)
dist_matrix = np.array(distances.get_2d_array(range(example_subgraph.num_vertices())))

vs, vt = 1, 10  # Replace with real vertex indices
estimated, real, abs_err, rel_err = calculate_errors_hierarchy(global_embeddings, dist_matrix, vs, vt)

# Print results
print(f"Embedding del nodo {vs}: {global_embeddings[vs]}, nodo {vt}: {global_embeddings[vt]}")
print(f"Distancia estimada (L1): {estimated}")
print(f"Distancia real: {real}")
print(f"Error absoluto: {abs_err}")
print(f"Error relativo: {rel_err:.2%}")
