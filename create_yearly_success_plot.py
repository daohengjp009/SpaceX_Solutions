import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create sample data
np.random.seed(42)

# Years of SpaceX operations
years = np.arange(2010, 2023)

# Create a realistic trend of increasing success rates over time
# Starting low and improving with experience
base_success_rates = np.array([0.40, 0.45, 0.50, 0.55, 0.65, 0.70, 0.75, 
                              0.80, 0.85, 0.85, 0.88, 0.90, 0.92])

# Add some random variation but ensure trend is preserved
variation = np.random.normal(0, 0.03, len(years))
success_rates = np.clip(base_success_rates + variation, 0, 1)

# Number of launches each year (increasing over time)
num_launches = [1, 2, 2, 3, 6, 7, 8, 18, 21, 13, 26, 31, 61]

# Create DataFrame
df = pd.DataFrame({
    'Year': years,
    'SuccessRate': success_rates,
    'Launches': num_launches
})

# Create the plot
plt.figure(figsize=(12, 8))

# Main line plot with success rate
ax1 = plt.subplot(111)
line = ax1.plot(df['Year'], df['SuccessRate'], marker='o', linewidth=3, markersize=10, 
           color='#005288', label='Success Rate')  # SpaceX blue

# Add value labels on the points
for i, row in df.iterrows():
    ax1.text(row['Year'], row['SuccessRate'] + 0.02, f"{row['SuccessRate']:.0%}", 
            ha='center', va='bottom', fontsize=10)

# Set up primary y-axis
ax1.set_ylim(0.3, 1.0)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Landing Success Rate', fontsize=12)
ax1.grid(True, alpha=0.3)

# Add secondary y-axis showing number of launches
ax2 = ax1.twinx()
bars = ax2.bar(df['Year'], df['Launches'], alpha=0.2, color='#A7A9AC', label='Number of Launches')  # SpaceX grey

# Set up secondary y-axis
ax2.set_ylabel('Number of Launches', fontsize=12)
ax2.set_ylim(0, max(df['Launches']) * 1.2)

# Add title and labels
plt.title('SpaceX Yearly Landing Success Rate (2010-2022)', fontsize=14, pad=20)

# Add dual legends
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

# Customize x-axis ticks to show all years
plt.xticks(years, rotation=45)

# Add annotations for key milestones
plt.annotate('First successful\nland landing', xy=(2015, 0.72), xytext=(2015, 0.60),
            arrowprops=dict(facecolor='black', width=1, headwidth=6, shrink=0.05), fontsize=9)

plt.annotate('First successful\ndrone ship landing', xy=(2016, 0.75), xytext=(2016, 0.62),
            arrowprops=dict(facecolor='black', width=1, headwidth=6, shrink=0.05), fontsize=9)

plt.annotate('Falcon Heavy\ndebut', xy=(2018, 0.84), xytext=(2018, 0.72),
            arrowprops=dict(facecolor='black', width=1, headwidth=6, shrink=0.05), fontsize=9)

# Adjust layout and save
plt.tight_layout()
plt.savefig('charts/yearly_success_rate.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close() 