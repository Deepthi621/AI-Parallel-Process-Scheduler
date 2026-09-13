import pandas as pd
import joblib


# ==========================================
# Load Trained Model
# ==========================================

model = joblib.load("model.pkl")


# ==========================================
# Load Unseen Test Workload
# ==========================================

data = pd.read_csv("../dataset/test_workload.csv")


# ==========================================
# Select Features
# ==========================================

features = [
    "cpu_usage",
    "memory_usage",
    "io_operations",
    "process_type"
]

X = data[features]


# ==========================================
# Predict Burst Time
# ==========================================

predictions = model.predict(X)


# ==========================================
# Add Predictions to Dataset
# ==========================================

data["predicted_burst_time"] = predictions.round(2)


# ==========================================
# Calculate Prediction Error
# ==========================================

data["prediction_error"] = (
    data["burst_time"] -
    data["predicted_burst_time"]
).abs().round(2)


# ==========================================
# Save Predictions
# ==========================================

output_columns = [
    "process_id",
    "arrival_time",
    "cpu_usage",
    "memory_usage",
    "io_operations",
    "process_type",
    "priority",
    "burst_time",
    "predicted_burst_time",
    "prediction_error"
]

data[output_columns].to_csv(
    "../dataset/predictions.csv",
    index=False
)


# ==========================================
# Display Results
# ==========================================

print("\n==========================================")
print(" AI PREDICTION RESULTS")
print("==========================================")

print(
    f"Test processes: {len(data)}"
)

print("\nSample Predictions:")

for _, row in data.head(10).iterrows():

    print(
        f"{row['process_id']}  "
        f"Actual: {row['burst_time']:.2f}  "
        f"Predicted: {row['predicted_burst_time']:.2f}  "
        f"Error: {row['prediction_error']:.2f}"
    )


# ==========================================
# Overall Prediction Error
# ==========================================

mean_error = data["prediction_error"].mean()

print(
    f"\nMean Prediction Error: {mean_error:.2f}"
)

print("\nPredictions saved to:")
print("../dataset/predictions.csv")

print("\nPrediction generation completed!")