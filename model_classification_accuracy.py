import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
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

# Define the models to evaluate
models = {
    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingClassifier(random_state=42),
    'SVM': SVC(probability=True, random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5)
}

# Create pipelines for each model
pipelines = {}
for name, model in models.items():
    pipelines[name] = Pipeline([
        ('scaler', StandardScaler()),
        ('model', model)
    ])

# Train and evaluate each model
accuracy_scores = {}
for name, pipeline in pipelines.items():
    # Train the model
    pipeline.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = pipeline.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    accuracy_scores[name] = accuracy * 100  # Convert to percentage

# Create a visualization of model accuracy
plt.figure(figsize=(12, 8))

# Sort models by accuracy
sorted_models = sorted(accuracy_scores.items(), key=lambda x: x[1], reverse=True)
model_names = [model[0] for model in sorted_models]
accuracies = [model[1] for model in sorted_models]

# Create a bar chart
bars = plt.bar(model_names, accuracies, color='blue', alpha=0.7)

# Add data labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=12)

# Add a horizontal line for average accuracy
avg_accuracy = sum(accuracies) / len(accuracies)
plt.axhline(y=avg_accuracy, color='red', linestyle='--', 
           label=f'Average Accuracy: {avg_accuracy:.1f}%')

# Highlight the best model
best_model_name = model_names[0]
best_model_accuracy = accuracies[0]
bars[0].set_color('green')

# Add labels and title
plt.xlabel('Classification Model', fontsize=14)
plt.ylabel('Accuracy (%)', fontsize=14)
plt.title('SpaceX Launch Success Prediction: Model Accuracy Comparison', fontsize=18, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.ylim(min(accuracies) - 5, 102)  # Make room for data labels
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()

# Add a text box with key findings
textstr = f"Best Model: {best_model_name} ({best_model_accuracy:.1f}%)\n"
textstr += f"Average Accuracy: {avg_accuracy:.1f}%\n"
textstr += f"Number of Features: {X.shape[1]}\n"
textstr += f"Training Data Size: {len(X_train)}\n"
textstr += f"Test Data Size: {len(X_test)}"

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.text(0.05, 0.05, textstr, transform=plt.gca().transAxes, fontsize=12,
        verticalalignment='bottom', bbox=props)

# Adjust layout and save
plt.tight_layout()
plt.savefig('model_classification_accuracy.png', dpi=300, bbox_inches='tight')

# Print the results
print("Model Classification Accuracy Results:")
print("=" * 50)
print(f"{'Model':<25} {'Accuracy (%)':<15}")
print("-" * 50)

for model_name, accuracy in sorted_models:
    print(f"{model_name:<25} {accuracy:<15.1f}")

print("\nBest performing model:", best_model_name, f"({best_model_accuracy:.1f}%)")
print("Visualization saved as 'model_classification_accuracy.png')") 