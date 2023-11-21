
import matplotlib.pyplot as plt
import numpy as np
from src.LinearApriori import LinearAprioriRunner
from src.SparkApriori import ParallelAprioriRunner

# Assuming the datasets are in the specified paths
# pumsb = "./pumsb.dat"
chess = "./dataset/chess.dat"
mushroom = "./dataset/mushroom.dat"
pumsb = "./dataset/pumsb.dat"


# Function to run both Linear and Parallel Apriori and plot the results
def run_and_plot(dataset_path, support_threshold):
    # Run Parallel Apriori
    time_list_p,total_time_p = ParallelAprioriRunner(dataset_path, support_threshold)

    # Run Linear Apriori
    time_list_s,total_time_s = LinearAprioriRunner(dataset_path, support_threshold)
    min_length = min(len(time_list_p),len(time_list_s))
    # Create a list for the x-axis (pass of iteration)
    # k_list = list(range(1, min_length + 1))
    k_list = np.arange(min_length)
    total_time_p=sum(time_list_p)
    total_time_s=sum(time_list_s)
    print(total_time_p,total_time_s)
    # Plot Parallel and Linear Apriori on the same figure
    plt.figure(figsize=(10, 6))
    print(time_list_s)
    print(time_list_p)
    print(k_list)
    width=0.2
    plt.bar(k_list, time_list_p[:min_length], color='blue', width=0.2, label='Parallel Apriori')
    plt.bar(k_list+width, time_list_s[:min_length], color='orange', width=0.2, label='Linear Apriori')

    plt.xlabel("Pass of Iteration [k]")
    plt.ylabel("Execution time (seconds)")
    plt.title(f"Execution Time Comparison for Dataset: {dataset_path}")
    plt.legend()
    plt.show()
    return total_time_p,total_time_s

total_time_p,total_time_s = run_and_plot(pumsb, 0.9)
print(total_time_p,total_time_s)