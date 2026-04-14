import pandas as pd
import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
from distance_utils import calculate_distance_matrix, calculate_route_cost
from ga_solver import GASolver
from map_visualizer import create_route_map, save_map
import config

def load_cities_from_csv(filename: str) -> Tuple[List[Tuple[float, float]], List[str]]:
    """Load city data from a CSV file."""
    df = pd.read_csv(filename)
    cities = list(zip(df['latitude'], df['longitude']))
    city_names = df['city'].tolist()
    return cities, city_names

def greedy_algorithm(distance_matrix: np.ndarray) -> Tuple[List[int], float]:
    """Implement a simple greedy algorithm for comparison."""
    n = len(distance_matrix)
    unvisited = set(range(1, n))
    current = 0
    route = [current]
    total_distance = 0
    
    while unvisited:
        next_city = min(unvisited, key=lambda x: distance_matrix[current][x])
        total_distance += distance_matrix[current][next_city]
        current = next_city
        route.append(current)
        unvisited.remove(current)
    
    # Add return to start
    total_distance += distance_matrix[current][0]
    route.append(0)
    
    return route, total_distance

def plot_fitness_history(fitness_history: List[float], filename: str = "fitness_history.png"):
    """Plot the fitness history of the genetic algorithm."""
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history)
    plt.title('Fitness History')
    plt.xlabel('Generation')
    plt.ylabel('Total Distance (km)')
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def main():
    # Load cities from CSV
    try:
        cities, city_names = load_cities_from_csv('cities.csv')
    except FileNotFoundError:
        print("Error: cities.csv not found. Please create a CSV file with columns: city,latitude,longitude")
        return
    
    # Calculate distance matrix
    distance_matrix = calculate_distance_matrix(cities)
    
    # Run genetic algorithm
    print("\nRunning Genetic Algorithm...")
    ga_solver = GASolver(distance_matrix)
    best_route, best_distance, fitness_history = ga_solver.run()
    
    # Run greedy algorithm for comparison
    print("\nRunning Greedy Algorithm...")
    greedy_route, greedy_distance = greedy_algorithm(distance_matrix)
    
    # Print results
    print("\nResults:")
    print(f"Genetic Algorithm - Total Distance: {best_distance:.2f} km")
    print(f"Greedy Algorithm - Total Distance: {greedy_distance:.2f} km")
    print(f"Improvement: {((greedy_distance - best_distance) / greedy_distance * 100):.2f}%")
    
    # Calculate cost
    cost = calculate_route_cost(best_distance, config.FUEL_RATE_PER_KM)
    print(f"Estimated Cost: ${cost:.2f}")
    
    # Create and save map
    print("\nGenerating route map...")
    m = create_route_map(cities, best_route, city_names)
    save_map(m)
    print("Map saved as route_map.html")
    
    # Plot fitness history
    plot_fitness_history(fitness_history)
    print("Fitness history plot saved as fitness_history.png")
    
    # Print route
    print("\nOptimized Route:")
    for i, city_idx in enumerate(best_route):
        print(f"{i+1}. {city_names[city_idx]}")

if __name__ == "__main__":
    main() 