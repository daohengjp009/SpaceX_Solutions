# SpaceX Falcon 9 First Stage Landing Prediction
## Summary and Explanation of Machine Learning Tasks

## Project Overview

SpaceX advertises Falcon 9 rocket launches for approximately $62 million, while other providers charge upwards of $165 million per launch. A significant portion of SpaceX's cost savings comes from their ability to reuse the first stage of the rocket. 

This project uses machine learning to predict whether a Falcon 9 first stage will successfully land after launch. This prediction could help competitors estimate SpaceX's launch costs and develop more competitive bidding strategies.

## Dataset

The project uses two datasets:
1. `dataset_part_2.csv` - Contains launch information, including outcomes and landing details
2. `dataset_part_3.csv` - Contains feature-engineered data with one-hot encoded categorical variables

Key features include:
- Flight number
- Payload mass
- Orbit type
- Launch site
- Grid fins usage
- Reused components
- Number of flights
- Landing pad information

## Machine Learning Workflow

### Task 1: Creating the Target Variable
```python
Y = data['Class'].to_numpy()
```
We extract the 'Class' column from the dataset to create our target variable. The column contains binary values where:
- 0 = unsuccessful landing
- 1 = successful landing

### Task 2: Standardizing Features
```python
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)
```
Standardization transforms all features to have a mean of 0 and a standard deviation of 1. This is important because:
- It prevents features with large values from dominating the model
- It improves convergence speed for many algorithms
- It makes feature coefficients more comparable

### Task 3: Splitting the Dataset
```python
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
```
We split the data with:
- 80% for training: Used to build the model
- 20% for testing: Used to evaluate model performance on unseen data
- Random state = 2: Ensures reproducibility

### Task 4-5: Logistic Regression Model
```python
parameters = {'C':[0.01, 0.1, 1], 'penalty':['l2'], 'solver':['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)
```
Logistic Regression is appropriate for this binary classification problem because:
- It naturally outputs probabilities of landing success
- It's less prone to overfitting when properly regularized
- It provides interpretable coefficients

We use GridSearchCV with 10-fold cross-validation to find the optimal regularization strength (C parameter).

### Task 6-7: Support Vector Machine (SVM)
```python
parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma': np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, Y_train)
```
SVM creates an optimal hyperplane to separate successful and unsuccessful landings:
- Can handle non-linear decision boundaries with kernel functions
- Focuses on maximizing the margin between classes
- Robust against overfitting in high-dimensional spaces

We explore multiple kernels and parameters to find the best configuration.

### Task 8-9: Decision Tree Classifier
```python
parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, Y_train)
```
Decision Trees create a flowchart-like structure:
- Naturally handle feature interactions
- Can capture non-linear patterns
- Produce highly interpretable rules

We tune multiple parameters to prevent overfitting and optimize performance.

### Task 10-11: K-Nearest Neighbors (KNN)
```python
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1, 2]}
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN, parameters, cv=10)
knn_cv.fit(X_train, Y_train)
```
KNN makes predictions based on the most similar historical launches:
- Makes predictions based on feature similarity
- Non-parametric (doesn't assume data distribution)
- Simple but effective for many problems

We primarily tune the number of neighbors (k) and distance metric.

### Task 12: Model Comparison and Selection
```python
models = {
    'Logistic Regression': logreg_score,
    'SVM': svm_score, 
    'Decision Tree': tree_score,
    'K-Nearest Neighbors': knn_score
}

best_model = max(models, key=models.get)
```
All models show similar performance with 83% accuracy on the test set. This indicates:
1. The problem has clear patterns that most algorithms can capture
2. With limited test data (18 samples), the differences between models may not be apparent
3. Model selection could consider factors beyond accuracy, such as:
   - Interpretability (Logistic Regression, Decision Tree)
   - Speed (Logistic Regression is typically fastest)
   - Ability to handle future data (SVM often generalizes well)

## Confusion Matrix Analysis

For each model, we generate confusion matrices to understand error patterns:
```python
yhat = model_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)
```

Most models show a pattern where false positives (predicting landing when it doesn't occur) are more common than false negatives. This suggests the models tend to be optimistic about landing success.

## Business Impact

This prediction capability would allow SpaceX competitors to:
1. Better estimate SpaceX's operational costs
2. Understand what factors contribute to successful landings
3. Develop their own reusable rocket technology more efficiently
4. Create more competitive pricing strategies

## Key Learning Outcomes

1. Applied machine learning to a real-world aerospace industry problem
2. Compared multiple classification algorithms on the same problem
3. Used hyperparameter tuning to optimize model performance
4. Analyzed prediction errors through confusion matrices
5. Learned to interpret model results in a business context

## Parameter Selection Guidelines

### General Approach
1. **Start simple**, then increase complexity
2. **Use domain knowledge** when possible
3. **Let data guide you** via cross-validation
4. **Avoid overfitting** by monitoring validation performance

### Parameter Selection Guidelines by Model

#### Logistic Regression
- **C parameter** (inverse regularization strength):
  - Start with C=1.0
  - Smaller C (0.1, 0.01) = stronger regularization (for many features)
  - Larger C (10, 100) = less regularization (for few features)
- **Penalty**: L2 (ridge) is default, L1 (lasso) for feature selection

#### Support Vector Machines
- **Kernel**: 
  - Linear: Start with this for high-dimensional data
  - RBF: For most non-linear problems
  - Polynomial: When features have clear interactions
  - Sigmoid: When data resembles probability distributions
- **C parameter**: Similar to logistic regression
- **Gamma**: Controls decision boundary flexibility
  - Low gamma: Smoother boundaries
  - High gamma: Can fit complex boundaries but may overfit

#### Decision Trees
- **Max depth**: Often 3-10 is sufficient; use cross-validation
- **Min samples split/leaf**: Higher values prevent overfitting
  - Small datasets: 5-10
  - Large datasets: 20-50
- **Criterion**: Gini usually works well, but test both

#### K-Nearest Neighbors
- **K value**: Often sqrt(n) where n is sample size
  - Small k (1-5): Complex boundaries, may overfit
  - Large k (10+): Smoother boundaries
- **Distance metric**: Euclidean (p=2) for most problems, Manhattan (p=1) for high-dimensional data

### Practical Workflow
1. **Grid Search**: When you have computing resources and few parameters
2. **Random Search**: Better for many parameters with wide ranges
3. **Bayesian Optimization**: For computationally expensive models
4. **Start with default parameters**, then tune most important ones first

### Key Parameters to Focus On
Focus on parameters with largest impact:
- SVM: kernel, C, gamma
- Tree: max_depth, min_samples_split
- KNN: n_neighbors
- All models: regularization parameters

For the SpaceX landing prediction task, our SVM model found the sigmoid kernel with C=1.0 and gamma=0.03162 to perform best on validation data, achieving 84.82% accuracy. This demonstrates how empirical testing through cross-validation remains the most reliable approach to parameter selection. 