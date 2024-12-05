import partition
from graph_tool.all import Graph, graph_draw #Pesado cargar esta libreria :c
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


part = g.new_vertex_property("int") 
g.vp["partition"] = part
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