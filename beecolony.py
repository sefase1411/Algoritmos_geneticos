import numpy as np
import random
import copy
import sys
import tsp_loader
from enum import Enum

num_bees = 50
max_epochs = 700

class Status(Enum):
    inactive = 0
    active = 1
    scout = 2

class Bee:
    def __init__(self, num_cities):
        self.status = Status.inactive
        self.path = list(range(num_cities))
        random.shuffle(self.path)
        self.error = self.tour_length()

    def tour_length(self):
        length = sum(distances[self.path[i]][self.path[i+1]] for i in range(len(self.path) - 1))
        length += distances[self.path[-1]][self.path[0]]
        return length

def solve(num_cities):
    global distances

    hive = [Bee(num_cities) for _ in range(num_bees)]
    best_bee = min(hive, key=lambda bee: bee.error)
    best_path = best_bee.path[:]
    best_length = best_bee.error

    num_active = int(num_bees * 0.50)
    num_scout = int(num_bees * 0.25)
    num_inactive = num_bees - (num_active + num_scout)

    for i in range(num_bees):
        if i < num_inactive:
            hive[i].status = Status.inactive
        elif i < num_inactive + num_scout:
            hive[i].status = Status.scout
        else:
            hive[i].status = Status.active

    for epoch in range(max_epochs):
        for bee in hive:
            if bee.status == Status.active:
                new_path = copy.copy(bee.path)
                i, j = random.sample(range(num_cities), 2)
                new_path[i], new_path[j] = new_path[j], new_path[i]
                
                new_length = sum(distances[new_path[k]][new_path[k+1]] for k in range(num_cities - 1))
                new_length += distances[new_path[-1]][new_path[0]]

                if new_length < bee.error or random.random() < 0.05:
                    bee.path = new_path
                    bee.error = new_length

                    if bee.error < best_length:
                        best_length = bee.error
                        best_path = bee.path[:]
                        print(f"Iteración {epoch+1}: Nueva mejor ruta encontrada con longitud {best_length:.6f}")

            elif bee.status == Status.scout:
                random_path = list(range(num_cities))
                random.shuffle(random_path)
                
                random_length = sum(distances[random_path[k]][random_path[k+1]] for k in range(num_cities - 1))
                random_length += distances[random_path[-1]][random_path[0]]

                if random_length < bee.error:
                    bee.path = random_path
                    bee.error = random_length

                    if bee.error < best_length:
                        best_length = bee.error
                        best_path = bee.path[:]
                        print(f"Iteración {epoch+1}: Nueva mejor ruta encontrada con longitud {best_length:.6f}")

    print("\nMejor recorrido encontrado:", best_path)
    print(f"Longitud del mejor recorrido: {best_length:.6f}")

def main():
    file_name = input("Ingrese el nombre del archivo .tsp (ejemplo: berlin52.tsp): ")
    cities = tsp_loader.load_tsp_file(file_name)
    global distances
    distances = tsp_loader.compute_distance_matrix(cities)

    solve(len(distances))

if __name__ == "__main__":
    main()
