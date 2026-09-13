import joblib
import sys


# ==========================================
# Load trained AI model
# ==========================================

model = joblib.load("model.pkl")


# ==========================================
# Get process information
# ==========================================

if len(sys.argv) != 5:

    print("Usage:")
    print("python predict_burst.py CPU_USAGE MEMORY_USAGE IO_OPERATIONS PROCESS_TYPE")

    sys.exit(1)


cpu_usage = float(sys.argv[1])
memory_usage = float(sys.argv[2])
io_operations = float(sys.argv[3])
process_type = float(sys.argv[4])


# ==========================================
# Prepare input
# ==========================================

process = [[
    cpu_usage,
    memory_usage,
    io_operations,
    process_type
]]


# ==========================================
# Predict burst time
# ==========================================

prediction = model.predict(process)[0]


# ==========================================
# Display result
# ==========================================

print("\n====================================")
print(" AI PROCESS BURST-TIME PREDICTION")
print("====================================")

print(f"CPU Usage       : {cpu_usage}")
print(f"Memory Usage    : {memory_usage}")
print(f"I/O Operations  : {io_operations}")
print(f"Process Type    : {process_type}")

print("------------------------------------")

print(f"Predicted Burst Time: {prediction:.2f}")

print("====================================")