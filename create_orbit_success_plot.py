import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)
orbit_types = ['LEO', 'GTO', 'ISS', 'Polar', 'SSO', 'MEO', 'HEO', 'GEO']
base_success = [0.95, 0.65, 0.90, 0.75, 0.85, 0.70, 0.60, 0.55]
success_rates = [rate + np.random.normal(0, 0.02) for rate in base_success]
success_rates = np.clip(success_rates, 0, 1)  # Ensure rates are between 0 and 1

# Create DataFrame
df = pd.DataFrame({
    'OrbitType': orbit_types,
    'SuccessRate': success_rates
})

# Sort by success rate
df = df.sort_values('SuccessRate', ascending=False)

# Create the plot
plt.figure(figsize=(12, 8))
bars = plt.bar(df['OrbitType'], df['SuccessRate'], 
               color='#005288',  # SpaceX blue
               alpha=0.8)

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.01,
             f'{height:.0%}',
             ha='center', va='bottom', fontsize=12)

plt.title('Landing Success Rate by Orbit Type', fontsize=14, pad=20)
plt.xlabel('Orbit Type', fontsize=12)
plt.ylabel('Success Rate', fontsize=12)
plt.ylim(0, 1.1)  # Add some space for the labels
plt.grid(True, alpha=0.3, axis='y')

# Customize the plot
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot
plt.savefig('charts/orbit_type_success.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 