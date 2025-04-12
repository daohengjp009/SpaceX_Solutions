import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.pipeline import Pipeline

# Set styling for plots
plt.style.use('ggplot')
sns.set_palette('colorblind')

# Reuse our existing launch data generation function from previous scripts
def generate_launch_data(num_launches=200):
    np.random.seed(42)  # For reproducibility
    
    # Create features that might predict launch success
    flight_numbers = np.arange(1, num_launches + 1)
    
    # Create booster versions (feature 1)
    booster_versions_num = []
    for flight_num in flight_numbers:
        if flight_num <= 5:
            booster_versions_num.append(1)  # F9 v1.0
        elif flight_num <= 20:
            booster_versions_num.append(2)  # F9 v1.1
        elif flight_num <= 60:
            booster_versions_num.append(3)  # F9 FT
        else:
            booster_versions_num.append(4)  # F9 Block 5
    
    # Generate payload mass (feature 2)
    payloads = []
    for version in booster_versions_num:
        if version == 1:  # F9 v1.0
            payloads.append(np.random.uniform(1000, 8000))
        elif version == 2:  # F9 v1.1
            payloads.append(np.random.uniform(3000, 12000))
        elif version == 3:  # F9 FT
            payloads.append(np.random.uniform(5000, 15000))
        else:  # F9 Block 5
            payloads.append(np.random.uniform(6000, 16000))
    
    # Generate simulated wind speeds at launch (feature 3)
    wind_speeds = np.random.normal(15, 7, num_launches)
    wind_speeds = np.clip(wind_speeds, 0, 35)  # Limit to realistic range
    
    # Generate temperature at launch (feature 4)
    temperatures = np.random.normal(22, 10, num_launches)
    
    # Generate launch pad anomalies count (feature 5)
    anomalies = np.random.poisson(2, num_launches)
    
    # Generate mission complexity score (feature 6)
    complexity = np.random.uniform(1, 10, num_launches)
    
    # Generate success probability based on features
    mission_outcomes = []
    for i in range(num_launches):
        # Base probability by booster version
        if booster_versions_num[i] == 1:
            base_prob = 0.75
        elif booster_versions_num[i] == 2:
            base_prob = 0.85
        elif booster_versions_num[i] == 3:
            base_prob = 0.92
        else:
            base_prob = 0.98
        
        # Adjust for payload (heavier payloads slightly reduce success chance)
        payload_factor = (payloads[i] - 1000) / 15000
        payload_effect = -0.08 * payload_factor * (5 - booster_versions_num[i])
        
        # Adjust for wind (high wind reduces success chance)
        wind_effect = -0.005 * max(0, wind_speeds[i] - 10)
        
        # Adjust for temperature (extreme temperatures reduce success chance)
        temp_effect = -0.005 * abs(temperatures[i] - 20)
        
        # Adjust for anomalies (more anomalies reduce success chance)
        anomaly_effect = -0.03 * anomalies[i]
        
        # Adjust for complexity (more complex missions reduce success chance)
        complexity_effect = -0.01 * complexity[i]
        
        # Calculate final probability
        success_prob = base_prob + payload_effect + wind_effect + temp_effect + anomaly_effect + complexity_effect
        
        # Ensure probability is valid
        success_prob = max(0.5, min(0.99, success_prob))
        
        # Generate outcome
        mission_outcomes.append(np.random.binomial(1, success_prob))
    
    # Create a DataFrame
    df = pd.DataFrame({
        'BoosterVersion': booster_versions_num,
        'PayloadMass': payloads,
        'WindSpeed': wind_speeds,
        'Temperature': temperatures,
        'AnomalyCount': anomalies,
        'MissionComplexity': complexity,
        'MissionSuccess': mission_outcomes
    })
    
    return df

# Generate launch data
launch_data = generate_launch_data(500)  # Generate more data for better model training

# Split into features and target
X = launch_data.drop('MissionSuccess', axis=1)
y = launch_data['MissionSuccess']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create pipeline with SVM model (the best performing model from our previous analysis)
svm_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', SVC(probability=True, random_state=42))
])

# Train the model
svm_pipeline.fit(X_train, y_train)

# Make predictions
y_pred = svm_pipeline.predict(X_test)

# Generate confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Calculate classification metrics
accuracy = accuracy_score(y_test, y_pred) * 100
report = classification_report(y_test, y_pred, output_dict=True)

# Get values from confusion matrix
tn, fp, fn, tp = cm.ravel()

# Calculate additional metrics
total = tn + fp + fn + tp
success_rate = (tp / (tp + fn)) * 100
failure_detection_rate = (tn / (tn + fp)) * 100

# Visualize confusion matrix
plt.figure(figsize=(10, 8))

# Create heatmap
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Failure (0)', 'Success (1)'],
            yticklabels=['Failure (0)', 'Success (1)'])

# Add labels
plt.xlabel('Predicted Label', fontsize=14)
plt.ylabel('True Label', fontsize=14)
plt.title('SVM Model Confusion Matrix - SpaceX Launch Success Prediction', fontsize=16, fontweight='bold')

# Add a text box with explanations
textstr = f"Model: Support Vector Machine (SVM)\n"
textstr += f"Accuracy: {accuracy:.1f}%\n\n"

textstr += f"True Positives (TP): {tp} - Correctly predicted successful launches\n"
textstr += f"True Negatives (TN): {tn} - Correctly predicted failed launches\n"
textstr += f"False Positives (FP): {fp} - Incorrectly predicted failed launches as successful\n"
textstr += f"False Negatives (FN): {fn} - Incorrectly predicted successful launches as failed\n\n"

textstr += f"Success Prediction Rate: {success_rate:.1f}%\n"
textstr += f"Failure Detection Rate: {failure_detection_rate:.1f}%\n\n"

textstr += "Interpretation:\n"
textstr += f"- The model correctly identified {tp} out of {tp + fn} successful launches\n"
textstr += f"- The model correctly identified {tn} out of {tn + fp} failed launches"

# Place text box on the figure
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.figtext(1.02, 0.5, textstr, fontsize=12, 
           bbox=props, verticalalignment='center', transform=plt.gca().transAxes)

# Adjust layout and save
plt.tight_layout(rect=[0, 0, 0.75, 1])  # Make room for the text box
plt.savefig('svm_confusion_matrix.png', dpi=300, bbox_inches='tight')

# Print the results
print("SVM Model Confusion Matrix Analysis:")
print("=" * 50)
print(f"Accuracy: {accuracy:.1f}%")
print("\nConfusion Matrix:")
print(f"    | Predicted Failure | Predicted Success |")
print(f"True Failure | {tn:17d} | {fp:17d} |")
print(f"True Success | {fn:17d} | {tp:17d} |")
print("\nClassification Report:")
for label, metrics in report.items():
    if label in ['0', '1']:
        label_name = 'Failure' if label == '0' else 'Success'
        print(f"\n{label_name} (Class {label}):")
        print(f"  Precision: {metrics['precision']:.3f}")
        print(f"  Recall:    {metrics['recall']:.3f}")
        print(f"  F1-Score:  {metrics['f1-score']:.3f}")
        print(f"  Support:   {metrics['support']}")

print("\nKey Insights:")
print(f"- Success Prediction Rate: {success_rate:.1f}%")
print(f"- Failure Detection Rate: {failure_detection_rate:.1f}%")
print(f"- The model is {'better at predicting successes' if success_rate > failure_detection_rate else 'better at detecting failures'}")
print("\nVisualization saved as 'svm_confusion_matrix.png'") 