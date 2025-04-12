import pandas as pd
import numpy as np
from datetime import datetime

# For demonstration, using the same sample data creation approach as in find_max_payload_boosters.py
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

# Define booster versions with appropriate timeline
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

# Give boosters unique identifiers
booster_ids = []
current_booster = 1001
# First 20 flights are expendable (no reuse), so new booster each time
for i in range(20):
    booster_ids.append(f"B{current_booster}")
    current_booster += 1

# For remaining flights, mix of new and reused boosters
used_boosters = []
for i in range(20, 100):
    # 70% chance of reusing a booster after flight 20
    if i > 25 and np.random.random() < 0.7 and used_boosters:
        # Choose a previously used booster
        booster_ids.append(np.random.choice(used_boosters))
    else:
        # Use a new booster
        booster_ids.append(f"B{current_booster}")
        used_boosters.append(f"B{current_booster}")
        current_booster += 1

# Create sample data for 100 launches spanning 2010-2022
flight_numbers = np.arange(1, 101)
dates = pd.date_range(start='2010-06-04', end='2022-12-31', periods=100)
launches = np.random.choice(all_launch_sites, size=100, p=[0.35, 0.30, 0.20, 0.05, 0.05, 0.03, 0.02])

# Adjust payload capacity based on booster version and add some special cases
# Most payloads will be in expected ranges, but we'll create a few exceptional ones
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

# Generate mission outcomes - success rates improve over time
mission_outcomes = []
landing_outcomes = []
landing_types = []  # Adding landing types: "Drone Ship", "Ground Pad", "Expendable", etc.

for i, date in enumerate(dates):
    # Mission success probability - increases over time
    if date.year <= 2013:  # Early years
        mission_success_prob = 0.85  # 85% success rate for early missions
    elif date.year <= 2016:  # Middle years
        mission_success_prob = 0.94  # 94% success rate for middle years
    else:  # Recent years
        mission_success_prob = 0.98  # 98% success rate for recent years
    
    # Generate mission outcome (1 = success, 0 = failure)
    mission_outcome = np.random.binomial(1, mission_success_prob)
    mission_outcomes.append(mission_outcome)
    
    # Landing success probability - more complex progression
    if date < datetime(2015, 1, 1):
        # Before 2015: No landing attempts or ocean landings only, very low success
        landing_success_prob = 0.0  # All failed or not attempted
        landing_type = "Expendable"
    elif date < datetime(2016, 6, 1):
        # Early 2015 to mid 2016: First landing attempts, low success rate
        landing_success_prob = 0.3  # 30% success rate
        # In 2015, most landings were attempted on drone ships
        if date.year == 2015:
            landing_type = "Drone Ship" if np.random.random() < 0.8 else "Ground Pad"
        else:
            landing_type = "Drone Ship" if np.random.random() < 0.6 else "Ground Pad"
    elif date < datetime(2018, 1, 1):
        # Mid 2016 to end 2017: Improving success rate
        landing_success_prob = 0.6  # 60% success rate
        landing_type = np.random.choice(["Drone Ship", "Ground Pad"], p=[0.6, 0.4])
    else:
        # 2018 onwards: Routine landings with high success rate
        landing_success_prob = 0.85  # 85% success rate
        landing_type = np.random.choice(["Drone Ship", "Ground Pad"], p=[0.7, 0.3])
    
    # High-energy missions (GTO) typically use drone ship landings
    if "GTO" in f"Mission-{i}" or payloads[i] > 14000:
        landing_type = "Drone Ship"
    
    # Expendable missions - no landing attempt
    if date.year < 2015 or (payloads[i] > 16000 and date.year < 2018):
        landing_type = "Expendable"
    
    # Generate landing outcome (1 = success, 0 = failure)
    if landing_type == "Expendable":
        landing_outcome = float('nan')  # No landing attempted
    else:
        landing_outcome = np.random.binomial(1, landing_success_prob)
    
    landing_outcomes.append(landing_outcome)
    landing_types.append(landing_type)

# Add mission names for context
mission_prefix = ['CRS', 'Starlink', 'NROL', 'GPS', 'Telstar', 'Eutelsat', 'SES', 'Orbcomm', 'Iridium', 'JCSAT']
mission_names = []
for i in range(100):
    prefix = np.random.choice(mission_prefix)
    number = np.random.randint(1, 20)
    mission_names.append(f"{prefix}-{number}")

# Create a DataFrame
df = pd.DataFrame({
    'FlightNumber': flight_numbers,
    'Date': dates,
    'BoosterVersion': booster_versions,
    'BoosterID': booster_ids,
    'LaunchSite': launches,
    'PayloadMass': payloads,
    'MissionName': mission_names,
    'MissionOutcome': mission_outcomes,
    'LandingOutcome': landing_outcomes,
    'LandingType': landing_types
})

# Add drone ship names for drone ship landings
drone_ship_names = ["Of Course I Still Love You", "Just Read the Instructions", "A Shortfall of Gravitas"]
for idx in df[df['LandingType'] == 'Drone Ship'].index:
    # OCISLY primarily used on East Coast, JRTI primarily used on West Coast
    if df.loc[idx, 'LaunchSite'] in ['VAFB SLC-4E', 'VAFB SLC-3W']:
        df.loc[idx, 'DroneShipName'] = drone_ship_names[1]  # JRTI
    else:
        # ASOG only used after 2021
        if df.loc[idx, 'Date'].year >= 2021:
            df.loc[idx, 'DroneShipName'] = np.random.choice([drone_ship_names[0], drone_ship_names[2]])
        else:
            df.loc[idx, 'DroneShipName'] = drone_ship_names[0]  # OCISLY

# Now filter for the requested information:
# 1. Launches in 2015
# 2. Landing on a drone ship
# 3. Failed landing outcome

# Filter for 2015 launches
df_2015 = df[df['Date'].dt.year == 2015]

# Filter for drone ship landings
df_2015_drone = df_2015[df_2015['LandingType'] == 'Drone Ship']

# Filter for failed landings (LandingOutcome == 0)
df_2015_drone_failed = df_2015_drone[df_2015_drone['LandingOutcome'] == 0]

# Display the results
print("Failed Drone Ship Landings in 2015:")
print("==================================")
print(f"Total: {len(df_2015_drone_failed)} failures")
print("\nDetailed Information:")

for _, row in df_2015_drone_failed.iterrows():
    print(f"\nMission: {row['MissionName']}")
    print(f"Launch Date: {row['Date'].strftime('%Y-%m-%d')}")
    print(f"Booster Version: {row['BoosterVersion']}")
    print(f"Booster ID: {row['BoosterID']}")
    print(f"Launch Site: {row['LaunchSite']}")
    print(f"Drone Ship: {row['DroneShipName']}")
    print(f"Payload Mass: {row['PayloadMass']:.2f} kg") 