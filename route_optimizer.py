import json
import numpy as np
from typing import List, Tuple
import folium
from geopy.distance import geodesic

class RouteOptimizer:
    def __init__(self, population_size: int = 100, mutation_rate: float = 0.1, generations: int = 100):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        
    def load_points(self, filename: str = 'selected_route.json') -> List[Tuple[float, float]]:
        """Load points from the saved route file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        return [(point['lat'], point['lng']) for point in data]
        
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate distance between two points using geodesic distance."""
        return geodesic(point1, point2).kilometers
        
    def calculate_route_distance(self, route: List[int], points: List[Tuple[float, float]]) -> float:
        """Calculate total distance of a route."""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.calculate_distance(points[route[i]], points[route[i + 1]])
        return total_distance
        
    def create_initial_population(self, num_points: int) -> List[List[int]]:
        """Create initial population of routes."""
        population = []
        for _ in range(self.population_size):
            route = list(range(num_points))
            np.random.shuffle(route)
            population.append(route)
        return population
        
    def mutate(self, route: List[int]) -> List[int]:
        """Mutate a route by swapping two random points."""
        if np.random.random() < self.mutation_rate:
            i, j = np.random.choice(len(route), 2, replace=False)
            route[i], route[j] = route[j], route[i]
        return route
        
    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Perform crossover between two parents to create a child route."""
        size = len(parent1)
        child = [-1] * size
        
        # Copy a random segment from parent1
        start, end = sorted(np.random.choice(size, 2, replace=False))
        child[start:end] = parent1[start:end]
        
        # Fill remaining positions with elements from parent2
        remaining = [x for x in parent2 if x not in child[start:end]]
        j = 0
        for i in range(size):
            if child[i] == -1:
                child[i] = remaining[j]
                j += 1
                
        return child
        
    def optimize(self, points: List[Tuple[float, float]]) -> Tuple[List[int], float]:
        """Optimize the route using genetic algorithm."""
        population = self.create_initial_population(len(points))
        best_route = None
        best_distance = float('inf')
        
        for generation in range(self.generations):
            # Calculate fitness for each route
            fitness_scores = []
            for route in population:
                distance = self.calculate_route_distance(route, points)
                fitness_scores.append(1 / distance)  # Higher fitness for shorter routes
                
            # Find best route
            best_idx = np.argmax(fitness_scores)
            current_best_distance = 1 / fitness_scores[best_idx]
            
            if current_best_distance < best_distance:
                best_distance = current_best_distance
                best_route = population[best_idx].copy()
                
            # Create new population
            new_population = [best_route]  # Elitism: keep the best route
            
            while len(new_population) < self.population_size:
                # Select parents using tournament selection
                parent1 = population[np.random.choice(len(population), p=fitness_scores/np.sum(fitness_scores))]
                parent2 = population[np.random.choice(len(population), p=fitness_scores/np.sum(fitness_scores))]
                
                # Create child through crossover and mutation
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
                
            population = new_population
            
        return best_route, best_distance
        
    def visualize_route(self, points: List[Tuple[float, float]], route: List[int], 
                       output_file: str = 'optimized_route.html'):
        """Visualize the optimized route on a map."""
        m = folium.Map(location=points[0], zoom_start=12)
        
        # Add markers for all points
        for i, point in enumerate(points):
            folium.Marker(
                point,
                popup=f'Point {i}',
                icon=folium.Icon(color='red' if i == 0 else 'blue')
            ).add_to(m)
            
        # Add lines for the route
        route_points = [points[i] for i in route]
        folium.PolyLine(
            route_points,
            color='blue',
            weight=2,
            opacity=1
        ).add_to(m)
        
        m.save(output_file)
        
def main():
    optimizer = RouteOptimizer()
    
    try:
        # Load points from the saved route
        points = optimizer.load_points()
        
        if len(points) < 2:
            print("Error: Need at least 2 points to optimize a route")
            return
            
        # Optimize the route
        best_route, best_distance = optimizer.optimize(points)
        
        print(f"\nOptimized Route:")
        print(f"Total Distance: {best_distance:.2f} km")
        print("\nRoute Sequence:")
        for i, point_idx in enumerate(best_route):
            print(f"{i+1}. Point {point_idx}: {points[point_idx]}")
            
        # Visualize the route
        optimizer.visualize_route(points, best_route)
        print("\nRoute visualization saved to 'optimized_route.html'")
        
    except FileNotFoundError:
        print("Error: No route file found. Please select points on the map first.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 