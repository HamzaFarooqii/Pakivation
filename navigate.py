import pandas as pd
from navigation import NavigationSystem
import time
import folium
from map_visualizer import create_route_map, save_map

def load_destinations(filename: str = 'cities.csv'):
    """Load destinations from CSV file."""
    df = pd.read_csv(filename)
    destinations = list(zip(df['latitude'], df['longitude']))
    names = df['city'].tolist()
    return destinations, names

def get_current_location():
    """Get current location from user input."""
    print("\nEnter your current location in Islamabad:")
    print("Example coordinates for reference:")
    print("Faisal Mosque: 33.7294, 73.0391")
    print("Blue Area: 33.7294, 73.0391")
    print("Centaurus Mall: 33.7294, 73.0391")
    
    try:
        lat = float(input("Latitude: "))
        lon = float(input("Longitude: "))
        return lat, lon
    except ValueError:
        print("Invalid input. Please enter valid coordinates.")
        return get_current_location()

def main():
    # Initialize navigation system
    nav = NavigationSystem()
    
    # Load destinations
    print("Loading Islamabad destinations...")
    destinations, names = load_destinations()
    nav.set_destinations(destinations, names)
    
    # Get current location
    current_location = get_current_location()
    nav.set_current_location(*current_location)
    
    print("\nNavigation started in Islamabad!")
    print("Type 'quit' to exit, 'next' to mark destination as reached")
    print("Available destinations:")
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")
    
    while True:
        # Get next destination and directions
        next_dest, message = nav.get_next_destination()
        if not next_dest:
            print("\nAll destinations have been visited!")
            break
            
        directions = nav.get_directions_to_next()
        if "error" in directions:
            print(f"\nError: {directions['error']}")
            break
            
        # Display information
        print("\n" + "="*50)
        print(f"Next Destination: {directions['destination_name']}")
        print(f"Distance: {directions['distance']}")
        print(f"Estimated Duration: {directions['duration']}")
        print(f"Note: {directions['estimated_speed']}")
        
        # Show progress
        progress = nav.get_progress()
        print(f"\nProgress: {progress['progress_percentage']:.1f}%")
        print(f"Visited: {progress['visited_destinations']}/{progress['total_destinations']}")
        
        # Create and save map
        m = create_route_map(
            [current_location] + [d[0] for d in nav.get_remaining_destinations()],
            [0] + list(range(1, len(nav.get_remaining_destinations()) + 1)),
            ["Current Location"] + [d[1] for d in nav.get_remaining_destinations()]
        )
        save_map(m, "islamabad_route.html")
        print("\nMap updated: islamabad_route.html")
        
        # Wait for user input
        command = input("\nEnter command (next/quit): ").lower()
        if command == 'quit':
            break
        elif command == 'next':
            nav.mark_destination_reached()
            print("\nDestination marked as reached!")
        else:
            print("Invalid command. Use 'next' or 'quit'.")
            
        # Update current location
        print("\nUpdate current location? (y/n)")
        if input().lower() == 'y':
            current_location = get_current_location()
            nav.set_current_location(*current_location)
            
        time.sleep(1)  # Small delay to prevent too frequent API calls
    
    # Final summary
    print("\nNavigation Summary:")
    print(f"Total destinations visited: {len(nav.get_visited_destinations())}")
    print("\nVisited destinations:")
    for i, dest in enumerate(nav.get_visited_destinations(), 1):
        print(f"{i}. {dest[1]}")

if __name__ == "__main__":
    main() 