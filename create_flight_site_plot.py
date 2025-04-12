import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)
launch_sites = ['KSC LC-39A', 'CCAFS SLC-40', 'VAFB SLC-4E']
flight_numbers = np.arange(1, 101)
sites = np.random.choice(launch_sites, size=100)
success_probs = 0.7 + (flight_numbers - 1) * 0.002  # Increasing success rate over time
success = np.random.binomial(1, success_probs)

# Create DataFrame
df = pd.DataFrame({
    'FlightNumber': flight_numbers,
    'LaunchSite': sites,
    'Class': success
})

# Create the plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', 
                hue='Class', style='Class',
                palette={0: 'red', 1: 'blue'},
                markers={0: 'X', 1: 'o'},
                s=100)  # Increased marker size

plt.title('Flight Number vs. Launch Site', fontsize=14, pad=20)
plt.xlabel('Flight Number', fontsize=12)
plt.ylabel('Launch Site', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(title='Landing Success', 
           labels=['Failed', 'Successful'],
           title_fontsize=12,
           fontsize=10)

# Adjust layout and save
plt.tight_layout()
plt.savefig('charts/flight_number_launch_site.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 