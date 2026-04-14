import numpy as np
import random
from typing import List, Tuple
from tqdm import tqdm
import config
from distance_utils import calculate_route_distance

class GASolver:
    def __init__(self, distance_matrix: np.ndarray):
        self.distance_matrix = distance_matrix
        self.n_cities = len(distance_matrix)
        self.population_size = config.POPULATION_SIZE
        self.mutation_rate = config.MUTATION_RATE
        self.tournament_size = config.TOURNAMENT_SIZE
        
    def initialize_population(self) -> List[List[int]]:
        """Initialize a population of random routes."""
        population = []
        for _ in range(self.population_size):
            route = list(range(self.n_cities))
            random.shuffle(route)
            population.append(route)
        return population
    
    def tournament_selection(self, population: List[List[int]], fitness_values: List[float]) -> List[int]:
        """Select a route using tournament selection."""
        tournament = random.sample(list(zip(population, fitness_values)), self.tournament_size)
        return min(tournament, key=lambda x: x[1])[0]
    
    def ordered_crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """Perform ordered crossover between two parents."""
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        
        def create_child(p1: List[int], p2: List[int]) -> List[int]:
            child = [-1] * size
            child[start:end] = p1[start:end]
            remaining = [x for x in p2 if x not in child[start:end]]
            j = 0
            for i in range(size):
                if child[i] == -1:
                    child[i] = remaining[j]
                    j += 1
            return child
        
        child1 = create_child(parent1, parent2)
        child2 = create_child(parent2, parent1)
        return child1, child2
    
    def swap_mutation(self, route: List[int]) -> List[int]:
        """Perform swap mutation on a route."""
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(len(route)), 2)
            route[i], route[j] = route[j], route[i]
        return route
    
    def calculate_fitness(self, route: List[int]) -> float:
        """Calculate the fitness (total distance) of a route."""
        return calculate_route_distance(route, self.distance_matrix)
    
    def run(self) -> Tuple[List[int], float, List[float]]:
        """Run the genetic algorithm."""
        population = self.initialize_population()
        best_fitness_history = []
        best_route = None
        best_fitness = float('inf')
        generations_without_improvement = 0
        
        for generation in tqdm(range(config.MAX_GENERATIONS), desc="Optimizing route"):
            # Calculate fitness for all routes
            fitness_values = [self.calculate_fitness(route) for route in population]
            
            # Update best route
            min_fitness_idx = np.argmin(fitness_values)
            if fitness_values[min_fitness_idx] < best_fitness:
                best_fitness = fitness_values[min_fitness_idx]
                best_route = population[min_fitness_idx].copy()
                generations_without_improvement = 0
            else:
                generations_without_improvement += 1
            
            best_fitness_history.append(best_fitness)
            
            # Check termination condition
            if generations_without_improvement >= config.NO_IMPROVEMENT_LIMIT:
                break
            
            # Create new population
            new_population = []
            while len(new_population) < self.population_size:
                # Selection
                parent1 = self.tournament_selection(population, fitness_values)
                parent2 = self.tournament_selection(population, fitness_values)
                
                # Crossover
                child1, child2 = self.ordered_crossover(parent1, parent2)
                
                # Mutation
                child1 = self.swap_mutation(child1)
                child2 = self.swap_mutation(child2)
                
                new_population.extend([child1, child2])
            
            # Ensure population size is maintained
            population = new_population[:self.population_size]
        
        return best_route, best_fitness, best_fitness_history 