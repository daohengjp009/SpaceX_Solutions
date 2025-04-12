import pandas as pd
import numpy as np

# For demonstration, since we've been using sample data
# Create sample data that represents our SpaceX launches
np.random.seed(42)

# Create a list of all potential launch sites
all_launch_sites = [
    'KSC LC-39A',          # Kennedy Space Center Launch Complex 39A
    'CCAFS SLC-40',        # Cape Canaveral Air Force Station Space Launch Complex 40
    'VAFB SLC-4E',         # Vandenberg Air Force Base Space Launch Complex 4E
    'CCAFS LC-40',         # Cape Canaveral Air Force Station Launch Complex 40
    'VAFB SLC-3W',         # Vandenberg Air Force Base Space Launch Complex 3W
    'KSC LC-39B',          # Kennedy Space Center Launch Complex 39B
    'Kwajalein Atoll'      # Marshall Islands launch site
]

# Define potential customers
customers = ['NASA', 'SpaceX', 'Commercial', 'DoD', 'ESA', 'JAXA', 'Other']

# Define rocket versions with appropriate timeline
# F9 v1.0: Flights 1-5 (2010-2013)
# F9 v1.1: Flights 6-20 (2013-2015)
# F9 FT (Full Thrust): Flights 21-60 (2015-2018)
# F9 Block 5: Flights 61-100 (2018-2022)
booster_versions = []

for flight_num in range(1, 101):
    if flight_num <= 5:
        booster_versions.append('F9 v1.0')
    elif flight_num <= 20:
        booster_versions.append('F9 v1.1')
    elif flight_num <= 60:
        booster_versions.append('F9 FT')
    else:
        booster_versions.append('F9 Block 5')

# Create sample data for 100 launches
np.random.seed(42)
launches = np.random.choice(all_launch_sites, size=100, p=[0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02])
flight_numbers = np.arange(1, 101)
dates = pd.date_range(start='2010-06-04', periods=100, freq='M')

# Adjust payload capacity based on booster version (newer versions can carry more)
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

success = np.random.binomial(1, 0.8, 100)  # 80% success rate overall

# Assign customers
customer_probs = []
for site in launches:
    if 'KSC' in site:
        # NASA has higher probability at Kennedy Space Center
        customer_probs.append([0.6, 0.1, 0.1, 0.05, 0.1, 0.03, 0.02])
    elif 'CCAFS' in site:
        # NASA has medium probability at Cape Canaveral
        customer_probs.append([0.4, 0.2, 0.2, 0.1, 0.05, 0.03, 0.02])
    else:
        # NASA has lower probability at other sites
        customer_probs.append([0.2, 0.3, 0.3, 0.1, 0.05, 0.03, 0.02])

launch_customers = [np.random.choice(customers, p=prob) for prob in customer_probs]

# Create a DataFrame
df = pd.DataFrame({
    'FlightNumber': flight_numbers,
    'Date': dates,
    'LaunchSite': launches,
    'PayloadMass': payloads,
    'Success': success,
    'Customer': launch_customers,
    'BoosterVersion': booster_versions
})

# Calculate statistics for F9 v1.1
f9v11_launches = df[df['BoosterVersion'] == 'F9 v1.1']
f9v11_count = len(f9v11_launches)
f9v11_total_payload = f9v11_launches['PayloadMass'].sum()
f9v11_avg_payload = f9v11_launches['PayloadMass'].mean()
f9v11_min_payload = f9v11_launches['PayloadMass'].min()
f9v11_max_payload = f9v11_launches['PayloadMass'].max()
f9v11_success_rate = f9v11_launches['Success'].mean() * 100

# Print results
print("\nF9 v1.1 Booster Payload Analysis:")
print("================================")
print(f"Total F9 v1.1 Launches: {f9v11_count}")
print(f"Total Payload Mass: {f9v11_total_payload:.2f} kg")
print(f"Average Payload Mass: {f9v11_avg_payload:.2f} kg per mission")
print(f"Minimum Payload Mass: {f9v11_min_payload:.2f} kg")
print(f"Maximum Payload Mass: {f9v11_max_payload:.2f} kg")
print(f"Success Rate: {f9v11_success_rate:.1f}%")

# Get all F9 v1.1 launches
print("\nF9 v1.1 Launch Details:")
print("======================")
print(f9v11_launches[['FlightNumber', 'Date', 'LaunchSite', 'PayloadMass', 'Customer', 'Success']].to_string(index=False))

# Comparison with other booster versions
print("\nAverage Payload by Booster Version:")
print("==================================")
for version in sorted(df['BoosterVersion'].unique()):
    avg = df[df['BoosterVersion'] == version]['PayloadMass'].mean()
    count = len(df[df['BoosterVersion'] == version])
    print(f"{version}: {avg:.2f} kg (from {count} launches)")

# Save results to a file
with open('f9v11_payload_results.md', 'w') as f:
    f.write("# F9 v1.1 Booster Payload Analysis\n\n")
    
    f.write("## Overall F9 v1.1 Statistics\n\n")
    f.write(f"- **Total F9 v1.1 Launches**: {f9v11_count}\n")
    f.write(f"- **Total Payload Mass**: {f9v11_total_payload:.2f} kg\n")
    f.write(f"- **Average Payload Mass**: {f9v11_avg_payload:.2f} kg per mission\n")
    f.write(f"- **Minimum Payload Mass**: {f9v11_min_payload:.2f} kg\n")
    f.write(f"- **Maximum Payload Mass**: {f9v11_max_payload:.2f} kg\n")
    f.write(f"- **Success Rate**: {f9v11_success_rate:.1f}%\n\n")
    
    f.write("## F9 v1.1 Launches\n\n")
    # Convert DataFrame to markdown table
    markdown_table = f9v11_launches[['FlightNumber', 'Date', 'LaunchSite', 'PayloadMass', 'Customer', 'Success']].to_markdown(index=False)
    f.write(markdown_table)
    
    f.write("\n\n## Comparison with Other Booster Versions\n\n")
    f.write("| Booster Version | Average Payload (kg) | Number of Launches |\n")
    f.write("|-----------------|----------------------|--------------------|\n")
    for version in sorted(df['BoosterVersion'].unique()):
        avg = df[df['BoosterVersion'] == version]['PayloadMass'].mean()
        count = len(df[df['BoosterVersion'] == version])
        f.write(f"| {version} | {avg:.2f} | {count} |\n")
    
    f.write("\n\n## Explanation\n\n")
    f.write("This analysis calculated the average payload mass carried by the Falcon 9 v1.1 booster version. ")
    f.write("The F9 v1.1 was SpaceX's first major upgrade to the Falcon 9, used between 2013-2015 for flights 6-20. ")
    f.write("Key improvements in the F9 v1.1 included stretched fuel tanks, upgraded Merlin 1D engines, and a new ")
    f.write("engine arrangement (octaweb), which increased payload capacity significantly compared to the original F9 v1.0. ")
    f.write("This version was an important step in SpaceX's development of reusable rocket technology, ")
    f.write("though it did not yet have the same payload capacity as later versions like the Falcon 9 Full Thrust and Block 5.") 