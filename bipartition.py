from graph_tool.all import Graph, GraphView, load_graph, graph_draw
import coarseningPhase as cP
import partition as pary
import uncoarseningPhase as uP
import random
import matplotlib.pyplot as plt

def separate(graph):
    vertices = graph.get_vertices()
    graph1 = Graph(graph,directed=False)
    graph2 = Graph(graph,directed=False)
    partition = graph.vp["partition"]

    for v in sorted(vertices, reverse=True):
        if partition[v] == 2: 
            graph2.remove_vertex(graph2.vertex(v))
        else:  
            graph1.remove_vertex(graph1.vertex(v))
    return [graph1, graph2]

def bipartition(graph):
    graphs = [graph]
    while graph.num_vertices() > 2:
        graph = cP.compress(graph)
        graphs.append(graph)
    pary.bipartition(graphs[len(graphs)-1])
    uP.decompress(graphs)
    #print(len(graphs)-1)
    return separate(graphs[0])

def k_partition(graph, k):
    if k == 1:
        return [graph]
    
    graphs = [graph]
    while graph.num_vertices() > 2:
        graph = cP.compress(graph)
        graphs.append(graph)
    
    pary.bipartition(graphs[-1])
    uP.decompress(graphs)

    subgraph1, subgraph2 = separate(graphs[0])

    partitions = []
    partitions.extend(k_partition(subgraph1, k // 2))
    partitions.extend(k_partition(subgraph2, k - k // 2))

    return partitions
