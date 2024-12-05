from graph_tool.all import Graph, graph_draw
import numpy as np
import random
from collections import deque
import heapq


def compress(graph):
    matched = dict()
    newGraph = Graph(graph,directed=False)
    child1 = newGraph.new_vertex_property("object")
    child2 = newGraph.new_vertex_property("object")
    weights = newGraph.ep["weight"]
    toBeDeleted = []
    for v in newGraph.vertices():
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
            #Merge node u and v
            x = newGraph.add_vertex()
            toBeDeleted.append(u)
            toBeDeleted.append(v)
            matched[v] = x #for deletion purposes
            matched[u] = x #for deletion purposes
            matched[x] = x
            
            child1[x] = u
            child2[x] = v
            for vertice in [u,v]:
                for edge in vertice.all_edges():
                    weight = newGraph.ep["weight"][edge]
                    other = edge.target() if edge.source() == vertice else edge.source()
                    if other in matched:
                        other = matched[other]
                    if other == x:
                        continue
                    # Check if edge already exists
                    existing_edge = newGraph.edge(other, x)
                    if existing_edge:
                        newGraph.ep["weight"][existing_edge] += weight
                    else:
                        new_edge = newGraph.add_edge(other, x)
                        newGraph.ep["weight"][new_edge] = weight
    for v in reversed(sorted(toBeDeleted)):
        newGraph.remove_vertex(v)
    
    newGraph.vp["child1"] = child1
    newGraph.vp["child2"] = child2
    return newGraph

