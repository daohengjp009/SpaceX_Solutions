import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)
orbit_types = ['LEO', 'GTO', 'ISS', 'Polar', 'SSO', 'MEO', 'HEO', 'GEO']
flight_numbers = np.arange(1, 101)

# Create orbit distribution that evolves over time
early_orbits = np.random.choice(['LEO', 'GTO', 'ISS'], size=30, p=[0.5, 0.3, 0.2])
mid_orbits = np.random.choice(['LEO', 'GTO', 'ISS', 'Polar', 'SSO'], 
                             size=40, p=[0.3, 0.2, 0.2, 0.15, 0.15])
late_orbits = np.random.choice(orbit_types, 
                              size=30, p=[0.25, 0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.05])

# Combine the orbit data
orbits = np.concatenate([early_orbits, mid_orbits, late_orbits])

# Calculate success based on orbit type and flight number 
# (higher flight numbers have better success rates)
success_base = {
    'LEO': 0.85, 'ISS': 0.80, 'SSO': 0.75, 'Polar': 0.65, 
    'GTO': 0.55, 'MEO': 0.60, 'HEO': 0.50, 'GEO': 0.45
}
success_probs = [min(0.95, success_base[orbit] + flight_num * 0.0005) for orbit, flight_num in zip(orbits, flight_numbers)]
success = np.random.binomial(1, success_probs)

# Create DataFrame
df = pd.DataFrame({
    'FlightNumber': flight_numbers,
    'OrbitType': orbits,
    'Class': success
})

# Create the plot with jitter to avoid overplotting
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
    
    plt.scatter(successes['FlightNumber'], 
                [orbit] * len(successes), 
                marker='o', 
                s=100, 
                color=orbit_colors[orbit],
                edgecolor='blue',
                linewidth=1.5)
    
    plt.scatter(failures['FlightNumber'], 
                [orbit] * len(failures), 
                marker='X', 
                s=100, 
                color=orbit_colors[orbit],
                edgecolor='red',
                linewidth=1.5)

# Add title and labels
plt.title('Flight Number vs. Orbit Type', fontsize=14, pad=20)
plt.xlabel('Flight Number', fontsize=12)
plt.ylabel('Orbit Type', fontsize=12)
plt.xlim(0, 105)  # Add some padding
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
plt.savefig('charts/flight_number_orbit_type.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 