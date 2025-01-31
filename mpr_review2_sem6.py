# -*- coding: utf-8 -*-
"""MPR_REVIEW2_SEM6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TUDuNmmIVKrg9mpOvaCdKuExTrCuxRj7
"""

import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# Step 1: Data Preparation
data = pd.read_csv('Car Data.csv')

# Step 2: Feature Engineering
# Selecting features and target variable
X = data[['Year', 'Mileage']]
y = data['Price']

# Manually implement train-test split
def train_test_split(X, y, test_size=0.2, random_state=None):
    if random_state:
        np.random.seed(random_state)

    # Shuffle indices
    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)

    # Calculate number of samples for testing
    num_test_samples = int(test_size * X.shape[0])

    # Split indices into training and testing sets
    test_indices = indices[:num_test_samples]
    train_indices = indices[num_test_samples:]

    # Split data based on indices
    X_train, X_test = X.iloc[train_indices], X.iloc[test_indices]
    y_train, y_test = y.iloc[train_indices], y.iloc[test_indices]

    return X_train, X_test, y_train, y_test

# Step 3: Model Training
# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Define Polynomial Regression Class
class PolynomialRegression:
    def __init__(self, degree):
        self.degree = degree

    def fit(self, X, y):
        # Create polynomial features
        self.X_poly = self.create_polynomial_features(X)

        # Solve for regression coefficients using normal equation
        self.coefficients = np.linalg.inv(self.X_poly.T.dot(self.X_poly)).dot(self.X_poly.T).dot(y)

    def predict(self, X):
        # Create polynomial features for prediction data
        X_poly = self.create_polynomial_features(X)

        # Predict using the coefficients
        y_pred = X_poly.dot(self.coefficients)
        return y_pred

    def create_polynomial_features(self, X):
        # Create polynomial features up to the specified degree
        X_poly = np.ones((len(X), 1))
        for i in range(1, self.degree + 1):
            X_poly = np.hstack((X_poly, X ** i))
        return X_poly

# Train the polynomial regression model
degree = 2  # Specify the degree of polynomial features
poly_regression = PolynomialRegression(degree=degree)
poly_regression.fit(X_train, y_train)

# Step 5: Define Model with Hidden Layers
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),  # Input layer
    tf.keras.layers.Dense(128, activation='relu'),  # Hidden layer with ReLU activation
    tf.keras.layers.Dense(64, activation='relu'),  # Hidden layer with ReLU activation
    tf.keras.layers.Dense(1)  # Output layer with 3 neurons for 3 outputs
])

# Step 6: Compile Model
model.compile(optimizer='adam', loss='mse')

# Step 7: Train Model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.1)

# Calculate R-squared manually
def r2_score(y_true, y_pred):
    sst = np.sum((y_true - np.mean(y_true))**2)
    ssr = np.sum((y_true - y_pred)**2)
    r2 = 1 - (ssr / sst)
    return r2

# Predict using the neural network model
y_pred = model.predict(X_test)

# Calculate R-squared for the neural network model
nn_r2 = r2_score(y_test, y_pred[:, 0])
print("Neural Network R^2:", nn_r2)

# Step 8: Model Evaluation for Polynomial Regression
# Make predictions
y_train_pred = poly_regression.predict(X_train)
y_test_pred = poly_regression.predict(X_test)

# Calculate R-squared for the polynomial regression model
poly_train_r2 = r2_score(y_train, y_train_pred)
poly_test_r2 = r2_score(y_test, y_test_pred)

print("Polynomial Regression Training R^2:", poly_train_r2)
print("Polynomial Regression Testing R^2:", poly_test_r2)

# Step 9: Prediction
# Example: Predicting the price of a car with Year=2022 and Mileage=30000
new_data = np.array([[2022, 30000]])
predicted_price = poly_regression.predict(new_data)
print("Predicted price (Polynomial Regression):", predicted_price)

# Step 10: Plotting the graph
plt.figure(figsize=(10, 6))

# Plot training data
plt.scatter(X_train['Mileage'], y_train, color='blue', label='Training Data')

# Plot testing data
plt.scatter(X_test['Mileage'], y_test, color='green', label='Testing Data')

# Plot regression line for training data
sort_axis_train = np.argsort(X_train['Mileage'])
plt.plot(X_train['Mileage'].iloc[sort_axis_train], y_train_pred[sort_axis_train], color='red', label='Regression Line (Polynomial Training)')

# Plot regression line for testing data
sort_axis_test = np.argsort(X_test['Mileage'])
plt.plot(X_test['Mileage'].iloc[sort_axis_test], y_test_pred[sort_axis_test], color='orange', label='Regression Line (Polynomial Testing)')

plt.title('Polynomial Regression')
plt.xlabel('Mileage')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()