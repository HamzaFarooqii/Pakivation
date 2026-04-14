from flask import Flask, render_template, request, jsonify
import os
import json
from route_optimizer import RouteOptimizer

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page with the map."""
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    """Run the Genetic Algorithm to optimize the selected route."""
    data = request.json
    selected_points = data.get('points', [])
    
    if len(selected_points) < 2:
        return jsonify({"error": "Need at least 2 points to optimize."}), 400
        
    # Save route for persistence/debugging (as it used to do)
    with open('selected_route.json', 'w') as f:
        json.dump(selected_points, f)
        
    # Prepare points for the optimizer -> List[Tuple[float, float]]
    points_tuple = [(point['lat'], point['lng']) for point in selected_points]
    
    # Initialize Route Optimizer
    optimizer = RouteOptimizer(population_size=100, generations=50) # using slightly lower generations for faster web response
    
    # Run the genetic algorithm
    best_route, best_distance = optimizer.optimize(points_tuple)
    
    # Convert numpy types to native Python ints for JSON serialization
    best_route = [int(i) for i in best_route]
    
    # Reorder coordinates based on GA result
    optimized_coords = [[points_tuple[i][0], points_tuple[i][1]] for i in best_route]
    
    # If it's a TSP, it should loop back to the start
    optimized_coords.append(optimized_coords[0]) 

    return jsonify({
        "status": "success",
        "optimized_coords": optimized_coords,
        "distance": round(best_distance, 2)
    })

def main():
    # Make sure templates dir exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    # Run the Flask app
    app.run(debug=True)

if __name__ == '__main__':
    main()