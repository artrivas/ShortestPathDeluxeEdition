# ShortestPathDeluxeEdition
# Files
- hierarchical_vertex_embeddings.npy
matriz de embeddings jerarquicos de numpy
-california_graph.gt
grafo de la bse de datos CaliforniaNodes 20k nodes 20k vertices de la librería graph_tool
# Code
- hierarchical.py
partición del grafo jerárquico random
- hierarchicalEmbeddings.py
utiliza el grafo particionado jerárquicamente y hace la matriz de embeddings correspondiente
- createGraph.py
usando la librería graph_tool carga de los archivos .txt los datos del grafo y lo guarda en un archivo .gt
- training.py
funciones de entrenamiento jerárquico: train_subgraph_embeddings, train_landmark_embeddings, train_high_error_embeddings.
- main.py
 lógica principal para calcular erroes y entrenamiento
