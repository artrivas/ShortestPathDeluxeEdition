from graph_tool.all import Graph

# Create a graph
g = Graph()

# Add some vertices
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()

# Add a vertex property to map to a vertex
coarse_map = g.new_vertex_property("object")

# Map v1 and v2 to v3
coarse_map[v1] = v3
coarse_map[v2] = v3
print(int(v1))
print(int(v2))
print(int(v3))

# Delete v2
g.remove_vertex(v2)
print(int(v1))
print(int(v3))

# Check that coarse_map still points to the correct vertex
print(coarse_map[v1] == v3)  # Should still be True
