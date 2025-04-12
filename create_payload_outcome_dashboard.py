import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import RangeSlider
import matplotlib.gridspec as gridspec

# Set styling for plots
plt.style.use('ggplot')
sns.set_palette('colorblind')
plt.rcParams['font.size'] = 10

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

# Define booster versions with appropriate timeline
# F9 v1.0: Flights 1-5 (2010-2013)
# F9 v1.1: Flights 6-20 (2013-2015)
# F9 FT (Full Thrust): Flights 21-60 (2015-2018)
# F9 Block 5: Flights 61-100 (2018-2022)
def get_booster_version(flight_num):
    if flight_num <= 5:
        return 'F9 v1.0'
    elif flight_num <= 20:
        return 'F9 v1.1'
    elif flight_num <= 60:
        return 'F9 FT'
    else:
        return 'F9 Block 5'

# Generate sample launch data with payload information
def generate_launch_data(num_launches=200):
    np.random.seed(42)  # For reproducibility
    
    flight_numbers = np.arange(1, num_launches + 1)
    dates = pd.date_range(start='2010-06-04', end='2022-12-31', periods=num_launches)
    
    # Assign booster versions based on flight numbers
    booster_versions = [get_booster_version(flight_num) for flight_num in flight_numbers]
    
    # Randomly assign launch sites with weighted probabilities
    site_codes = list(launch_sites.keys())
    site_probabilities = [0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02]
    launch_site_codes = np.random.choice(site_codes, size=num_launches, p=site_probabilities)
    
    # Generate payloads based on booster version - newer versions can carry heavier payloads
    payloads = []
    for version in booster_versions:
        if version == 'F9 v1.0':
            payloads.append(np.random.uniform(1000, 8000))
        elif version == 'F9 v1.1':
            payloads.append(np.random.uniform(3000, 12000))
        elif version == 'F9 FT':
            payloads.append(np.random.uniform(5000, 15000))
        else:  # F9 Block 5
            payloads.append(np.random.uniform(6000, 16000))
    
    # Generate mission outcomes with success probability based on booster version and payload
    mission_outcomes = []
    for i, (version, payload) in enumerate(zip(booster_versions, payloads)):
        # Base success probability by version
        if version == 'F9 v1.0':
            base_prob = 0.75
        elif version == 'F9 v1.1':
            base_prob = 0.85
        elif version == 'F9 FT':
            base_prob = 0.92
        else:  # F9 Block 5
            base_prob = 0.98
        
        # Modify probability based on payload (heavier payloads slightly more risky)
        # Normalize payload to 0-1 range within its version's typical range
        if version == 'F9 v1.0':
            payload_factor = (payload - 1000) / (8000 - 1000)
        elif version == 'F9 v1.1':
            payload_factor = (payload - 3000) / (12000 - 3000)
        elif version == 'F9 FT':
            payload_factor = (payload - 5000) / (15000 - 5000)
        else:  # F9 Block 5
            payload_factor = (payload - 6000) / (16000 - 6000)
        
        # Higher payloads slightly decrease success probability (but newer versions less affected)
        if version == 'F9 v1.0':
            success_prob = base_prob - (payload_factor * 0.15)
        elif version == 'F9 v1.1':
            success_prob = base_prob - (payload_factor * 0.10)
        elif version == 'F9 FT':
            success_prob = base_prob - (payload_factor * 0.05)
        else:  # F9 Block 5
            success_prob = base_prob - (payload_factor * 0.02)
        
        # Ensure probability is valid
        success_prob = max(0.5, min(0.99, success_prob))
        
        # Generate outcome
        mission_outcomes.append(np.random.binomial(1, success_prob))
    
    # Create a DataFrame
    df = pd.DataFrame({
        'FlightNumber': flight_numbers,
        'Date': dates,
        'BoosterVersion': booster_versions,
        'LaunchSite': launch_site_codes,
        'PayloadMass': payloads,
        'MissionOutcome': mission_outcomes
    })
    
    # Add site names for better readability
    df['SiteName'] = df['LaunchSite'].apply(lambda x: launch_sites[x]['name'])
    
    # Add descriptive outcome
    df['Outcome'] = df['MissionOutcome'].apply(lambda x: 'Success' if x == 1 else 'Failure')
    
    # Add year for time-based analysis
    df['Year'] = df['Date'].dt.year
    
    return df

# Generate data
launches_df = generate_launch_data(200)

