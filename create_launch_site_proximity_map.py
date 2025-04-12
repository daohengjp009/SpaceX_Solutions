import pandas as pd
import numpy as np
import folium
from folium import Marker, Icon, LayerControl, PolyLine
from folium.plugins import MeasureControl
import math

# Reuse launch sites from our previous scripts
launch_sites = {
    'KSC LC-39A': {'name': 'Kennedy Space Center Launch Complex 39A', 'lat': 28.6080, 'lon': -80.6043},
    'CCAFS SLC-40': {'name': 'Cape Canaveral Air Force Station Space Launch Complex 40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-4E': {'name': 'Vandenberg Air Force Base Space Launch Complex 4E', 'lat': 34.6332, 'lon': -120.6130},
    'CCAFS LC-40': {'name': 'Cape Canaveral Air Force Station Launch Complex 40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-3W': {'name': 'Vandenberg Air Force Base Space Launch Complex 3W', 'lat': 34.6364, 'lon': -120.5895},
    'KSC LC-39B': {'name': 'Kennedy Space Center Launch Complex 39B', 'lat': 28.6270, 'lon': -80.6208},
    'Kwajalein Atoll': {'name': 'Kwajalein Atoll Omelek Island', 'lat': 9.0477, 'lon': 167.7431}
}

# For this example, we'll focus on Kennedy Space Center Launch Complex 39A
selected_site_code = 'KSC LC-39A'
selected_site = launch_sites[selected_site_code]

# Function to calculate distance between two points using Haversine formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    radius = 6371  # Radius of the Earth in kilometers
    
    # Calculate the distance
    distance = radius * c
    
    return distance

# Create points of interest around KSC LC-39A
points_of_interest = {
    'Atlantic Ocean Coastline': {'lat': 28.6070, 'lon': -80.5772, 'type': 'Coastline'},
    'NASA Parkway': {'lat': 28.5807, 'lon': -80.6514, 'type': 'Highway'},
    'Kennedy Space Center Visitor Complex': {'lat': 28.5234, 'lon': -80.6820, 'type': 'Facility'},
    'Vehicle Assembly Building': {'lat': 28.5858, 'lon': -80.6508, 'type': 'Facility'},
    'SpaceX Landing Zone 1': {'lat': 28.4857, 'lon': -80.5431, 'type': 'Landing Site'},
    'Launch Control Center': {'lat': 28.5817, 'lon': -80.6483, 'type': 'Facility'}
}

# Calculate distances from the selected launch site to all points of interest
for name, point in points_of_interest.items():
    distance = calculate_distance(
        selected_site['lat'], selected_site['lon'],
        point['lat'], point['lon']
    )
    point['distance_km'] = distance
    point['distance_mi'] = distance * 0.621371  # Convert to miles

# Create a Folium map centered on the selected launch site
site_map = folium.Map(
    location=[selected_site['lat'], selected_site['lon']],
    zoom_start=12,
    tiles='CartoDB positron'
)

# Add marker for the launch site
folium.Marker(
    location=[selected_site['lat'], selected_site['lon']],
    popup=f"<b>{selected_site['name']}</b><br>Site code: {selected_site_code}",
    icon=folium.Icon(icon='rocket', prefix='fa', color='blue')
).add_to(site_map)

# Create feature groups for different types of POIs
coastline_fg = folium.FeatureGroup(name='Coastline')
highway_fg = folium.FeatureGroup(name='Highways')
facility_fg = folium.FeatureGroup(name='Facilities')
landing_fg = folium.FeatureGroup(name='Landing Sites')

# Add markers for points of interest with connection lines to the launch site
for name, point in points_of_interest.items():
    # Choose icon and color based on point type
    if point['type'] == 'Coastline':
        icon = folium.Icon(icon='water', prefix='fa', color='blue')
        feature_group = coastline_fg
        line_color = 'blue'
    elif point['type'] == 'Highway':
        icon = folium.Icon(icon='road', prefix='fa', color='gray')
        feature_group = highway_fg
        line_color = 'gray'
    elif point['type'] == 'Facility':
        icon = folium.Icon(icon='building', prefix='fa', color='orange')
        feature_group = facility_fg
        line_color = 'orange'
    elif point['type'] == 'Landing Site':
        icon = folium.Icon(icon='crosshairs', prefix='fa', color='green')
        feature_group = landing_fg
        line_color = 'green'
    else:
        icon = folium.Icon(icon='info', prefix='fa', color='purple')
        feature_group = site_map
        line_color = 'purple'
    
    # Add marker
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=f"<b>{name}</b><br>Type: {point['type']}<br>Distance: {point['distance_km']:.2f} km ({point['distance_mi']:.2f} mi)",
        icon=icon
    ).add_to(feature_group)
    
    # Add line connecting to launch site with distance popup
    folium.PolyLine(
        locations=[[selected_site['lat'], selected_site['lon']], [point['lat'], point['lon']]],
        color=line_color,
        weight=2,
        opacity=0.7,
        popup=f"Distance: {point['distance_km']:.2f} km ({point['distance_mi']:.2f} mi)"
    ).add_to(feature_group)

# Add feature groups to map
coastline_fg.add_to(site_map)
highway_fg.add_to(site_map)
facility_fg.add_to(site_map)
landing_fg.add_to(site_map)

# Add a measuring tool
site_map.add_child(MeasureControl())

# Add layer control
folium.LayerControl().add_to(site_map)

# Add a title
title_html = f'''
<h3 align="center" style="font-size:16px"><b>{selected_site['name']} Proximity Analysis</b></h3>
'''
site_map.get_root().html.add_child(folium.Element(title_html))

# Add a legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;
            border-radius: 5px;">
    <p><i class="fa fa-rocket fa-1x" style="color:blue"></i> Launch Site</p>
    <p><i class="fa fa-water fa-1x" style="color:blue"></i> Coastline</p>
    <p><i class="fa fa-road fa-1x" style="color:gray"></i> Highway</p>
    <p><i class="fa fa-building fa-1x" style="color:orange"></i> Facility</p>
    <p><i class="fa fa-crosshairs fa-1x" style="color:green"></i> Landing Site</p>
</div>
'''
site_map.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
site_map.save('launch_site_proximity_map.html')

# Print information about the selected site
print(f"Launch Site Proximity Analysis: {selected_site['name']}")
print("=" * 70)
print(f"Site Location: {selected_site['lat']}, {selected_site['lon']}")
print("\nNearby Points of Interest:")
print("-" * 70)
print(f"{'Point of Interest':<35} {'Type':<15} {'Distance (km)':<15} {'Distance (mi)':<15}")
print("-" * 70)

# Sort points of interest by distance
sorted_poi = sorted(points_of_interest.items(), key=lambda x: x[1]['distance_km'])

for name, point in sorted_poi:
    print(f"{name:<35} {point['type']:<15} {point['distance_km']:<15.2f} {point['distance_mi']:<15.2f}")

print("\nNote: Open 'launch_site_proximity_map.html' in a web browser to view the interactive map.") 