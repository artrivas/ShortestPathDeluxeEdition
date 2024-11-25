from graph_tool.all import Graph, graph_draw
import numpy as np


def compress(graph):
    matched = dict()
    newGraph = Graph(graph)
    for v in graph.vertices():
        if v not in matched:
            max_edge = None
            max_weight = float('-inf')
            for neigh in v.all_neighbors():
                if neigh not in matched:
                    weight =  float(graph.ep["weight"][graph.edge(v,neigh)]) #Heavy Edge Matching, Only 2*|E| iterations
                    if weight > max_weight:
                        max_edge = (v,neigh)
                        max_weight = weight
            if max_edge != None:
                u,v = max_edge
                matched[v] = True
                matched[u] = True
                #Merge node u and v
                x = newGraph.add_vertex()
                for vertice in max_edge:
                    for edge in vertice.all_edges():
                        source = edge.source()
                        weight = graph.ep["weight"][edge]

                        # Check if edge already exists
                        existing_edge = newGraph.edge(source, x)
                        if existing_edge:
                            newGraph.ep["weight"][existing_edge] += weight
                        else:
                            new_edge = newGraph.add_edge(source, x)
                            newGraph.ep["weight"][new_edge] = weight
                newGraph.remove_vertex(newGraph.vertex(u), fast=True)
                newGraph.remove_vertex(newGraph.vertex(v), fast=True)
    return newGraph

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
edge_weights[e1] = 1.5
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