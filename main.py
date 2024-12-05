from hiearchical import *
from hierarchicalEmbeddings import *
from training import *
import networkx as nx
import os


from graph_tool.all import load_graph
import networkx as nx

def load_graph_tool_to_networkx(gt_file_path):
    """
    Load a Graph-tool graph from a .gt file and convert it to a NetworkX graph.

    Args:
        gt_file_path: Path to the Graph-tool file.

    Returns:
        A NetworkX graph with 'x' and 'y' attributes for all nodes.
    """
    # Load the Graph-tool graph
    gt_graph = load_graph(gt_file_path)

    # Convert Graph-tool graph to NetworkX graph
    nx_graph = nx.Graph()

    # Copy vertices
    for v in gt_graph.vertices():
        nx_graph.add_node(int(v))  # Add the vertex ID as a node

        # Copy attributes for each vertex
        for key, value in gt_graph.vp.items():
            nx_graph.nodes[int(v)][key] = value[v]

        # Add default 'x' and 'y' attributes if missing
        if 'x' not in nx_graph.nodes[int(v)]:
            nx_graph.nodes[int(v)]['x'] = 0  # Replace with meaningful coordinates if available
        if 'y' not in nx_graph.nodes[int(v)]:
            nx_graph.nodes[int(v)]['y'] = 0  # Replace with meaningful coordinates if available

    # Copy edges
    for e in gt_graph.edges():
        source = int(e.source())
        target = int(e.target())

        # Add the edge
        nx_graph.add_edge(source, target)

        # Copy attributes for each edge
        for key, value in gt_graph.ep.items():
            nx_graph[source][target][key] = value[e]

    return nx_graph


if not os.path.exists("hierarchical_vertex_embeddings.npy"):
    print("Matrix of embeddings not found...")
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

def error():
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


def main(embedding_file, dist_matrix, subgraph_hierarchy, landmarks, output_file, learning_rate=0.01, epochs=100):
    print("Step 1: Loading hierarchical embeddings...")
    embedding_matrix = np.load(embedding_file)
    print(f"Loaded embeddings with shape: {embedding_matrix.shape}")

    print("\nStep 2: Subgraph training...")
    for subgraph_id, subgraph_data in subgraph_hierarchy.items():
        subgraph = subgraph_data["graph"]
        print(f"Training on subgraph {subgraph_id} with {len(list(subgraph.vertices()))} vertices.")
        embedding_matrix = train_subgraph_embeddings(
            embedding_matrix, subgraph, dist_matrix, learning_rate, epochs
        )
        print(f"Completed training for subgraph {subgraph_id}.")

    print("\nStep 3: Landmark training...")
    print(f"Using {len(landmarks)} landmarks for training.")
    embedding_matrix = train_landmark_embeddings(
        embedding_matrix, landmarks, dist_matrix, learning_rate, epochs
    )
    print("Completed landmark training.")

    print("\nStep 4: High-error pair training...")
    print(f"Training on the top {100} high-error pairs.")
    embedding_matrix = train_high_error_embeddings(
        embedding_matrix, dist_matrix, num_pairs=100, learning_rate=learning_rate, epochs=epochs
    )
    print("Completed high-error pair training.")

    print("\nStep 5: Saving final embeddings...")
    np.save(output_file, embedding_matrix)
    print(f"Final embeddings saved to {output_file}.")

    return embedding_matrix



if __name__ == "__main__":
    # Inputs
    embedding_file = "hierarchical_vertex_embeddings.npy"
    graph = load_graph("california_graph.gt")
    subgraph_hierarchy = hierarchical_partition(graph, max_levels=4, vertex_size_threshold=10)
    output_file = "refined_hierarchical_embeddings.npy"

    graph = load_graph_tool_to_networkx("california_graph.gt")
    # Compute distance matrix for active nodes
    active_dist_matrix = graph#compute_active_distance_matrix(graph, active_nodes)
    print("Distance matrix for active nodes computed.")
    
    # Run the training workflow with the active distance matrix
    final_embeddings = main(
        embedding_file,
        active_dist_matrix,
        subgraph_hierarchy,
        output_file,
        learning_rate=0.01,
        epochs=50
    )
