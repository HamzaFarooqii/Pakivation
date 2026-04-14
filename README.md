# Pakivation - AI Route Optimizer

A Python application that optimizes delivery routes using Genetic Algorithms and visualizes them using OpenStreetMap.

## Features

- Genetic Algorithm-based route optimization
- Comparison with Greedy Algorithm
- Interactive map visualization using Folium
- Distance and cost calculations
- Progress tracking and visualization
- Support for custom city data

## Requirements

- Python 3.8+
- Required packages (install using `pip install -r requirements.txt`):
  - geopy
  - folium
  - pandas
  - numpy
  - tqdm
  - matplotlib

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Prepare your cities data in `cities.csv` with columns:
   - city: City name
   - latitude: Latitude coordinate
   - longitude: Longitude coordinate

## Usage

1. Run the main script:
   ```bash
   python main.py
   ```

2. The program will:
   - Load city data from cities.csv
   - Run the Genetic Algorithm optimization
   - Compare with Greedy Algorithm
   - Generate an interactive map (route_map.html)
   - Create a fitness history plot (fitness_history.png)
   - Display results in the console

## Output

- `route_map.html`: Interactive map showing the optimized route
- `fitness_history.png`: Plot showing the optimization progress
- Console output with:
  - Total distance
  - Comparison with greedy algorithm
  - Estimated cost
  - Optimized route sequence

## Customization

You can modify the following parameters in `config.py`:
- Genetic Algorithm parameters (population size, mutation rate, etc.)
- Map visualization settings
- Cost calculation parameters

## Example

The included `cities.csv` contains 10 major cities in Pakistan. You can modify this file to include your own cities or delivery points.

## License

MIT License 