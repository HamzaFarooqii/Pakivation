import folium
from folium import plugins
import pandas as pd
import json
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def load_locations():
    """Load locations from CSV file."""
    df = pd.read_csv('cities.csv')
    return df.to_dict('records')

def create_map():
    """Create the initial map centered on Islamabad."""
    m = folium.Map(
        location=[33.6844, 73.0479],  # Center of Islamabad
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add a layer control
    folium.LayerControl().add_to(m)
    
    # Add a fullscreen option
    plugins.Fullscreen().add_to(m)
    
    return m

@app.route('/')
def index():
    """Render the main page with the map."""
    locations = load_locations()
    return render_template('index.html', locations=locations)

@app.route('/save_route', methods=['POST'])
def save_route():
    """Save the selected route."""
    data = request.json
    selected_points = data.get('points', [])
    
    # Save the selected points to a file
    with open('selected_route.json', 'w') as f:
        json.dump(selected_points, f)
    
    return jsonify({"status": "success"})

def main():
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Create the HTML template
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Islamabad Route Planner</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        #map { height: 600px; }
        .control-panel {
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .selected-points {
            margin-top: 20px;
        }
        .point-list {
            max-height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Islamabad Route Planner</h1>
        
        <div class="control-panel">
            <h3>Instructions:</h3>
            <ol>
                <li>Click on the map to set your starting point (red marker)</li>
                <li>Click on the map to add delivery points (blue markers)</li>
                <li>Use the buttons below to manage your route</li>
            </ol>
            <button onclick="clearRoute()">Clear Route</button>
            <button onclick="saveRoute()">Save Route</button>
            <button onclick="optimizeRoute()">Optimize Route</button>
        </div>

        <div id="map"></div>

        <div class="selected-points">
            <h3>Selected Points:</h3>
            <div class="point-list" id="pointList"></div>
        </div>
    </div>

    <script>
        // Initialize the map
        var map = L.map('map').setView([33.6844, 73.0479], 12);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Store markers and points
        var startMarker = null;
        var deliveryMarkers = [];
        var selectedPoints = [];

        // Add click handler to map
        map.on('click', function(e) {
            if (!startMarker) {
                // Set starting point
                startMarker = L.marker(e.latlng, {
                    icon: L.divIcon({
                        className: 'start-marker',
                        html: '🚗',
                        iconSize: [30, 30]
                    })
                }).addTo(map);
                selectedPoints.push({
                    type: 'start',
                    lat: e.latlng.lat,
                    lng: e.latlng.lng
                });
            } else {
                // Add delivery point
                var marker = L.marker(e.latlng, {
                    icon: L.divIcon({
                        className: 'delivery-marker',
                        html: '📦',
                        iconSize: [30, 30]
                    })
                }).addTo(map);
                deliveryMarkers.push(marker);
                selectedPoints.push({
                    type: 'delivery',
                    lat: e.latlng.lat,
                    lng: e.latlng.lng
                });
            }
            updatePointList();
        });

        function updatePointList() {
            var list = document.getElementById('pointList');
            list.innerHTML = '';
            selectedPoints.forEach((point, index) => {
                var div = document.createElement('div');
                div.innerHTML = `${index + 1}. ${point.type === 'start' ? 'Starting Point' : 'Delivery Point'}: ${point.lat.toFixed(4)}, ${point.lng.toFixed(4)}`;
                list.appendChild(div);
            });
        }

        function clearRoute() {
            if (startMarker) {
                map.removeLayer(startMarker);
                startMarker = null;
            }
            deliveryMarkers.forEach(marker => map.removeLayer(marker));
            deliveryMarkers = [];
            selectedPoints = [];
            updatePointList();
        }

        function saveRoute() {
            fetch('/save_route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ points: selectedPoints })
            })
            .then(response => response.json())
            .then(data => {
                alert('Route saved successfully!');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error saving route');
            });
        }

        function optimizeRoute() {
            if (selectedPoints.length < 2) {
                alert('Please select at least one delivery point');
                return;
            }
            saveRoute();
            // Here you would typically call your genetic algorithm
            alert('Route optimization started! Check the console for results.');
        }
    </script>
</body>
</html>
        ''')
    
    # Run the Flask app
    app.run(debug=True)

if __name__ == '__main__':
    main() 