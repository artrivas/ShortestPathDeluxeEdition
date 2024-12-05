import pandas as pd
import random

def select_random_nodes(nodes_file,output_file="RandomSelect.txt", num_nodes=100):
    # Cargar el archivo de nodos
    nodes_df = pd.read_csv(nodes_file, sep=" ", header=None, names=["id", "longitude", "latitude"])    
    # Verificar que haya suficientes nodos para seleccionar
    if num_nodes > len(nodes_df):
        raise ValueError(f"No hay suficientes nodos en el archivo para seleccionar {num_nodes}. Total disponible: {len(nodes_df)}")
    
    # Seleccionar nodos aleatoriamente
    selected_nodes = nodes_df.sample(n=num_nodes, random_state=42).reset_index(drop=True)
    
    selected_nodes.to_csv(output_file, sep=" ", index=False, header=False)
    print(f"Nodos seleccionados guardados en {output_file}")

    return selected_nodes

# Uso de la función
nodes_file_path = "./CaliforniaNodesCoordinates.txt"
selected_nodes = select_random_nodes(nodes_file_path,"RandomSelect.txt", 100)

print("Nodos seleccionados:")
print(selected_nodes)
