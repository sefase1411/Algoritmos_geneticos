import numpy as np
import random
import tsp_loader  

# tsp_loader.py
num_iterations = 700
num_ants = 50
alpha = 2.0
beta = 5.0
rho = 0.3
Q = 500

def initialize_pheromones(num_cities):
    """Inicializa la matriz de feromonas con un valor pequeño."""
    return np.ones((num_cities, num_cities)) * 0.1

def probability_distribution(pheromones, distances, current_city, allowed_cities):
    """Calcula la probabilidad de moverse a cada ciudad no visitada."""
    probabilities = []
    for city in allowed_cities:
        tau = pheromones[current_city][city] ** alpha  # Feromonas
        eta = (1.0 / distances[current_city][city]) ** beta  # Heurística (distancia inversa)
        probabilities.append(tau * eta)
    probabilities = np.array(probabilities)
    return probabilities / probabilities.sum()

def construct_solution(pheromones, distances, num_cities):
    """Cada hormiga construye una solución recorriendo las ciudades."""
    start_city = random.randint(0, num_cities - 1)
    tour = [start_city]
    allowed_cities = list(range(num_cities))
    allowed_cities.remove(start_city)
    
    while allowed_cities:
        current_city = tour[-1]
        probabilities = probability_distribution(pheromones, distances, current_city, allowed_cities)
        next_city = np.random.choice(allowed_cities, p=probabilities)
        tour.append(next_city)
        allowed_cities.remove(next_city)
    
    return tour

def tour_length(tour, distances):
    """Calcula la longitud total de un recorrido."""
    length = sum(distances[tour[i]][tour[i+1]] for i in range(len(tour) - 1))
    length += distances[tour[-1]][tour[0]]  # Volver a la ciudad inicial
    return length

def update_pheromones(pheromones, all_tours, all_lengths):
    """Actualiza la matriz de feromonas basada en los recorridos de las hormigas."""
    pheromones *= (1 - rho)  # Evaporación
    for tour, length in zip(all_tours, all_lengths):
        for i in range(len(tour) - 1):
            pheromones[tour[i]][tour[i+1]] += Q / length
            pheromones[tour[i+1]][tour[i]] += Q / length

def aco_algorithm(distances):
    """Ejecuta el algoritmo ACO sobre la matriz de distancias."""
    num_cities = len(distances)
    pheromones = initialize_pheromones(num_cities)
    
    best_tour = None
    best_length = float('inf')
    
    for iteration in range(num_iterations):
        all_tours = [construct_solution(pheromones, distances, num_cities) for _ in range(num_ants)]
        all_lengths = [tour_length(tour, distances) for tour in all_tours]
        
        min_length = min(all_lengths)
        if min_length < best_length:
            best_length = min_length
            best_tour = all_tours[all_lengths.index(min_length)]
            print(f"Iteración {iteration+1}: Nueva mejor ruta encontrada con longitud {best_length}")
        
        update_pheromones(pheromones, all_tours, all_lengths)
    
    return best_tour, best_length

def main():
    """Carga los datos y ejecuta ACO."""
    file_name = input("Ingrese el nombre del archivo .tsp (ejemplo: berlin52.tsp): ")
    cities = tsp_loader.load_tsp_file(file_name)
    distances = tsp_loader.compute_distance_matrix(cities)
    
    best_tour, best_length = aco_algorithm(distances)
    print(f"\nMejor recorrido encontrado: {best_tour}")
    print(f"Longitud del mejor recorrido: {best_length}")

if __name__ == "__main__":
    main()
