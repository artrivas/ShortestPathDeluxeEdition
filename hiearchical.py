from graph_tool.all import Graph, load_graph, GraphView
import random
import matplotlib.pyplot as plt
import networkx as nx

def hierarchical_partition(graph, max_levels, vertex_size_threshold):
    """
    Perform hierarchical partitioning of a graph and track the hierarchy.

    Args:
        graph: The input graph.
        max_levels: Maximum number of levels in the hierarchy.
        vertex_size_threshold: Minimum size of a subgraph to partition further.

    Returns:
        hierarchy: A nested dictionary representing the hierarchy.
    """
    hierarchy = {}

    def partition_graph(current_graph, level, parent_id):
        # Create a unique ID for the current graph
        graph_id = len(hierarchy)
        hierarchy[graph_id] = {
            "level": level,
            "parent": parent_id,
            "graph": current_graph,
            "children": []
        }
        
        print(f"Partitioning level {level}, nodes: {current_graph.num_vertices()}, edges: {current_graph.num_edges()}")

        # Stop if maximum levels reached or graph is too small
        if level >= max_levels or current_graph.num_vertices() <= vertex_size_threshold:
            return
        
        # Perform graph partitioning
        blocks = random_partition(current_graph, k=2)  # Example: Random partitioning
        num_blocks = len(set(blocks.a))  # Number of blocks
        print(f"Level {level}: Found {num_blocks} blocks")

        if num_blocks <= 1:
            return

        # Create subgraphs and recursively partition them
        subgraphs = {}
        for v in current_graph.vertices():
            block = blocks[v]
            if block not in subgraphs:
                subgraphs[block] = current_graph.new_vertex_property("bool")
            subgraphs[block][v] = True

        for block, mask in subgraphs.items():
            subgraph = Graph(GraphView(current_graph, vfilt=mask), directed=False)
            child_id = len(hierarchy)
            hierarchy[graph_id]["children"].append(child_id)
            partition_graph(subgraph, level + 1, parent_id=graph_id)

    partition_graph(graph, level=0, parent_id=None)
    return hierarchy

# Example: Random partitioning
def random_partition(graph, k=2):
    """
    Randomly partition the graph into k blocks.
    """
    blocks = graph.new_vertex_property("int")
    for v in graph.vertices():
        blocks[v] = random.randint(0, k - 1)
    return blocks


# Print the hierarchy
def print_hierarchy(hierarchy):
    for graph_id, data in hierarchy.items():
        parent = data["parent"]
        children = data["children"]
        print(f"Graph ID: {graph_id}, Level: {data['level']}, Parent: {parent}, Children: {children}, "
              f"Nodes: {data['graph'].num_vertices()}, Edges: {data['graph'].num_edges()}")

# Load the graph
# graph = load_graph("california_graph.gt")
# hierarchy = hierarchical_partition(graph, max_levels=4, vertex_size_threshold=10)
# print_hierarchy(hierarchy)



# Visualize the graph
def visualize_hierarchy(hierarchy):
    tree = nx.DiGraph()
    for graph_id, data in hierarchy.items():
        tree.add_node(graph_id, level=data["level"])
        for child_id in data["children"]:
            tree.add_edge(graph_id, child_id)

    pos = nx.nx_agraph.graphviz_layout(tree, prog="dot")
    nx.draw(tree, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=8, arrows=True)
    plt.show()

# Visualize the hierarchy
# visualize_hierarchy(hierarchy)


