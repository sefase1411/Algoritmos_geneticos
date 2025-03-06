import numpy as np
import random
import tsp_loader
from deap import base, creator, tools, algorithms

# Parámetros similares a ACO
pop_size = 50   # Tamaño de la población
num_generations = 700  # Número de generaciones
cx_prob = 0.8  # Probabilidad de cruce
mut_prob = 0.3  # Probabilidad de mutación

def evaluate(individual, distances):
    """Evalúa un individuo calculando la longitud total del recorrido."""
    length = sum(distances[individual[i-1]][individual[i]] for i in range(len(individual)))
    length += distances[individual[-1]][individual[0]]  # Volver a la ciudad inicial
    return (length,)

def main():
    """Carga los datos y ejecuta el algoritmo genético."""
    file_name = input("Ingrese el nombre del archivo .tsp (ejemplo: berlin52.tsp): ")
    cities = tsp_loader.load_tsp_file(file_name)
    distances = tsp_loader.compute_distance_matrix(cities)
    num_cities = len(cities)
    
    # Definir estructura de optimización
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(num_cities), num_cities)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.3)
    toolbox.register("select", tools.selTournament, tournsize=5)
    toolbox.register("evaluate", evaluate, distances=distances)
    
    # Inicializar población
    population = toolbox.population(n=pop_size)
    
    # Algoritmo evolutivo
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    hall_of_fame = tools.HallOfFame(1)
    
    algorithms.eaSimple(population, toolbox, cxpb=cx_prob, mutpb=mut_prob, ngen=num_generations, 
                        stats=stats, halloffame=hall_of_fame, verbose=True)
    
    best_solution = hall_of_fame[0]
    best_distance = evaluate(best_solution, distances)[0]
    
    print("\nMejor recorrido encontrado:", best_solution)
    print("Longitud del mejor recorrido:", best_distance)

if __name__ == "__main__":
    main()
