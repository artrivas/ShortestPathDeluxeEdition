from graph_tool.all import Graph, graph_draw
import numpy as np
import random
from collections import deque
import heapq


def compress(graph):
    matched = dict()
    newGraph = Graph(graph,directed=False)
    coarse_map = graph.new_vertex_property("object")
    weights = graph.ep["weight"]
    for v in graph.vertices():
        if v in matched:
            continue
        max_edge = None
        max_weight = float('-inf')
        for e in v.all_edges():
            neigh = e.target() if e.source() == v else e.source()
            if neigh not in matched:
                weight = weights[e]
                if weight > max_weight:
                    max_edge = (v,neigh)
                    max_weight = weight
        if max_edge != None:
            u,v = max_edge
            matched[v] = True
            matched[u] = True
            #Merge node u and v
            x = newGraph.add_vertex()
            coarse_map[u] = x
            coarse_map[v] = v
            for vertice in [u,v]:
                for edge in vertice.all_edges():
                    weight = newGraph.ep["weight"][edge]
                    other = edge.target() if edge.source() == vertice else edge.source()
                    # Check if edge already exists
                    existing_edge = newGraph.edge(other, x)
                    if existing_edge:
                        newGraph.ep["weight"][existing_edge] += weight
                    else:
                        new_edge = newGraph.add_edge(other, x)
                        newGraph.ep["weight"][new_edge] = weight
                    
            newGraph.remove_vertex(newGraph.vertex(u), fast=True)
            newGraph.remove_vertex(newGraph.vertex(v), fast=True)
    graph.vp["collapse"] = coarse_map
    return newGraph