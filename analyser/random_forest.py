"""
Random Forest Regressor for Toronto Shelter Occupancy Forecasting

Predicts OCCUPIED_BEDS from various metadata while avoiding common pitfalls such as target leakage.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Force sklearn pipeline outputs to be numpy arrays (prevents pandas column renaming issues)
from sklearn import set_config
set_config(transform_output="default")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

os.makedirs("analyser", exist_ok=True)

# ==== Step 1: Load Dataset ====
file_path = "../dataset/all_data.csv"
df = pd.read_csv(file_path, low_memory=False)

print("Actual column names in the dataset:")
print(df.columns.tolist())

# Create a subset with relevant columns.
# NOTE: We've removed 'CAPACITY_ACTUAL_BED' to reduce the chance of target leakage.
df_subset = df[[
    "OCCUPANCY_DATE", 
    "ORGANIZATION_NAME",
    "SHELTER_GROUP",
    "LOCATION_NAME",
    "LOCATION_POSTAL_CODE",
    "PROGRAM_ID",
    "OCCUPIED_BEDS",          # target
    "Max Temp (Â°C)",
    "Min Temp (Â°C)",
    "Inflation_Rate_Change",
    "Population", 
    "Unemployment rate 10"
]].dropna()  # Remove any rows with missing values in these key columns

print("Subset created. Shape:", df_subset.shape)

# ==== Step 2: Define Features & Target ====
target_col = "OCCUPIED_BEDS"
date_col = "OCCUPANCY_DATE"

# Drop the target and date columns from the predictors
X = df_subset.drop(columns=[target_col, date_col])
y = df_subset[target_col]

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include="object").columns.tolist()
numerical_cols = X.select_dtypes(include=np.number).columns.tolist()

print("Categorical columns:", categorical_cols)
print("Numerical columns:", numerical_cols)

# ==== Step 3: Build the Preprocessor Using a ColumnTransformer ====
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
        ("num", StandardScaler(), numerical_cols)
    ]
)

# ==== Step 4: Construct the Pipeline ====
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# ==== Step 5: Split the Data ====
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Training shape:", X_train.shape, "Test shape:", X_test.shape)

# ==== Step 6: Train the Model ====
model.fit(X_train, y_train)
print("Model training complete.")

# ==== Step 7: Predict & Evaluate ====
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# ==== Step 8: Plot Actual vs Predicted (First 100 Samples) ====
plt.figure(figsize=(10, 6))
plt.plot(y_test.values[:100], label="Actual", alpha=0.7)
plt.plot(y_pred[:100], label="Predicted", alpha=0.7)
plt.title("Random Forest Predictions vs Actual (First 100 Points)")
plt.xlabel("Sample Index")
plt.ylabel("Occupied Beds")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("random_forest_results_toronto.png")
plt.show()

