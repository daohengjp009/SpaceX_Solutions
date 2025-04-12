import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)
orbit_types = ['LEO', 'GTO', 'ISS', 'Polar', 'SSO', 'MEO', 'HEO', 'GEO']

# Define typical payload ranges for different orbit types
payload_ranges = {
    'LEO': (1000, 10000),    # Low Earth Orbit - wide range
    'GTO': (4000, 12000),    # Geostationary Transfer Orbit - heavier
    'ISS': (2000, 8000),     # International Space Station - medium
    'Polar': (1000, 5000),   # Polar Orbit - lighter
    'SSO': (1000, 4000),     # Sun-Synchronous Orbit - lighter
    'MEO': (3000, 9000),     # Medium Earth Orbit - medium
    'HEO': (2000, 7000),     # Highly Elliptical Orbit - medium
    'GEO': (5000, 14000)     # Geostationary Orbit - heaviest
}

# Generate data points - 15 missions for each orbit type
num_per_orbit = 15
orbits = []
payloads = []
success_list = []

for orbit in orbit_types:
    orbits.extend([orbit] * num_per_orbit)
    
    # Generate random payloads within the typical range for this orbit
    min_payload, max_payload = payload_ranges[orbit]
    orbit_payloads = np.random.uniform(min_payload, max_payload, num_per_orbit)
    payloads.extend(orbit_payloads)
    
    # Calculate success probability based on orbit type and payload mass
    # Heavier payloads have lower success rates
    base_success = {
        'LEO': 0.85, 'ISS': 0.80, 'SSO': 0.75, 'Polar': 0.65, 
        'GTO': 0.55, 'MEO': 0.60, 'HEO': 0.50, 'GEO': 0.45
    }
    
    for payload in orbit_payloads:
        # Adjust success probability based on payload (heavier = lower success)
        payload_factor = (max_payload - payload) / (max_payload - min_payload) * 0.3
        success_prob = min(0.95, max(0.2, base_success[orbit] + payload_factor))
        success_list.append(np.random.binomial(1, success_prob))

# Create DataFrame
df = pd.DataFrame({
    'OrbitType': orbits,
    'PayloadMass': payloads,
    'Class': success_list
})

# Create the plot
plt.figure(figsize=(12, 8))
ax = plt.subplot(111)

# Use a custom palette that distinguishes orbit types
palette = sns.color_palette("bright", len(orbit_types))
orbit_colors = dict(zip(orbit_types, palette))

# Plot each orbit type
for orbit in orbit_types:
    orbit_data = df[df['OrbitType'] == orbit]
    
    # Plot successes and failures with different markers
    successes = orbit_data[orbit_data['Class'] == 1]
    failures = orbit_data[orbit_data['Class'] == 0]
    
    plt.scatter(successes['PayloadMass'], 
                [orbit] * len(successes), 
                marker='o', 
                s=100, 
                color=orbit_colors[orbit],
                edgecolor='blue',
                linewidth=1.5)
    
    plt.scatter(failures['PayloadMass'], 
                [orbit] * len(failures), 
                marker='X', 
                s=100, 
                color=orbit_colors[orbit],
                edgecolor='red',
                linewidth=1.5)

# Add title and labels
plt.title('Payload Mass vs. Orbit Type', fontsize=14, pad=20)
plt.xlabel('Payload Mass (kg)', fontsize=12)
plt.ylabel('Orbit Type', fontsize=12)
plt.xlim(0, 15000)  # Add some padding
plt.grid(True, alpha=0.3)

# Add legends for success/failure markers
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', markersize=10, label='Successful Landing', markeredgecolor='blue'),
    Line2D([0], [0], marker='X', color='w', markerfacecolor='gray', markersize=10, label='Failed Landing', markeredgecolor='red')
]
plt.legend(handles=legend_elements, loc='upper left')

# Add a separate legend for orbit types
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=orbit) 
          for orbit, color in orbit_colors.items()]
leg = ax.legend(handles=handles, loc='upper right', title='Orbit Types')

# Adjust layout and save
plt.tight_layout()
plt.savefig('charts/payload_mass_orbit_type.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 