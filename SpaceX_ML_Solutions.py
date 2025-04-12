"""
SpaceX Machine Learning Prediction - Part 5
Complete Solution Code for All Tasks
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

# Define the confusion matrix plotting function
def plot_confusion_matrix(y, y_predict):
    """This function plots the confusion matrix"""
    cm = confusion_matrix(y, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax)  # annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix')
    ax.xaxis.set_ticklabels(['did not land', 'land'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    plt.show()

# Load data (in actual execution, uncomment and adjust the following lines)
# data = pd.read_csv("dataset_part_2.csv")
# X = pd.read_csv("dataset_part_3.csv")

print("Data Loading and Preparation")
print("-----------------------------")
print("In a real execution, the data would be loaded from files or URLs.")
print("For this example, we're providing the code but not executing the data loading.")

# TASK 1: Create a NumPy array from the column 'Class' in data
print("\nTASK 1: Create target variable Y")
print("--------------------------------")
print("Y = data['Class'].to_numpy()")
print("This converts the 'Class' column to a NumPy array for the target variable.")

# TASK 2: Standardize the data
print("\nTASK 2: Standardize the feature data")
print("-----------------------------------")
print("transform = preprocessing.StandardScaler()")
print("X = transform.fit_transform(X)")
print("This standardizes all features to have mean=0 and standard deviation=1.")

# TASK 3: Split the data into training and testing sets
print("\nTASK 3: Split data into training and testing sets")
print("----------------------------------------------")
print("X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)")
print("This splits the data with 80% for training and 20% for testing.")

# TASK 4: Create a GridSearchCV object for logistic regression
print("\nTASK 4: Logistic Regression with GridSearchCV")
print("--------------------------------------------")
print("""parameters = {'C':[0.01, 0.1, 1], 'penalty':['l2'], 'solver':['lbfgs']}
lr = LogisticRegression()
logreg_cv = GridSearchCV(lr, parameters, cv=10)
logreg_cv.fit(X_train, Y_train)
print("Tuned hyperparameters (best parameters): ", logreg_cv.best_params_)
print("Accuracy: ", logreg_cv.best_score_)""")
print("This finds the best parameters for logistic regression using 10-fold cross-validation.")

# TASK 5: Calculate accuracy of logistic regression on test data
print("\nTASK 5: Calculate logistic regression accuracy on test data")
print("--------------------------------------------------------")
print("""logreg_score = logreg_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(logreg_score))""")
print("This evaluates how well the tuned logistic regression performs on unseen test data.")

# TASK 6: Create a GridSearchCV object for SVM
print("\nTASK 6: Support Vector Machine with GridSearchCV")
print("----------------------------------------------")
print("""parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma': np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(svm, parameters, cv=10)
svm_cv.fit(X_train, Y_train)
print("Tuned hyperparameters (best parameters): ", svm_cv.best_params_)
print("Accuracy: ", svm_cv.best_score_)""")
print("This finds the optimal SVM configuration through grid search.")

# TASK 7: Calculate accuracy of SVM on test data
print("\nTASK 7: Calculate SVM accuracy on test data")
print("-------------------------------------------")
print("""svm_score = svm_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(svm_score))""")
print("This evaluates the tuned SVM model on the test dataset.")

# TASK 8: Create a GridSearchCV object for decision tree
print("\nTASK 8: Decision Tree with GridSearchCV")
print("--------------------------------------")
print("""parameters = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(tree, parameters, cv=10)
tree_cv.fit(X_train, Y_train)
print("Tuned hyperparameters (best parameters): ", tree_cv.best_params_)
print("Accuracy: ", tree_cv.best_score_)""")
print("This finds the best decision tree configuration using grid search.")

# TASK 9: Calculate accuracy of decision tree on test data
print("\nTASK 9: Calculate Decision Tree accuracy on test data")
print("---------------------------------------------------")
print("""tree_score = tree_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(tree_score))""")
print("This evaluates the optimized decision tree on the test dataset.")

# TASK 10: Create a GridSearchCV object for KNN
print("\nTASK 10: K-Nearest Neighbors with GridSearchCV")
print("--------------------------------------------")
print("""parameters = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1, 2]}
KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(KNN, parameters, cv=10)
knn_cv.fit(X_train, Y_train)
print("Tuned hyperparameters (best parameters): ", knn_cv.best_params_)
print("Accuracy: ", knn_cv.best_score_)""")
print("This tunes the KNN model to find optimal parameters.")

# TASK 11: Calculate accuracy of KNN on test data
print("\nTASK 11: Calculate KNN accuracy on test data")
print("------------------------------------------")
print("""knn_score = knn_cv.score(X_test, Y_test)
print("Test set accuracy: {:.2f}".format(knn_score))""")
print("This evaluates the tuned KNN model on the test dataset.")

# TASK 12: Find the best performing model
print("\nTASK 12: Find the best performing model")
print("--------------------------------------")
print("""# Create a dictionary of models and their scores
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
    print(f"{model}: {score:.2f}")""")
print("This compares all models to identify which performs best on the test data.")

print("\nNOTE: In actual execution, you would also plot confusion matrices for each model using:")
print("yhat = model_cv.predict(X_test)")
print("plot_confusion_matrix(Y_test, yhat)") 