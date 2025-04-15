import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# === Optional: Hide dtype warnings ===
warnings.filterwarnings('ignore', category=pd.errors.DtypeWarning)

# === LOAD DATA ===
df = pd.read_csv('../dataset/all_data.csv', parse_dates=['OCCUPANCY_DATE'], low_memory=False)

# === CLEANING ===
df = df.dropna(subset=['OCCUPIED_BEDS'])              # Drop rows with missing target
df.fillna(0, inplace=True)                            # Fill other missing values

# === FEATURE ENGINEERING ===
df['DAY'] = df['OCCUPANCY_DATE'].dt.day
df['MONTH'] = df['OCCUPANCY_DATE'].dt.month
df['YEAR'] = df['OCCUPANCY_DATE'].dt.year
df['WEEKDAY'] = df['OCCUPANCY_DATE'].dt.weekday

# === SELECT RELEVANT COLUMNS ===
columns_to_keep = [
    'OCCUPIED_BEDS',
    'Max Temp (Â°C)',
    'Min Temp (Â°C)',
    'Inflation_Rate_Change',
    'Population',
    'Unemployment rate 10',
    'DAY', 'MONTH', 'YEAR', 'WEEKDAY'
]

df_model = df[columns_to_keep].copy()

# === HANDLE DTYPE ISSUES ===
df_model['Max Temp (Â°C)'] = pd.to_numeric(df_model['Max Temp (Â°C)'], errors='coerce')
df_model['Min Temp (Â°C)'] = pd.to_numeric(df_model['Min Temp (Â°C)'], errors='coerce')
df_model['Inflation_Rate_Change'] = pd.to_numeric(df_model['Inflation_Rate_Change'], errors='coerce')
df_model['Population'] = pd.to_numeric(df_model['Population'], errors='coerce')
df_model['Unemployment rate 10'] = pd.to_numeric(df_model['Unemployment rate 10'], errors='coerce')
df_model.dropna(inplace=True)

# === SPLIT ===
X = df_model.drop(columns=['OCCUPIED_BEDS'])
y = df_model['OCCUPIED_BEDS']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# === TRAIN ===
rf = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
rf.fit(X_train, y_train)

# === PREDICT ===
y_pred = rf.predict(X_test)

# === METRICS ===
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n==== Random Forest Model Evaluation ====")
print(f'R² Score: {r2:.4f}')
print(f'MAE: {mae:.2f}')
print(f'RMSE: {rmse:.2f}')
print("========================================\n")

# === PLOT: ACTUAL vs PREDICTED ===
plt.figure(figsize=(12, 6))
plt.plot(y_test.values[:100], label='Actual', marker='o')
plt.plot(y_pred[:100], label='Predicted', marker='x')
plt.title('Actual vs Predicted Bed Occupancy')
plt.xlabel('Sample Index')
plt.ylabel('Occupied Beds')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('random_forest_results_toronto.png')
plt.show()

# === PLOT: FEATURE IMPORTANCE ===
importances = pd.Series(rf.feature_importances_, index=X.columns)
top_features = importances.nlargest(10)

plt.figure(figsize=(8, 6))
top_features.plot(kind='barh')
plt.title("Top Feature Importances")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.show()

