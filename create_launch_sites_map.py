import pandas as pd
import numpy as np
import folium
from folium import Marker, Icon

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

# Create a folium map centered on United States
spacex_map = folium.Map(
    location=[39.8283, -98.5795],  # Approximate center of the US
    zoom_start=3,
    tiles='OpenStreetMap'
)

# Add markers for each launch site
for site_code, site_info in launch_sites.items():
    # Create a custom icon for SpaceX launch sites
    icon = Icon(
        icon='rocket',
        prefix='fa',
        color='white',
        icon_color='#005288'  # SpaceX blue
    )
    
    # Add marker with popup information
    Marker(
        location=[site_info['lat'], site_info['lon']],
        popup=f"<strong>{site_info['name']}</strong><br>Site code: {site_code}",
        icon=icon
    ).add_to(spacex_map)

# Add a title to the map
title_html = '''
<h3 align="center" style="font-size:16px"><b>SpaceX Launch Sites Worldwide</b></h3>
'''
spacex_map.get_root().html.add_child(folium.Element(title_html))

# Add a legend to the map
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;
            border-radius: 5px;">
    <p><i class="fa fa-rocket fa-1x" style="color:#005288"></i> SpaceX Launch Site</p>
</div>
'''
spacex_map.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
spacex_map.save('spacex_launch_sites_map.html')

print("Launch sites map created successfully! Open 'spacex_launch_sites_map.html' in a web browser to view.")
print("\nLaunch Sites Information:")
print("=" * 50)
for site_code, site_info in launch_sites.items():
    print(f"Site: {site_info['name']} ({site_code})")
    print(f"Location: {site_info['lat']}, {site_info['lon']}")
    print("-" * 30) 