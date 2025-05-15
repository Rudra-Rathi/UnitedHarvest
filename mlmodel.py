import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
import matplotlib.pyplot as plt

# Load and preprocess the data
df = pd.read_csv("synthetic_individual_prices_realistic_dates.csv")
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values("date")

# Function to create lagged features
def create_lagged_features(df, column, n_lags=5):
    temp_df = pd.DataFrame()
    for i in range(1, n_lags + 1):
        temp_df[f'{column}lag{i}'] = df[column].shift(i)
    temp_df[f'{column}_target'] = df[column]
    temp_df['date'] = df['date']
    return temp_df.dropna()

# Define product and create lagged features
product = "mango"
lagged = create_lagged_features(df, product, n_lags=5)

# Prepare features and target
X = lagged[[f'{product}lag{i}' for i in range(1, 6)]]
y = lagged[f'{product}_target']
dates = lagged['date']

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

# Train XGBoost model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print(f"RMSE on {product} prediction: {rmse:.2f}")

# Plot actual vs predicted
plt.figure(figsize=(12, 6))
plt.plot(dates.iloc[-len(y_test):], y_test.values, label="Actual")
plt.plot(dates.iloc[-len(y_test):], y_pred, label="Predicted")
plt.title(f"{product.capitalize()} Price Prediction")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
