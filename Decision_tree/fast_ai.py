import cudf
from cuml.model_selection import train_test_split
from cuml.tree import DecisionTreeClassifier
from cuml.metrics import classification_report, accuracy_score
from cuml import get_dummies
import matplotlib.pyplot as plt
from cuml.tree import (
    plot_tree,
)  # Assuming you have a compatible version for visualization

# Load CSV file into cuDF DataFrame
csv_file_path = r"C:\Users\powwe\Documents\MF_data_analysis_divison\External\result.csv"
transactions_df = cudf.read_csv(csv_file_path)

# Check for null values
if transactions_df.isnull().sum().any():
    print("There are null values in the dataset. Consider handling them.")
    transactions_df.fillna(0, inplace=True)  # Example of filling nulls with 0

# Prepare data (assume 'net_value' is your target variable)
X = transactions_df.drop(columns=["net_value"])  # Features
y = transactions_df["net_value"]  # Target variable

# Specify columns to be one-hot encoded
columns_to_encode = [
    "discount_rate",
    "service",
    "tcb_item_name",
    "sex",
    "prefecture_code",
    "set_unit",
    "staff_name",
]

# Create dummy variables only for the specified columns using cuDF
X_encoded = get_dummies(X[columns_to_encode], drop_first=True)

# Select only numeric columns from the original DataFrame
numeric_columns = X.drop(columns=columns_to_encode).select_dtypes(
    include=["int", "float"]
)

# Combine with the rest of the DataFrame
X = cudf.concat([numeric_columns, X_encoded], axis=1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Create a Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Visualize the tree (if compatible, otherwise you may need to skip this part)
plt.figure(figsize=(12, 8))
plot_tree(
    clf, filled=True, feature_names=X.columns
)  # Adjust if necessary for visualization
plt.show()
