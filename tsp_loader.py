import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def load_tsp_file(file_path):
    """Carga un archivo .tsp y extrae las coordenadas de las ciudades."""
    cities = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    node_section = False
    for line in lines:
        line = line.strip()
        if line.startswith("NODE_COORD_SECTION"):
            node_section = True
            continue
        elif line.startswith("EOF"):
            break
        elif node_section:
            parts = line.split()
            if len(parts) == 3:
                city_id = int(parts[0])
                x, y = float(parts[1]), float(parts[2])
                cities[city_id] = (x, y)
    
    return cities

def compute_distance_matrix(cities):
    """Calcula la matriz de distancias euclidianas entre ciudades."""
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))
    
    def euclidean_distance(p1, p2):
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = euclidean_distance(cities[i+1], cities[j+1])
    
    return distance_matrix

def save_to_txt(file_name, cities, distance_matrix):
    """Guarda la información en un archivo de texto."""
    with open(file_name, 'w') as f:
        f.write("Coordenadas de las ciudades:\n")
        for city, coord in cities.items():
            f.write(f"Ciudad {city}: {coord}\n")
        
        f.write("\nMatriz de Distancias:\n")
        np.savetxt(f, distance_matrix, fmt="%.2f")
    print(f"La información ha sido guardada en {file_name}")

def plot_graph(cities, distance_matrix):
    """Dibuja el grafo de ciudades y sus conexiones."""
    G = nx.Graph()
    
    for city, coord in cities.items():
        G.add_node(city, pos=coord)
    
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            G.add_edge(i + 1, j + 1, weight=round(distance_matrix[i][j], 2))
    
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=300, font_size=8, font_color='red')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6)
    plt.title("Grafo de Ciudades y Distancias")
    plt.show()

def main():
    """Ejecuta la carga y representación del TSP."""
    file_name = input("Ingrese el nombre del archivo .tsp (ejemplo: berlin52.tsp): ")
    file_path = os.path.join(os.getcwd(), file_name)
    
    if not os.path.exists(file_path):
        print("Error: El archivo no existe en el directorio actual.")
        return
    
    cities = load_tsp_file(file_path)
    distance_matrix = compute_distance_matrix(cities)
    
    output_file = file_name.replace(".tsp", "_output.txt")
    save_to_txt(output_file, cities, distance_matrix)
    
    plot_graph(cities, distance_matrix)

if __name__ == "__main__":
    main()
