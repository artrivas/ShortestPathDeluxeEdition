import numpy as np

def train_subgraph_embeddings(embedding_matrix, subgraph, dist_matrix, learning_rate=0.01, epochs=100):
    vertices = list(subgraph.vertices())
    vertex_indices = [int(v) for v in vertices]

    for epoch in range(epochs):
        for i, vs in enumerate(vertex_indices):
            for vt in vertex_indices:
                if vs != vt:
                    # True and estimated distances
                    true_distance = dist_matrix[vs, vt]
                    estimated_distance = np.sum(np.abs(embedding_matrix[vs] - embedding_matrix[vt]))
                    
                    # Gradient calculation
                    if true_distance > 0:
                        error = estimated_distance - true_distance
                        gradient = np.sign(embedding_matrix[vs] - embedding_matrix[vt])
                        
                        # Gradient descent update
                        embedding_matrix[vs] -= learning_rate * error * gradient
                        embedding_matrix[vt] += learning_rate * error * gradient

    return embedding_matrix


def select_landmarks(graph, embedding_matrix, num_landmarks):
    # Random node
    landmarks = [list(graph.nodes)[0]]

    for _ in range(1, num_landmarks):
        # Find the node farthest from the current landmarks
        max_distance = -1
        farthest_node = None

        for node in graph.nodes:
            if node not in landmarks:
                # Compute the minimum distance to any current landmark
                min_distance = min(
                    np.linalg.norm(embedding_matrix[node] - embedding_matrix[landmark])
                    for landmark in landmarks
                )
                if min_distance > max_distance:
                    max_distance = min_distance
                    farthest_node = node

        # Add the farthest node as a new landmark
        landmarks.append(farthest_node)

    return landmarks




def train_landmark_embeddings(embedding_matrix, landmarks, dist_matrix, learning_rate=0.01, epochs=100):
    for epoch in range(epochs):
        for vs in landmarks:
            for vt in range(len(embedding_matrix)):
                if vs != vt:
                    # True and estimated distances
                    true_distance = dist_matrix[vs, vt]
                    estimated_distance = np.sum(np.abs(embedding_matrix[vs] - embedding_matrix[vt]))

                    # Gradient calculation
                    if true_distance > 0:
                        error = estimated_distance - true_distance
                        gradient = np.sign(embedding_matrix[vs] - embedding_matrix[vt])
                        
                        # Gradient descent update
                        embedding_matrix[vs] -= learning_rate * error * gradient
                        embedding_matrix[vt] += learning_rate * error * gradient

    return embedding_matrix


def train_high_error_embeddings(embedding_matrix, dist_matrix, num_pairs=100, learning_rate=0.01, epochs=100):
    num_vertices = embedding_matrix.shape[0]
    errors = []

    # Calculate errors for all pairs
    for vs in range(num_vertices):
        for vt in range(num_vertices):
            if vs != vt:
                true_distance = dist_matrix[vs, vt]
                estimated_distance = np.sum(np.abs(embedding_matrix[vs] - embedding_matrix[vt]))
                abs_error = np.abs(estimated_distance - true_distance)
                errors.append((abs_error, vs, vt))

    # Sort by error and select the highest ones
    high_error_pairs = sorted(errors, key=lambda x: x[0], reverse=True)[:num_pairs]

    # Train on high-error pairs
    for epoch in range(epochs):
        for error, vs, vt in high_error_pairs:
            true_distance = dist_matrix[vs, vt]
            estimated_distance = np.sum(np.abs(embedding_matrix[vs] - embedding_matrix[vt]))
            
            # Gradient calculation
            if true_distance > 0:
                error = estimated_distance - true_distance
                gradient = np.sign(embedding_matrix[vs] - embedding_matrix[vt])
                
                # Gradient descent update
                embedding_matrix[vs] -= learning_rate * error * gradient
                embedding_matrix[vt] += learning_rate * error * gradient

    return embedding_matrix


def l1_distance(graph, u, v):
    x1 = graph.nodes[u].get('x', 0)  
    y1 = graph.nodes[u].get('y', 0)  
    x2 = graph.nodes[v].get('x', 0)
    y2 = graph.nodes[v].get('y', 0)
    return abs(x1 - x2) + abs(y1 - y2)



# def get_active_nodes(subgraph_hierarchy, landmarks, high_error_pairs):
#     """
#     Collect active nodes from subgraph hierarchy, landmarks, and high-error pairs.

#     Args:
#         subgraph_hierarchy: A dictionary of subgraphs (hierarchical partition).
#         landmarks: List of landmark node IDs.
#         high_error_pairs: List of (source, target) node pairs.

#     Returns:
#         A set of active node IDs.
#     """
#     active_nodes = set()

#     # Add nodes from all subgraphs
#     for subgraph_data in subgraph_hierarchy.values():
#         subgraph = subgraph_data["graph"]
#         active_nodes.update(int(v) for v in subgraph.vertices())

#     # Add landmarks
#     active_nodes.update(landmarks)

#     # Add nodes from high-error pairs
#     for vs, vt in high_error_pairs:
#         active_nodes.add(vs)
#         active_nodes.add(vt)

#     return list(active_nodes)