# Create a three-panel dashboard with different payload ranges
# We'll create three static images at different payload ranges to simulate a slider

# Define payload ranges to display
payload_ranges = [
    (0, 16000, "All Payloads"),
    (0, 8000, "Light Payloads (0-8,000 kg)"),
    (8000, 16000, "Heavy Payloads (8,000-16,000 kg)"),
]

# Function to create and save a scatter plot for a specific payload range
def create_payload_outcome_plot(min_payload, max_payload, title, filename):
    # Create a large figure
    fig = plt.figure(figsize=(15, 10))
    fig.suptitle(f"SpaceX Payload vs. Launch Outcome Analysis: {title}", fontsize=20, fontweight='bold', y=0.98)
    
    # Create a grid for the plots
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1])
    
    # Main scatter plot
    ax_scatter = plt.subplot(gs[0, :])
    
    # Filter data for the specified payload range
    filtered_df = launches_df[(launches_df['PayloadMass'] >= min_payload) & 
                              (launches_df['PayloadMass'] <= max_payload)]
    
    # Create a scatter plot with different colors for success and failure
    success_df = filtered_df[filtered_df['MissionOutcome'] == 1]
    failure_df = filtered_df[filtered_df['MissionOutcome'] == 0]
    
    # Plot failures
    ax_scatter.scatter(failure_df['PayloadMass'], failure_df['BoosterVersion'], 
                      marker='X', s=100, c='red', alpha=0.7, label='Failure')
    
    # Plot successes
    ax_scatter.scatter(success_df['PayloadMass'], success_df['BoosterVersion'], 
                      marker='o', s=80, c='green', alpha=0.5, label='Success')
    
    # Set labels and title
    ax_scatter.set_xlabel('Payload Mass (kg)', fontsize=12)
    ax_scatter.set_ylabel('Booster Version', fontsize=12)
    ax_scatter.set_title(f'Payload Mass vs. Booster Version', fontsize=16)
    ax_scatter.grid(True, linestyle='--', alpha=0.7)
    ax_scatter.legend(fontsize=12)
    
    # Add a vertical line at the middle of the payload range for reference
    mid_payload = (min_payload + max_payload) / 2
    if min_payload < 8000 < max_payload:
        ax_scatter.axvline(x=8000, color='black', linestyle='--', alpha=0.3, 
                          label='Light/Heavy Payload Boundary')
    
    # Success rate by payload bins
    ax_payload = plt.subplot(gs[1, 0])
    
    # Create payload bins
    bin_width = (max_payload - min_payload) / 5  # 5 bins across the range
    bins = np.arange(min_payload, max_payload + bin_width, bin_width)
    filtered_df['PayloadBin'] = pd.cut(filtered_df['PayloadMass'], bins=bins)
    
    # Calculate success rate by bin
    payload_success = filtered_df.groupby('PayloadBin')['MissionOutcome'].agg(['mean', 'count'])
    payload_success['mean'] = payload_success['mean'] * 100  # Convert to percentage
    
    # Plot the success rate by payload bin
    bars = ax_payload.bar(range(len(payload_success)), payload_success['mean'], 
                         alpha=0.7, color='teal')
    
    # Add count labels
    for i, (idx, row) in enumerate(payload_success.iterrows()):
        ax_payload.text(i, row['mean'] + 2, f"n={row['count']}", 
                       ha='center', va='bottom', fontsize=9)
    
    # Set labels and formatting
    bin_labels = [f"{b.left:.0f}-{b.right:.0f}" for b in payload_success.index]
    ax_payload.set_xticks(range(len(payload_success)))
    ax_payload.set_xticklabels(bin_labels, rotation=45, ha='right')
    ax_payload.set_xlabel('Payload Mass Range (kg)', fontsize=12)
    ax_payload.set_ylabel('Success Rate (%)', fontsize=12)
    ax_payload.set_title('Success Rate by Payload Mass', fontsize=14)
    ax_payload.set_ylim(0, 105)
    ax_payload.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Success rate by booster version
    ax_booster = plt.subplot(gs[1, 1])
    
    # Calculate success rate by booster version
    booster_success = filtered_df.groupby('BoosterVersion')['MissionOutcome'].agg(['mean', 'count'])
    booster_success['mean'] = booster_success['mean'] * 100  # Convert to percentage
    
    # Sort by version chronologically
    version_order = ['F9 v1.0', 'F9 v1.1', 'F9 FT', 'F9 Block 5']
    booster_success = booster_success.reindex(version_order)
    
    # Plot the success rate by booster version
    bars = ax_booster.bar(range(len(booster_success)), booster_success['mean'], 
                         alpha=0.7, color='purple')
    
    # Add count labels
    for i, (idx, row) in enumerate(booster_success.iterrows()):
        ax_booster.text(i, row['mean'] + 2, f"n={row['count']}", 
                       ha='center', va='bottom', fontsize=9)
    
    # Set labels and formatting
    ax_booster.set_xticks(range(len(booster_success)))
    ax_booster.set_xticklabels(booster_success.index, rotation=45, ha='right')
    ax_booster.set_xlabel('Booster Version', fontsize=12)
    ax_booster.set_ylabel('Success Rate (%)', fontsize=12)
    ax_booster.set_title('Success Rate by Booster Version', fontsize=14)
    ax_booster.set_ylim(0, 105)
    ax_booster.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add summary statistics in a text box
    filtered_success = len(filtered_df[filtered_df['MissionOutcome'] == 1])
    filtered_total = len(filtered_df)
    filtered_success_rate = (filtered_success / filtered_total) * 100 if filtered_total > 0 else 0
    
    textstr = f"Payload Range: {min_payload:.0f} - {max_payload:.0f} kg\n"
    textstr += f"Launch Success Rate: {filtered_success_rate:.1f}%\n"
    textstr += f"Successful Launches: {filtered_success} / {filtered_total}\n"
    
    # Find payload range with highest success rate
    best_bin_idx = payload_success['mean'].idxmax() if not payload_success.empty else None
    if best_bin_idx is not None:
        best_bin = best_bin_idx  # Use the index directly, which is already a category with left and right
        textstr += f"Best Payload Range: {best_bin.left:.0f} - {best_bin.right:.0f} kg ({payload_success.loc[best_bin, 'mean']:.1f}%)\n"
    
    # Find best booster version
    best_version_idx = booster_success['mean'].idxmax() if not booster_success.empty else None
    if best_version_idx is not None:
        best_version = best_version_idx  # Use the index directly
        textstr += f"Best Booster Version: {best_version} ({booster_success.loc[best_version, 'mean']:.1f}%)"
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    fig.text(0.5, 0.01, textstr, ha='center', fontsize=12, bbox=props)
    
    # Adjust layout and save
    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    
    return filtered_df

