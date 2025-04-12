import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)
launch_sites = ['KSC LC-39A', 'CCAFS SLC-40', 'VAFB SLC-4E']
payload_masses = np.random.uniform(1000, 15000, 100)  # kg
sites = np.random.choice(launch_sites, size=100)
success_probs = 0.9 - (payload_masses - 1000) * 0.00003  # Higher payload = lower success
success = np.random.binomial(1, success_probs)

# Create DataFrame
df = pd.DataFrame({
    'PayloadMass': payload_masses,
    'LaunchSite': sites,
    'Class': success
})

# Create the plot
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x='PayloadMass', y='LaunchSite', 
                hue='Class', style='Class',
                palette={0: 'red', 1: 'blue'},
                markers={0: 'X', 1: 'o'},
                s=100)  # Increased marker size

plt.title('Payload Mass vs. Launch Site', fontsize=14, pad=20)
plt.xlabel('Payload Mass (kg)', fontsize=12)
plt.ylabel('Launch Site', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(title='Landing Success', 
           labels=['Failed', 'Successful'],
           title_fontsize=12,
           fontsize=10)

# Adjust layout and save
plt.tight_layout()
plt.savefig('charts/payload_mass_launch_site.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 