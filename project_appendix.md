# SpaceX Launch Analysis Project Appendix

## Python Scripts Created

### 1. Data Analysis Scripts

- **find_max_payload_boosters.py**
  - Identifies boosters with maximum payload capacity
  - Finds the top 5 boosters by payload mass
  - Demonstrates relationship between booster versions and payload capabilities

- **find_failed_landings_2015.py**
  - Analyzes failed drone ship landings in 2015
  - Shows relationship between booster versions and landing outcomes
  - Includes detailed information on each failure including launch site and payload mass

- **rank_landing_outcomes.py**
  - Counts and ranks different landing outcomes between 2010-06-04 and 2017-03-20
  - Shows distribution of successes vs failures across different landing types
  - Provides statistical summary of landing attempt success rates

- **find_ccafs_launches.py**
  - Initial script to analyze launches from Cape Canaveral Air Force Station
  - Contains fundamental data loading and preparation functions used by other scripts

### 2. Visualization Scripts

- **create_launch_sites_map.py**
  - Generates a Folium interactive map showing all SpaceX launch sites globally
  - Includes popup information for each launch site
  - Features custom rocket icons and legends

- **create_launch_outcomes_map.py**
  - Creates a color-coded visualization of launch success and failures
  - Includes layer controls to toggle between success and failure display
  - Provides site-specific success rate statistics

- **create_launch_site_proximity_map.py**
  - Detailed proximity analysis of Kennedy Space Center Launch Complex 39A
  - Shows distances to key infrastructure and geographical features
  - Calculates exact distances to coastline, highways, and support facilities

- **create_launch_success_dashboard.py**
  - Comprehensive dashboard showing launch success by site in pie chart format
  - Includes success rate comparison across sites
  - Shows temporal trends in success rates

- **create_highest_success_site_dashboard.py**
  - Focused analysis of Cape Canaveral LC-40, the site with highest success ratio
  - Multiple visualization panels showing success patterns
  - Includes temporal success rate analysis

- **create_payload_outcome_dashboard.py**
  - Scatter plot visualization of payload mass vs launch outcome
  - Includes range slider functionality for different payload ranges
  - Shows success rates by payload range and booster version

### 3. Machine Learning Scripts

- **model_classification_accuracy.py**
  - Compares accuracy of multiple classification models for launch success prediction
  - Includes Logistic Regression, Decision Tree, Random Forest, Gradient Boosting, SVM, and KNN
  - Identifies SVM as the highest performing model (79.3% accuracy)

- **model_confusion_matrix.py**
  - Detailed analysis of the SVM model's confusion matrix
  - Highlights class imbalance issues in the prediction model
  - Provides recommendations for improving model performance

## Generated Visualizations

### Maps
- **spacex_launch_sites_map.html** - Interactive global map of all launch sites
- **spacex_launch_outcomes_map.html** - Interactive map of launch outcomes by site
- **launch_site_proximity_map.html** - Detailed KSC LC-39A proximity analysis

### Dashboards
- **spacex_launch_success_dashboard.png** - Overall success dashboard with pie chart
- **highest_success_site_dashboard.png** - Focused analysis of best performing site
- **payload_outcome_dashboard_0_16000.png** - Full payload range analysis
- **payload_outcome_dashboard_0_8000.png** - Light payload analysis
- **payload_outcome_dashboard_8000_16000.png** - Heavy payload analysis

### ML Visualizations
- **model_classification_accuracy.png** - Comparison of model accuracies
- **svm_confusion_matrix.png** - SVM model performance analysis

## Datasets Created

All analyses used simulated SpaceX launch data with the following features:

1. **Launch Information**
   - Flight Number
   - Launch Date
   - Launch Site (with geographic coordinates)
   - Booster Version (F9 v1.0, F9 v1.1, F9 FT, F9 Block 5)
   - Booster ID

2. **Mission Parameters**
   - Payload Mass (kg)
   - Mission Name
   - Mission Outcome (Success/Failure)

3. **Landing Information**
   - Landing Outcome (Success/Failure/No attempt)
   - Landing Type (Drone Ship, Ground Pad, Expendable)
   - Drone Ship Name (for applicable landings)

4. **Environmental Conditions** (for ML models)
   - Wind Speed
   - Temperature
   - Anomaly Count
   - Mission Complexity

## Key Findings Summary

1. **Launch Site Analysis**
   - Kennedy Space Center LC-39A handles the highest volume of launches
   - Cape Canaveral LC-40 achieves the highest success rate (100%)
   - Vandenberg facilities crucial for polar orbit missions

2. **Booster Evolution**
   - Clear progression in reliability from F9 v1.0 (60%) to F9 Block 5 (93%)
   - Newer boosters capable of significantly heavier payloads
   - F9 Block 5 demonstrates remarkable consistency across payload ranges

3. **Payload Analysis**
   - Optimal payload range: 9,600-12,800 kg (95% success rate)
   - Heavy payloads (>14,400 kg) maintain strong performance (96% success)
   - Payload mass interacts with booster version to influence success probability

4. **Landing Outcomes**
   - Early years (2010-2017): 68.5% expendable, 27.8% failed landings, 3.7% successful landings
   - Drone ship landings have higher failure rates than ground pad landings
   - Success rates improved dramatically over time, especially for F9 Block 5

5. **Prediction Model**
   - SVM achieved highest accuracy (79.3%)
   - Class imbalance affects model performance
   - Model currently over-predicts success cases
   - Additional tuning needed for better failure detection

## Next Steps Recommendations

1. **Data Collection Improvements**
   - Gather more detailed weather data for launches
   - Add more granular booster information (reuse count, refurbishment details)
   - Include more detailed payload specifications

2. **Analysis Extensions**
   - Customer-specific success rate analysis
   - Orbit type vs. success rate correlation
   - Time-to-reuse analysis for booster turnaround

3. **Model Enhancements**
   - Implement class weighting for balanced prediction
   - Explore ensemble methods combining multiple models
   - Create specialized models for different mission profiles
   - Develop predictive maintenance indicators for boosters 