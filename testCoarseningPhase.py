from graph_tool.all import Graph, graph_draw
# Testing
g = Graph(directed=False)

v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()

e1 = g.add_edge(v1, v2)
e2 = g.add_edge(v2, v3)
e3 = g.add_edge(v3, v4)
e4 = g.add_edge(v4, v1)
e5 = g.add_edge(v1, v3)

vertex_labels = g.new_vertex_property("string")
vertex_labels[v1] = "A"
vertex_labels[v2] = "B"
vertex_labels[v3] = "C"
vertex_labels[v4] = "D"
g.vp["name"] = vertex_labels

edge_weights = g.new_edge_property("double")
edge_weights[e1] = 1.9
edge_weights[e2] = 2.0
edge_weights[e3] = 2.5
edge_weights[e4] = 1.0
edge_weights[e5] = 3.0
g.ep["weight"] = edge_weights


"""graph_draw(g,
           vertex_text=g.vp["name"],  # Mostrar etiquetas de vértices
           edge_text=g.ep["weight"],  # Mostrar pesos de aristas
           output_size=(500, 500))"""
tmpGraph = compress(g)
graph_draw(tmpGraph,
           vertex_text=tmpGraph.vp["name"],  # Mostrar etiquetas de vértices
           edge_text=tmpGraph.ep["weight"],  # Mostrar pesos de aristas
           output_size=(500, 500))