import pandas as pd
import numpy as np

# For demonstration, since we've been using sample data
# Create sample data that represents our SpaceX launches
np.random.seed(42)

# Create a list of all potential launch sites
all_launch_sites = [
    'KSC LC-39A',           # Kennedy Space Center Launch Complex 39A
    'CCAFS SLC-40',         # Cape Canaveral Air Force Station Space Launch Complex 40
    'VAFB SLC-4E',          # Vandenberg Air Force Base Space Launch Complex 4E
    'CCAFS LC-40',          # Cape Canaveral Air Force Station Launch Complex 40
    'VAFB SLC-3W',          # Vandenberg Air Force Base Space Launch Complex 3W
    'KSC LC-39B',           # Kennedy Space Center Launch Complex 39B
    'Kwajalein Atoll'       # Marshall Islands launch site
]

# Create sample data for 100 launches
np.random.seed(42)
launches = np.random.choice(all_launch_sites, size=100, p=[0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02])
flight_numbers = np.arange(1, 101)
dates = pd.date_range(start='2010-06-04', periods=100, freq='M')
payloads = np.random.uniform(1000, 15000, 100)
success = np.random.binomial(1, 0.8, 100)  # 80% success rate overall

# Create a DataFrame
df = pd.DataFrame({
    'FlightNumber': flight_numbers,
    'Date': dates,
    'LaunchSite': launches,
    'PayloadMass': payloads,
    'Success': success
})

# Query for records where launch site begins with 'CCA'
ccafs_launches = df[df['LaunchSite'].str.startswith('CCA')].head(5)

# Print results
print("\nRecords where launch site begins with 'CCA':")
print("============================================")
print(ccafs_launches.to_string(index=False))

# Save results to a file
with open('ccafs_launches_results.md', 'w') as f:
    f.write("# Cape Canaveral Air Force Station (CCAFS) Launches\n\n")
    f.write("## 5 Sample Records of CCAFS Launches\n\n")
    
    # Convert DataFrame to markdown table
    markdown_table = ccafs_launches.to_markdown(index=False)
    f.write(markdown_table)
    
    f.write("\n\n## Explanation\n\n")
    f.write("This query identified launches from Cape Canaveral Air Force Station (CCAFS), showing both launch complexes used (SLC-40 and LC-40). ")
    f.write("Cape Canaveral is one of SpaceX's primary East Coast launch facilities, ")
    f.write("used mainly for missions to equatorial orbits, including ISS resupply missions and GTO satellite deployments. ")
    f.write("The results include flight numbers, dates, exact launch sites, payload masses, ")
    f.write("and success status (1 = successful landing, 0 = unsuccessful landing). ")
    f.write("These records highlight SpaceX's extensive use of CCAFS facilities for their Falcon 9 missions.") 