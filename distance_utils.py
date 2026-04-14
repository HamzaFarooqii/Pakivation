from geopy.distance import geodesic
import numpy as np
from typing import List, Tuple
import googlemaps
import config
import time

def get_google_maps_client() -> googlemaps.Client:
    """Initialize and return Google Maps client."""
    if not config.GOOGLE_MAPS_API_KEY:
        raise ValueError("Google Maps API key is required. Please add it to config.py")
    return googlemaps.Client(key=config.GOOGLE_MAPS_API_KEY)

def calculate_distance_matrix(cities: List[Tuple[float, float]]) -> np.ndarray:
    """
    Calculate the distance matrix between all pairs of cities using Google Maps Distance Matrix API.
    Falls back to Haversine formula if API fails.
    
    Args:
        cities: List of (latitude, longitude) tuples
        
    Returns:
        numpy.ndarray: Distance matrix where matrix[i][j] is the distance between city i and j
    """
    n = len(cities)
    distance_matrix = np.zeros((n, n))
    
    try:
        # Initialize Google Maps client
        gmaps = get_google_maps_client()
        
        # Convert coordinates to addresses or use them directly
        origins = [f"{lat},{lon}" for lat, lon in cities]
        destinations = origins.copy()
        
        # Make API request
        result = gmaps.distance_matrix(
            origins=origins,
            destinations=destinations,
            mode="driving",
            units="metric"
        )
        
        # Process results
        for i in range(n):
            for j in range(n):
                if i != j:
                    try:
                        # Extract distance in kilometers
                        distance = result['rows'][i]['elements'][j]['distance']['value'] / 1000
                        distance_matrix[i][j] = distance
                    except (KeyError, TypeError):
                        # Fallback to Haversine if API result is invalid
                        distance = geodesic(cities[i], cities[j]).kilometers
                        distance_matrix[i][j] = distance
                else:
                    distance_matrix[i][j] = 0
                    
        # Add a small delay to respect API rate limits
        time.sleep(0.1)
        
    except Exception as e:
        print(f"Warning: Google Maps API failed: {str(e)}")
        print("Falling back to Haversine distance calculation...")
        
        # Fallback to Haversine formula
        for i in range(n):
            for j in range(i + 1, n):
                distance = geodesic(cities[i], cities[j]).kilometers
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
    
    return distance_matrix

def calculate_route_distance(route: List[int], distance_matrix: np.ndarray) -> float:
    """
    Calculate the total distance of a route.
    
    Args:
        route: List of city indices in the order to visit
        distance_matrix: Pre-calculated distance matrix
        
    Returns:
        float: Total distance of the route
    """
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    # Add distance back to starting point
    total_distance += distance_matrix[route[-1]][route[0]]
    return total_distance

def calculate_route_cost(distance: float, fuel_rate: float) -> float:
    """
    Calculate the cost of a route based on distance and fuel rate.
    
    Args:
        distance: Total distance in kilometers
        fuel_rate: Cost per kilometer
        
    Returns:
        float: Total cost of the route
    """
    return distance * fuel_rate 