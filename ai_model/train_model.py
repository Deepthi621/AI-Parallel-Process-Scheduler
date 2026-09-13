import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score


# ==========================================
# Load Dataset
# ==========================================

data = pd.read_csv("../dataset/process_data.csv")


# ==========================================
# Select Features and Target
# ==========================================

features = [
    "cpu_usage",
    "memory_usage",
    "io_operations",
    "process_type"
]

X = data[features]
y = data["burst_time"]


# ==========================================
# Split Dataset
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==========================================
# Create Random Forest Model
# ==========================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# ==========================================
# Train Model
# ==========================================

print("\nTraining AI model...")

model.fit(X_train, y_train)


# ==========================================
# Make Predictions
# ==========================================

predictions = model.predict(X_test)


# ==========================================
# Evaluate Model
# ==========================================

mae = mean_absolute_error(
    y_test,
    predictions
)

r2 = r2_score(
    y_test,
    predictions
)


# ==========================================
# Display Results
# ==========================================

print("\n==========================================")
print(" AI MODEL RESULTS")
print("==========================================")

print(
    f"Total processes   : {len(data)}"
)

print(
    f"Training samples  : {len(X_train)}"
)

print(
    f"Testing samples   : {len(X_test)}"
)

print(
    f"Mean Absolute Error : {mae:.2f}"
)

print(
    f"R2 Score            : {r2:.2f}"
)


# ==========================================
# Show Sample Predictions
# ==========================================

print("\nSample Predictions:")

for actual, predicted in zip(
    y_test.iloc[:10],
    predictions[:10]
):
    print(
        f"Actual: {actual:.2f} "
        f"Predicted: {predicted:.2f}"
    )


# ==========================================
# Save Model
# ==========================================

joblib.dump(
    model,
    "model.pkl"
)

print("\nModel saved as:")
print("model.pkl")

print("\nTraining completed successfully!")