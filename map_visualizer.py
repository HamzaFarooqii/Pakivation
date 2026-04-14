import folium
from typing import List, Tuple
import config

def create_route_map(cities: List[Tuple[float, float]], 
                    route: List[int], 
                    city_names: List[str] = None) -> folium.Map:
    """
    Create an interactive map showing the optimized route.
    
    Args:
        cities: List of (latitude, longitude) tuples
        route: List of city indices in the order to visit
        city_names: Optional list of city names for markers
        
    Returns:
        folium.Map: Interactive map with route visualization
    """
    # Calculate center of the map
    center_lat = sum(lat for lat, _ in cities) / len(cities)
    center_lon = sum(lon for _, lon in cities) / len(cities)
    
    # Create the map
    m = folium.Map(location=[center_lat, center_lon], 
                  zoom_start=config.MAP_ZOOM)
    
    # Add markers for each city
    for i, (lat, lon) in enumerate(cities):
        # Create popup text
        if city_names:
            popup_text = f"{i+1}. {city_names[i]}"
        else:
            popup_text = f"City {i+1}"
        
        # Add marker
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            icon=folium.Icon(color=config.MARKER_COLOR, icon='info-sign')
        ).add_to(m)
    
    # Create route coordinates
    route_coords = [cities[i] for i in route]
    # Add the return to start
    route_coords.append(cities[route[0]])
    
    # Add the route line
    folium.PolyLine(
        route_coords,
        color=config.ROUTE_COLOR,
        weight=2,
        opacity=1
    ).add_to(m)
    
    return m

def save_map(m: folium.Map, filename: str = "route_map.html"):
    """Save the map to an HTML file."""
    m.save(filename) 