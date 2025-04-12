import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Add year and month for time-based analysis
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    
    return df

# Generate data
launches_df = generate_launch_data(200)

# Calculate success rates for each site
success_by_site = launches_df[launches_df['MissionOutcome'] == 1].groupby('SiteName').size()
total_by_site = launches_df.groupby('SiteName').size()
success_rates = (success_by_site / total_by_site * 100)

# Find the site with the highest success rate (that has more than 5 launches)
sites_with_min_launches = total_by_site[total_by_site >= 5].index
if len(sites_with_min_launches) > 0:
    success_rates_filtered = success_rates[sites_with_min_launches]
    best_site = success_rates_filtered.idxmax()
    best_site_code = next(code for code, info in launch_sites.items() if info['name'] == best_site)
    best_site_success_rate = success_rates_filtered.max()
else:
    # Fallback if no site has at least 5 launches
    best_site = success_rates.idxmax()
    best_site_code = next(code for code, info in launch_sites.items() if info['name'] == best_site)
    best_site_success_rate = success_rates.max()

# Filter data for the best site
best_site_data = launches_df[launches_df['SiteName'] == best_site]

# Create a figure for the dashboard
plt.figure(figsize=(15, 10))
plt.suptitle(f'Launch Performance: {best_site}', fontsize=20, fontweight='bold', y=0.98)

# Define grid for subplots
plt.subplot(2, 2, 1)

# 1. Pie chart of success vs failure for this site
labels = ['Success', 'Failure']
success_count = len(best_site_data[best_site_data['MissionOutcome'] == 1])
failure_count = len(best_site_data[best_site_data['MissionOutcome'] == 0])
sizes = [success_count, failure_count]
colors = ['green', 'red']
explode = (0.1, 0)  # Explode the success slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title(f'Launch Outcomes at {best_site}', fontsize=14)

# 2. Success rate over time (yearly)
plt.subplot(2, 2, 2)
yearly_stats = best_site_data.groupby('Year').agg(
    success=('MissionOutcome', 'sum'),
    total=('MissionOutcome', 'count')
)
yearly_stats['rate'] = yearly_stats['success'] / yearly_stats['total'] * 100

# Create a bar plot
plt.bar(yearly_stats.index, yearly_stats['rate'], color='teal')
plt.axhline(y=best_site_success_rate, color='red', linestyle='-', linewidth=2, label=f'Overall Rate: {best_site_success_rate:.1f}%')
plt.xlabel('Year')
plt.ylabel('Success Rate (%)')
plt.title(f'Success Rate by Year at {best_site}', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, 105)
plt.legend()

# 3. Bar chart comparing launch volume
plt.subplot(2, 2, 3)
site_launch_counts = total_by_site.sort_values(ascending=False)
colors = ['gold' if site == best_site else 'skyblue' for site in site_launch_counts.index]

plt.bar(site_launch_counts.index, site_launch_counts.values, color=colors)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Number of Launches')
plt.title('Launch Volume by Site', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 4. Comparison of success rates across sites
plt.subplot(2, 2, 4)
ordered_rates = success_rates.sort_values(ascending=False)
colors = ['gold' if site == best_site else 'skyblue' for site in ordered_rates.index]

bars = plt.bar(ordered_rates.index, ordered_rates.values, color=colors)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Success Rate (%)')
plt.title('Success Rate by Site', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.ylim(0, 105)

# Add data labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

# Add summary statistics in a text box
textstr = f"Site: {best_site}\n"
textstr += f"Success Rate: {best_site_success_rate:.1f}%\n"
textstr += f"Total Launches: {len(best_site_data)}\n"
textstr += f"Successful Launches: {success_count}\n"
textstr += f"Failed Launches: {failure_count}"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.figtext(0.5, 0.01, textstr, ha='center', fontsize=12, bbox=props)

# Adjust layout and save
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('highest_success_site_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"Dashboard for {best_site} created successfully!")
print("Dashboard saved as 'highest_success_site_dashboard.png'")

# Print detailed statistics about the best site
print("\nDetailed Statistics for Best Site:")
print("=" * 60)
print(f"Site: {best_site} (Code: {best_site_code})")
print(f"Success Rate: {best_site_success_rate:.1f}%")
print(f"Total Launches: {len(best_site_data)}")
print(f"Successful Launches: {success_count}")
print(f"Failed Launches: {failure_count}")

# List all launches at this site
print("\nLaunch History:")
print("-" * 60)
print(f"{'Flight #':<10} {'Date':<15} {'Outcome':<10}")
print("-" * 60)

for _, launch in best_site_data.sort_values('Date').iterrows():
    print(f"{launch['FlightNumber']:<10} {launch['Date'].strftime('%Y-%m-%d'):<15} {launch['Outcome']:<10}")

# Calculate average launches per year for this site
years_active = best_site_data['Year'].nunique()
avg_launches_per_year = len(best_site_data) / years_active if years_active > 0 else 0

print("\nAdditional Insights:")
print("-" * 60)
print(f"Years Active: {years_active}")
print(f"Average Launches Per Year: {avg_launches_per_year:.1f}") 