# Create plots for each payload range
for min_payload, max_payload, title in payload_ranges:
    filename = f"payload_outcome_dashboard_{min_payload}_{max_payload}.png"
    filtered_data = create_payload_outcome_plot(min_payload, max_payload, title, filename)
    
    # Print summary for this range
    success_count = len(filtered_data[filtered_data['MissionOutcome'] == 1])
    total_count = len(filtered_data)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"\nPayload Range: {min_payload} - {max_payload} kg ({title})")
    print("=" * 60)
    print(f"Launches: {total_count}")
    print(f"Success Rate: {success_rate:.1f}%")
    
    # Success rate by booster version
    print("\nSuccess Rate by Booster Version:")
    booster_stats = filtered_data.groupby('BoosterVersion')['MissionOutcome'].agg(['mean', 'count'])
    booster_stats['mean'] = booster_stats['mean'] * 100  # Convert to percentage
    for version, stats in booster_stats.iterrows():
        print(f"  {version}: {stats['mean']:.1f}% ({int(stats['count'])} launches)")
    
    # Binned payload success rates
    bin_width = (max_payload - min_payload) / 5  # 5 bins across the range
    bins = np.arange(min_payload, max_payload + bin_width, bin_width)
    filtered_data['PayloadBin'] = pd.cut(filtered_data['PayloadMass'], bins=bins)
    
    print("\nSuccess Rate by Payload Mass Range:")
    payload_stats = filtered_data.groupby('PayloadBin')['MissionOutcome'].agg(['mean', 'count'])
    payload_stats['mean'] = payload_stats['mean'] * 100  # Convert to percentage
    for bin_range, stats in payload_stats.iterrows():
        print(f"  {bin_range.left:.0f}-{bin_range.right:.0f} kg: {stats['mean']:.1f}% ({int(stats['count'])} launches)")

print("\nDashboards created successfully!")
print("Main dashboard: payload_outcome_dashboard_0_16000.png")
print("Light payloads: payload_outcome_dashboard_0_8000.png")
print("Heavy payloads: payload_outcome_dashboard_8000_16000.png") 