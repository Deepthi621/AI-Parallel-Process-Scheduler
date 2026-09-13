import pandas as pd
import numpy as np


# ==========================================
# Configuration
# ==========================================

TRAINING_PROCESSES = 1000
TEST_PROCESSES = 100

np.random.seed(42)


# ==========================================
# Generate Process Data
# ==========================================

def generate_processes(number_of_processes, start_id=1):

    data = []

    for i in range(number_of_processes):

        process_number = start_id + i

        process_id = f"P{process_number}"

        # Arrival time
        arrival_time = i

        # Process characteristics
        cpu_usage = np.random.randint(20, 91)

        memory_usage = np.random.randint(100, 801)

        io_operations = np.random.randint(1, 11)

        process_type = np.random.randint(1, 4)

        priority = np.random.randint(1, 4)


        # ==================================
        # Generate realistic burst time
        # ==================================

        burst_time = (
            0.10 * cpu_usage
            + 0.005 * memory_usage
            - 0.40 * io_operations
            + 1.50 * process_type
            + np.random.normal(0, 1.5)
        )

        # Keep burst time within a reasonable range
        burst_time = max(2, min(30, burst_time))

        burst_time = round(burst_time, 2)


        data.append([
            process_id,
            arrival_time,
            cpu_usage,
            memory_usage,
            io_operations,
            process_type,
            priority,
            burst_time
        ])


    columns = [
        "process_id",
        "arrival_time",
        "cpu_usage",
        "memory_usage",
        "io_operations",
        "process_type",
        "priority",
        "burst_time"
    ]

    return pd.DataFrame(data, columns=columns)


# ==========================================
# Generate Training Dataset
# ==========================================

training_data = generate_processes(
    TRAINING_PROCESSES,
    1
)

training_data.to_csv(
    "../dataset/process_data.csv",
    index=False
)


# ==========================================
# Generate Test Workload
# ==========================================

test_data = generate_processes(
    TEST_PROCESSES,
    TRAINING_PROCESSES + 1
)

test_data.to_csv(
    "../dataset/test_workload.csv",
    index=False
)


# ==========================================
# Display Results
# ==========================================

print("\n==========================================")
print(" PROCESS DATASET GENERATION")
print("==========================================")

print(
    f"Training processes : {len(training_data)}"
)

print(
    f"Test processes     : {len(test_data)}"
)

print("\nTraining dataset saved to:")
print("../dataset/process_data.csv")

print("\nTest workload saved to:")
print("../dataset/test_workload.csv")

print("\nSample training data:")
print(training_data.head())

print("\nSample test workload:")
print(test_data.head())

print("\nDataset generation completed!")