import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# Load Performance Results
# ==========================================

results = pd.read_csv(
    "../results/performance_results.csv"
)


# ==========================================
# 1. Execution Time vs Threads
# ==========================================

omp = results[
    results["scheduler"] == "OpenMP SJF"
]

ai = results[
    results["scheduler"] == "AI + OpenMP"
]


plt.figure(figsize=(8, 5))

plt.plot(
    omp["threads"],
    omp["execution_time"],
    marker="o",
    label="OpenMP SJF"
)

plt.plot(
    ai["threads"],
    ai["execution_time"],
    marker="o",
    label="AI + OpenMP"
)

plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (seconds)")
plt.title("Execution Time vs Number of Threads")
plt.xticks([1, 2, 4, 8, 12])
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "../results/execution_time_vs_threads.png",
    dpi=300
)

plt.close()


# ==========================================
# 2. Speedup vs Threads
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    omp["threads"],
    omp["speedup"],
    marker="o",
    label="OpenMP SJF"
)

plt.plot(
    ai["threads"],
    ai["speedup"],
    marker="o",
    label="AI + OpenMP"
)

plt.xlabel("Number of Threads")
plt.ylabel("Speedup")
plt.title("Speedup vs Number of Threads")
plt.xticks([1, 2, 4, 8, 12])
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "../results/speedup_vs_threads.png",
    dpi=300
)

plt.close()


# ==========================================
# 3. Thread Utilization vs Threads
# ==========================================

plt.figure(figsize=(8, 5))

plt.plot(
    ai["threads"],
    ai["utilization"],
    marker="o",
    label="AI + OpenMP"
)

plt.xlabel("Number of Threads")
plt.ylabel("Thread Utilization (%)")
plt.title("AI + OpenMP Thread Utilization")
plt.xticks([1, 2, 4, 8, 12])
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "../results/thread_utilization.png",
    dpi=300
)

plt.close()


# ==========================================
# 4. Actual vs Predicted Burst Time
# ==========================================

predictions = pd.read_csv(
    "../dataset/predictions.csv"
)

plt.figure(figsize=(9, 5))

process_numbers = range(
    1,
    len(predictions) + 1
)

plt.plot(
    process_numbers,
    predictions["burst_time"],
    marker="o",
    markersize=3,
    label="Actual Burst Time"
)

plt.plot(
    process_numbers,
    predictions["predicted_burst_time"],
    marker="x",
    markersize=3,
    label="AI Predicted Burst Time"
)

plt.xlabel("Test Process")
plt.ylabel("Burst Time")
plt.title("Actual vs AI-Predicted Burst Time")
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    "../results/actual_vs_predicted.png",
    dpi=300
)

plt.close()


# ==========================================
# Completion Message
# ==========================================

print("\n==========================================")
print(" GRAPHS GENERATED SUCCESSFULLY")
print("==========================================")

print("\nCreated files:")

print("1. execution_time_vs_threads.png")
print("2. speedup_vs_threads.png")
print("3. thread_utilization.png")
print("4. actual_vs_predicted.png")

print("\nAll graphs saved in:")
print("../results/")