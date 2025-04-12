import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec

# Set styling for plots
plt.style.use('ggplot')
sns.set_palette('colorblind')

# Reuse launch sites from our previous scripts
launch_sites = {
    'KSC LC-39A': {'name': 'Kennedy Space Center LC-39A', 'lat': 28.6080, 'lon': -80.6043},
    'CCAFS SLC-40': {'name': 'Cape Canaveral SLC-40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-4E': {'name': 'Vandenberg SLC-4E', 'lat': 34.6332, 'lon': -120.6130},
    'CCAFS LC-40': {'name': 'Cape Canaveral LC-40', 'lat': 28.5618, 'lon': -80.5770},
    'VAFB SLC-3W': {'name': 'Vandenberg SLC-3W', 'lat': 34.6364, 'lon': -120.5895},
    'KSC LC-39B': {'name': 'Kennedy Space Center LC-39B', 'lat': 28.6270, 'lon': -80.6208},
    'Kwajalein Atoll': {'name': 'Kwajalein Atoll', 'lat': 9.0477, 'lon': 167.7431}
}

# Generate sample launch data
def generate_launch_data(num_launches=200):
    np.random.seed(42)  # For reproducibility
    
    flight_numbers = np.arange(1, num_launches + 1)
    dates = pd.date_range(start='2010-06-04', end='2022-12-31', periods=num_launches)
    
    # Randomly assign launch sites with weighted probabilities
    site_codes = list(launch_sites.keys())
    site_probabilities = [0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02]
    launch_site_codes = np.random.choice(site_codes, size=num_launches, p=site_probabilities)
    
    # Generate mission outcomes with improving success rates over time
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
    
    # Add site names for better readability
    df['SiteName'] = df['LaunchSite'].apply(lambda x: launch_sites[x]['name'])
    
    # Add descriptive outcome
    df['Outcome'] = df['MissionOutcome'].apply(lambda x: 'Success' if x == 1 else 'Failure')
    
    return df

# Generate data
launches_df = generate_launch_data(200)

# Create a figure for the dashboard
plt.figure(figsize=(15, 10))
plt.suptitle('SpaceX Launch Success Dashboard', fontsize=20, fontweight='bold', y=0.98)

# Set up the grid for multiple plots
gs = GridSpec(2, 2, height_ratios=[1, 1])

# 1. Pie chart of successful launches by site
ax1 = plt.subplot(gs[0, 0])
success_by_site = launches_df[launches_df['MissionOutcome'] == 1].groupby('SiteName').size()
total_by_site = launches_df.groupby('SiteName').size()

# Calculate percentages for labels
success_percentages = {}
for site in success_by_site.index:
    success_percentages[site] = f"{site}\n({success_by_site[site]}/{total_by_site[site]})"

ax1.pie(success_by_site, 
        labels=[success_percentages[site] for site in success_by_site.index], 
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        explode=[0.05] * len(success_by_site),  # Slight explode for all slices
        textprops={'fontsize': 9})
ax1.set_title('Successful Launches by Site', fontsize=14)

# 2. Bar chart of success rates by site
ax2 = plt.subplot(gs[0, 1])
success_rates = (success_by_site / total_by_site * 100).sort_values(ascending=False)
bars = ax2.bar(success_rates.index, success_rates.values, color=sns.color_palette('colorblind')[:len(success_rates)])

# Add data labels on bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

ax2.set_title('Success Rate by Launch Site', fontsize=14)
ax2.set_ylabel('Success Rate (%)')
ax2.set_ylim(0, 105)  # Give a little space above 100%
plt.xticks(rotation=45, ha='right')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# 3. Time series of launches showing success trend
ax3 = plt.subplot(gs[1, :])
launches_df['Year'] = launches_df['Date'].dt.year
yearly_data = launches_df.groupby(['Year', 'Outcome']).size().unstack().fillna(0)

if 'Success' in yearly_data.columns and 'Failure' in yearly_data.columns:
    yearly_data['Total'] = yearly_data['Success'] + yearly_data['Failure']
    yearly_data['SuccessRate'] = yearly_data['Success'] / yearly_data['Total'] * 100
    
    # Plot the success rate as a line
    ax3_rate = ax3.twinx()
    ax3_rate.plot(yearly_data.index, yearly_data['SuccessRate'], 'r-', marker='o', linewidth=2, label='Success Rate')
    ax3_rate.set_ylabel('Success Rate (%)', color='r')
    ax3_rate.set_ylim(0, 105)  # Give a little space above 100%
    ax3_rate.tick_params(axis='y', labelcolor='r')
    
    # Plot the launch counts as bars
    ax3.bar(yearly_data.index, yearly_data['Success'], label='Success', alpha=0.7, color='green')
    ax3.bar(yearly_data.index, yearly_data['Failure'], bottom=yearly_data['Success'], 
            label='Failure', alpha=0.7, color='red')
    
    ax3.set_title('Launches and Success Rate Over Time', fontsize=14)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Number of Launches')
    ax3.legend(loc='upper left')
    ax3_rate.legend(loc='lower right')
    ax3.grid(axis='y', linestyle='--', alpha=0.7)

# Add an overall success rate text box
total_success = len(launches_df[launches_df['MissionOutcome'] == 1])
total_launches = len(launches_df)
success_rate = total_success / total_launches * 100

textstr = f'Overall Success Rate: {success_rate:.1f}%\n'
textstr += f'Total Launches: {total_launches}\n'
textstr += f'Successful Launches: {total_success}'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.figtext(0.5, 0.01, textstr, ha='center', fontsize=12, bbox=props)

# Adjust layout and save
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('spacex_launch_success_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("SpaceX Launch Success Dashboard created successfully!")
print("Dashboard saved as 'spacex_launch_success_dashboard.png'")

# Print some summary statistics
print("\nLaunch Success Summary by Site:")
print("=" * 50)
print(f"{'Launch Site':<25} {'Success':<10} {'Total':<10} {'Rate (%)':<10}")
print("-" * 50)

for site in total_by_site.index:
    if site in success_by_site:
        success_count = success_by_site[site]
    else:
        success_count = 0
    
    total_count = total_by_site[site]
    rate = (success_count / total_count) * 100
    
    print(f"{site:<25} {success_count:<10d} {total_count:<10d} {rate:<10.1f}")

print("\nOverall Success Rate: {:.1f}%".format(success_rate)) 