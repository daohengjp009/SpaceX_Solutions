import pandas as pd
import numpy as np
import folium
from folium import Marker, Icon, LayerControl
from folium.plugins import MarkerCluster

# Reuse data generation code similar to previous scripts
np.random.seed(42)

# Create a list of all potential launch sites
launch_sites = {
    'KSC LC-39A': {'name': 'Kennedy Space Center Launch Complex 39A', 'lat': 28.6080, 'lon': -80.6043},
    'CCAFS SLC-40': {'name': 'Cape Canaveral Air Force Station Space Launch Complex 40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-4E': {'name': 'Vandenberg Air Force Base Space Launch Complex 4E', 'lat': 34.6332, 'lon': -120.6130},
    'CCAFS LC-40': {'name': 'Cape Canaveral Air Force Station Launch Complex 40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-3W': {'name': 'Vandenberg Air Force Base Space Launch Complex 3W', 'lat': 34.6364, 'lon': -120.5895},
    'KSC LC-39B': {'name': 'Kennedy Space Center Launch Complex 39B', 'lat': 28.6270, 'lon': -80.6208},
    'Kwajalein Atoll': {'name': 'Kwajalein Atoll Omelek Island', 'lat': 9.0477, 'lon': 167.7431}
}

# Generate sample launch data
def generate_launch_data(num_launches=100):
    flight_numbers = np.arange(1, num_launches + 1)
    dates = pd.date_range(start='2010-06-04', end='2022-12-31', periods=num_launches)
    
    # Randomly assign launch sites
    site_codes = list(launch_sites.keys())
    site_probabilities = [0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02]  # Probability for each site
    launch_site_codes = np.random.choice(site_codes, size=num_launches, p=site_probabilities)
    
    # Generate mission outcomes (success/failure) - success rate improves over time
    mission_outcomes = []
    for date in dates:
        if date.year <= 2013:  # Early years
            success_prob = 0.85
        elif date.year <= 2016:  # Middle years
            success_prob = 0.94
        else:  # Recent years
            success_prob = 0.98
        
        mission_outcomes.append(np.random.binomial(1, success_prob))
    
    # Create a DataFrame
    df = pd.DataFrame({
        'FlightNumber': flight_numbers,
        'Date': dates,
        'LaunchSite': launch_site_codes,
        'MissionOutcome': mission_outcomes
    })
    
    # Add site coordinates
    df['Latitude'] = df['LaunchSite'].apply(lambda x: launch_sites[x]['lat'])
    df['Longitude'] = df['LaunchSite'].apply(lambda x: launch_sites[x]['lon'])
    df['SiteName'] = df['LaunchSite'].apply(lambda x: launch_sites[x]['name'])
    
    # Add a more descriptive outcome
    df['Outcome'] = df['MissionOutcome'].apply(lambda x: 'Success' if x == 1 else 'Failure')
    
    return df

# Generate the launch data
launches_df = generate_launch_data(100)

# Create a Folium map centered on United States
spacex_map = folium.Map(
    location=[39.8283, -98.5795],  # Approximate center of the US
    zoom_start=3,
    tiles='CartoDB positron'  # Light background for better visibility of markers
)

# Create separate feature groups for successes and failures
success_fg = folium.FeatureGroup(name='Successful Launches')
failure_fg = folium.FeatureGroup(name='Failed Launches')

# Add markers with color-coding based on mission outcome
for idx, row in launches_df.iterrows():
    # Choose icon color based on outcome
    if row['Outcome'] == 'Success':
        icon_color = 'green'
        feature_group = success_fg
    else:
        icon_color = 'red'
        feature_group = failure_fg
    
    # Create a customized popup with more information
    popup_html = f"""
    <b>Flight Number:</b> {row['FlightNumber']}<br>
    <b>Date:</b> {row['Date'].strftime('%Y-%m-%d')}<br>
    <b>Launch Site:</b> {row['SiteName']}<br>
    <b>Outcome:</b> <span style='color:{icon_color};'>{row['Outcome']}</span>
    """
    
    # Add marker
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5,
        popup=folium.Popup(popup_html, max_width=300),
        color=icon_color,
        fill=True,
        fill_color=icon_color,
        fill_opacity=0.7,
        weight=2
    ).add_to(feature_group)

# Add the feature groups to the map
success_fg.add_to(spacex_map)
failure_fg.add_to(spacex_map)

# Add Layer control to toggle between success and failure
folium.LayerControl().add_to(spacex_map)

# Add a title
title_html = '''
<h3 align="center" style="font-size:16px"><b>SpaceX Launch Success and Failure Map</b></h3>
'''
spacex_map.get_root().html.add_child(folium.Element(title_html))

# Add a legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; right: 50px; 
            border:2px solid grey; z-index:9999; font-size:14px;
            background-color:white; padding: 10px;
            border-radius: 5px;">
    <p><i style="background:green;border-radius:50%;width:10px;height:10px;display:inline-block;"></i> Successful Launch</p>
    <p><i style="background:red;border-radius:50%;width:10px;height:10px;display:inline-block;"></i> Failed Launch</p>
</div>
'''
spacex_map.get_root().html.add_child(folium.Element(legend_html))

# Save the map to an HTML file
spacex_map.save('spacex_launch_outcomes_map.html')

print("Launch outcomes map created successfully! Open 'spacex_launch_outcomes_map.html' in a web browser to view.")
print("\nLaunch Outcomes Summary:")
print("=" * 50)
success_count = len(launches_df[launches_df['Outcome'] == 'Success'])
failure_count = len(launches_df[launches_df['Outcome'] == 'Failure'])
print(f"Total Launches: {len(launches_df)}")
print(f"Successful Launches: {success_count} ({success_count/len(launches_df)*100:.1f}%)")
print(f"Failed Launches: {failure_count} ({failure_count/len(launches_df)*100:.1f}%)")

# Launch site statistics
print("\nLaunch Site Success Rates:")
print("=" * 50)
site_stats = launches_df.groupby('LaunchSite').agg(
    total_launches=('FlightNumber', 'count'),
    successful=('MissionOutcome', 'sum')
)
site_stats['success_rate'] = site_stats['successful'] / site_stats['total_launches'] * 100

for site_code, row in site_stats.iterrows():
    print(f"Site: {launch_sites[site_code]['name']} ({site_code})")
    print(f"Total Launches: {row['total_launches']}")
    print(f"Success Rate: {row['success_rate']:.1f}%")
    print("-" * 30) 