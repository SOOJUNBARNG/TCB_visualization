# NYAN
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Optionally, visualize the tree (requires matplotlib)
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt


# Load CSV file into DataFrame
csv_file_path = r"C:\Users\powwe\Documents\MF_data_analysis_divison\External\result.csv"
transactions_df = pd.read_csv(csv_file_path)

# Define the number of bins
num_bins = 10

# Define quantiles for 10 bins
quantiles = (
    transactions_df["net_value"]
    .quantile([i / num_bins for i in range(num_bins + 1)])
    .values
)
labels = [f"Bin {i + 1}" for i in range(num_bins)]

# Create a new column with binned data
transactions_df["net_value_binned"] = pd.cut(
    transactions_df["net_value"], bins=quantiles, labels=labels, include_lowest=True
)

# # Count occurrences in each bin
# bin_counts = transactions_df['net_value_binned'].value_counts()
# print(bin_counts)
