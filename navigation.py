from typing import List, Tuple, Dict
import time
import config
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

class NavigationSystem:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="islamabad_navigator")
        self.current_location = None
        self.remaining_destinations = []
        self.visited_destinations = []
        self.current_route = None
        
    def set_current_location(self, latitude: float, longitude: float):
        """Set the current location of the user."""
        self.current_location = (latitude, longitude)
        
    def set_destinations(self, destinations: List[Tuple[float, float]], destination_names: List[str] = None):
        """Set the list of destinations to visit."""
        self.remaining_destinations = list(zip(destinations, destination_names)) if destination_names else destinations
        self.visited_destinations = []
        self.current_route = None
        
    def get_next_destination(self) -> Tuple[Tuple[float, float], str]:
        """Get the next destination to visit."""
        if not self.remaining_destinations:
            return None, "No more destinations"
            
        if not self.current_location:
            return self.remaining_destinations[0], "Please set current location first"
            
        # Find the nearest destination
        nearest_dest = min(
            self.remaining_destinations,
            key=lambda x: geodesic(self.current_location, x[0]).kilometers
        )
        return nearest_dest
        
    def get_directions_to_next(self) -> Dict:
        """Get directions to the next destination."""
        if not self.current_location:
            return {"error": "Current location not set"}
            
        next_dest, dest_name = self.get_next_destination()
        if not next_dest:
            return {"error": "No more destinations"}
            
        try:
            # Calculate distance and estimated time
            distance = geodesic(self.current_location, next_dest[0]).kilometers
            # Assuming average speed of 40 km/h in Islamabad
            estimated_time = distance / 40 * 60  # in minutes
            
            return {
                "distance": f"{distance:.1f} km",
                "duration": f"{estimated_time:.0f} minutes",
                "next_destination": next_dest,
                "destination_name": dest_name,
                "estimated_speed": "40 km/h (average speed in Islamabad)"
            }
                
        except Exception as e:
            return {"error": str(e)}
            
    def mark_destination_reached(self):
        """Mark the current destination as reached and move to the next one."""
        if self.remaining_destinations:
            reached = self.remaining_destinations.pop(0)
            self.visited_destinations.append(reached)
            self.current_route = None
            return True
        return False
        
    def get_progress(self) -> Dict:
        """Get the current progress of the journey."""
        total = len(self.visited_destinations) + len(self.remaining_destinations)
        visited = len(self.visited_destinations)
        
        return {
            "total_destinations": total,
            "visited_destinations": visited,
            "remaining_destinations": len(self.remaining_destinations),
            "progress_percentage": (visited / total * 100) if total > 0 else 0
        }
        
    def get_remaining_destinations(self) -> List[Tuple[Tuple[float, float], str]]:
        """Get the list of remaining destinations."""
        return self.remaining_destinations
        
    def get_visited_destinations(self) -> List[Tuple[Tuple[float, float], str]]:
        """Get the list of visited destinations."""
        return self.visited_destinations 