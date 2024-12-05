from graph_tool.all import Graph, graph_draw #Pesado cargar esta libreria :c
import random
import heapq

"""
Tal vez crear otro atributo en el cual se deba añadir el atributo a que vertice colapsaron -> checkear si funciona realmente
"""
def find_boundary_vertices(graph, partition):
    boundary_vertices = set()
    for v in graph.vertices():
        for neighbor in v.all_neighbors():
            if partition[neighbor] != partition[v]:
                boundary_vertices.add(v)
                break
    return boundary_vertices

def calculate_gain(graph,v, partition):
    external = 0.0
    internal = 0.0
    weights = graph.ep["weight"]
    for edge in v.all_edges():
        u = edge.target() if edge.source() == v else edge.source()
        weight = weights[edge]
        if partition[u] == partition[v]:
            internal += weight
        else:
            external += weight
    return external - internal



#Insert we initially insert into the data structures the gains for only the boundary vertices
#Swap vertices -> update the gains of the adjacent vertices of v not yet begin swapped
def BKL(graph, partition, boundary_vertices,inte,exte, max_iterations=10):
    for _ in range(max_iterations):
        improved = False
        for v in boundary_vertices:
            gain = calculate_gain(graph, v, partition)
            if gain > 0:
                partition[v] = 0 if partition[v] == 2 else 2
                temp = exte[v]
                exte[v] = inte[v]
                inte[v] = temp
                
                for u in v.get_all_neighbors():
                    inte[u] += 1 if partition[u] != partition[v] else -1
                    exte[u] += 1 if partition[u] == partition[v] else -1

                    if exte[u] and u not in boundary_vertices:
                        boundary_vertices.add(u)
                    elif not exte[u] and u in boundary_vertices:
                        boundary_vertices.discard(u)

                improved = True
        if not improved:
            break
    return partition

def preprocess(graph,partition):
    inte = graph.new_vertex_property("int")
    exte = graph.new_vertex_property("int")
    for v in graph.vertices():
        for edge in v.all_edges():
            u = edge.target() if edge.source() == v else edge.source()
            if partition[u] == partition[v]:
                inte[v] += 1
            else:
                exte[v] += 1
    graph.vp["internal"] = inte
    graph.vp["external"] = exte    

def decompress(listGraphs):
    itr = len(listGraphs)-1
    p1 = listGraphs[itr].vp["partition"]
    preprocess(listGraphs[itr],p1)
    boundary_vertices = find_boundary_vertices(listGraphs[itr],p1)
    gsize = listGraphs[itr].num_vertices()
    while itr: #Expect to represent itr>=1
        pAfter = listGraphs[itr].vp["partition"] #graph after comprression
        pBefore = listGraphs[itr-1].new_vertex_property("int") #graph before compression
        child1 = listGraphs[itr].vp["child1"]
        child2 = listGraphs[itr].vp["child2"]
        #Project the vertices of G_{i+1} to G_i
        newExte = listGraphs[itr-1].new_vertex_property("int")
        newInte = listGraphs[itr-1].new_vertex_property("int")
        for v in listGraphs[itr].vertices():
            if child1[v]:
                pBefore[child1[v]] = pAfter[v]
            if child2[v]:
                pBefore[child2[v]] = pAfter[v]
        
        for v in listGraphs[itr-1].vertices():
            for u in v.all_neighbors():
                if pBefore[u] == pBefore[v]:
                    newInte[v] +=1
                else:
                    newExte[v] +=1
        #Up to see BKL-refinement
        if listGraphs[itr-1].num_vertices() <= gsize*2/100:
            BKL(listGraphs[itr-1],pBefore,boundary_vertices,newInte,newExte)
        else:
            BKL(listGraphs[itr-1],pBefore,boundary_vertices,newInte,newExte,1)
        listGraphs[itr-1].vp["internal"] = newInte
        listGraphs[itr-1].vp["external"] = newExte
        listGraphs[itr-1].vp["partition"] = pBefore#graph before compression
        itr-=1

    