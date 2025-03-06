# NYAN
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score

# Optionally, visualize the tree (requires matplotlib)
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt


# Index(['sales_id', 'sales_item_id', 'discount_id', 'discount_rate', 'service',
#        'net_value', 'tcb_item_code', 'tcb_item_name', 'agreement_form_code',
#        'doctor_form', 'treatment_form', 'category',
#        'tcb_treatment_detail_name', 'set_unit', 'te_code', 'te_kind',
#        'tcb_patient_id', 'staff_code', 'staff_name', 'first_visit_date', 'id',
#        'code', 'last_name', 'first_name', 'full_name', 'middle_name',
#        'last_name_kana', 'first_name_kana', 'full_name_kana',
#        'middle_name_kana', 'sex', 'born_on', 'nationality', 'zip_code',
#        'prefecture_code', 'address', 'mobile', 'phone_number', 'email',
#        'created_at', 'update_at', 'clinic_name'

# Load CSV file into DataFrame
csv_file_path = r"C:\Users\powwe\Documents\MF_data_analysis_divison\External\result.csv"
transactions_df = pd.read_csv(csv_file_path)

# print(transactions_df.columns)
# Prepare data (assume 'target_column' is your target variable)
# You may need to adjust this based on your actual dataset
X = transactions_df.drop(columns=["net_value"])  # Features
# y = transactions_df['net_value']  # Target variable
# basic_info = transactions_df['net_value'].describe()


# Define the number of bins
num_bins = 4

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
y = transactions_df["net_value_binned"]


# Specify columns to be one-hot encoded
columns_to_encode = [
    "discount_rate",
    "service",
    "tcb_item_name",
    "sex",
    "prefecture_code",
    "set_unit",
    "clinic_name",
    "te_kind",
    "agreement_form_code",
    "doctor_form",
    "treatment_form",
    "category",
]  # ,'staff_name']  # Replace with your actual column names

# Create dummy variables only for the specified columns
X_encoded = pd.get_dummies(X[columns_to_encode], drop_first=True)

# # Select only numeric columns from the original DataFrame
# numeric_columns = X.drop(columns=columns_to_encode).select_dtypes(include=['int', 'float'])

# # Combine with the rest of the DataFrame
# X = pd.concat([numeric_columns, X_encoded], axis=1)
# X.head(20).to_csv("mid_result.csv")
# print(X)

X = X_encoded

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create a Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)

print("done_create_decision_tree")

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("done_predict")

# plt.figure(figsize=(12, 8))
# plot_tree(clf, filled=True, feature_names=X.columns, class_names=['Class1', 'Class2'])
# plt.show()
