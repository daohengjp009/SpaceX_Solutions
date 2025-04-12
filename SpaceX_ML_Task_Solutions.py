"""
SpaceX Machine Learning Prediction - Part 5
Complete Task Solutions
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(y, y_predict):
    """this function plots the confusion matrix"""
    cm = confusion_matrix(y, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)  # annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

# Load the dataframes
# In the actual notebook, this would be:
# data = pd.read_csv("dataset_part_2.csv")
# X = pd.read_csv("dataset_part_3.csv")

# TASK 1: Create target variable Y
Y = data['Class'].to_numpy()

# TASK 2: Standardize the data
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

# TASK 3: Split data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Verify test set size
print("Test set shape:", Y_test.shape)  # Should show 18 samples

# TASK 4: Create and fit a GridSearchCV object for logistic regression
parameters = {'C': [0.01, 0.1, 1], 
              'penalty': ['l2'], 
              'solver': ['lbfgs']}
              
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)

# Display best parameters and score
print("Tuned hyperparameters (best parameters): ", logreg_cv.best_params_)
print("Accuracy: ", logreg_cv.best_score_)

# TASK 5: Calculate accuracy on test data for logistic regression
logreg_score = logreg_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(logreg_score))

# Plot confusion matrix for logistic regression
yhat = logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# TASK 6: Create and fit a GridSearchCV object for SVM
parameters = {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma': np.logspace(-3, 3, 5)}
              
svm = SVC()
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, Y_train)

# Display best parameters and score
print("Tuned hyperparameters (best parameters): ", svm_cv.best_params_)
print("Accuracy: ", svm_cv.best_score_)

# TASK 7: Calculate accuracy on test data for SVM
svm_score = svm_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(svm_score))

# Plot confusion matrix for SVM
yhat = svm_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# TASK 8: Create and fit a GridSearchCV object for decision tree
parameters = {'criterion': ['gini', 'entropy'],
              'splitter': ['best', 'random'],
              'max_depth': [2*n for n in range(1, 10)],
              'max_features': ['auto', 'sqrt'],
              'min_samples_leaf': [1, 2, 4],
              'min_samples_split': [2, 5, 10]}
              
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, Y_train)

# Display best parameters and score
print("Tuned hyperparameters (best parameters): ", tree_cv.best_params_)
print("Accuracy: ", tree_cv.best_score_)

# TASK 9: Calculate accuracy on test data for decision tree
tree_score = tree_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(tree_score))

# Plot confusion matrix for decision tree
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# TASK 10: Create and fit a GridSearchCV object for KNN
parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1, 2]}
              
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN, parameters, cv=10)
knn_cv.fit(X_train, Y_train)

# Display best parameters and score
print("Tuned hyperparameters (best parameters): ", knn_cv.best_params_)
print("Accuracy: ", knn_cv.best_score_)

# TASK 11: Calculate accuracy on test data for KNN
knn_score = knn_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(knn_score))

# Plot confusion matrix for KNN
yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)

# TASK 12: Find the best performing model
# Create a dictionary of models and their scores
models = {
    'Logistic Regression': logreg_score,
    'SVM': svm_score, 
    'Decision Tree': tree_score,
    'K-Nearest Neighbors': knn_score
}

# Find the best model
best_model = max(models, key=models.get)
print(f"The best performing model is: {best_model} with accuracy: {models[best_model]:.2f}")

# Compare all models
for model, score in models.items():
    print(f"{model}: {score:.2f}") 