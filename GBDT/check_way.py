import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer

# ropping NaNs might reduce the data size, which could affect model performance.
# Imputing NaNs is generally preferred when you want to retain all data points.
# HistGradientBoostingClassifier is a specialized version of Gradient Boosting that can handle NaNs without preprocessing.

# Load CSV file into DataFrame
csv_file_path = r"C:\Users\powwe\Documents\MF_data_analysis_divison\External\result.csv"
transactions_df = pd.read_csv(csv_file_path)

# Prepare data (assume 'target_column' is your target variable)
X = transactions_df.drop(columns=["net_value"])  # Features

# Define the number of bins
num_bins = 10

# Define quantiles for 4 bins
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
]

# Create dummy variables only for the specified columns
X_encoded = pd.get_dummies(X[columns_to_encode], drop_first=True)

# Use only the encoded features
X = X_encoded

X.to_csv("mid.csv")

# GradientBoostingClassifier does not accept missing values encoded as NaN natively. For supervised learning, you might want to consider sklearn.ensemble.HistGradientBoostingClassifier and Regressor which accept missing values encoded as NaNs natively. Alternatively, it is possible to preprocess the data, for instance by using an imputer transformer in a pipeline or drop samples with missing values. See https://scikit-learn.org/stable/modules/impute.html You can find a list of all estimators that handle NaN values at the following page: https://scikit-learn.org/stable/modules/impute.html#estimators-that-handle-nan-values
# Drop rows with NaN values
X = X.dropna()
y = y.loc[X.index]  # Ensure the target variable matches the filtered rows


# # Create an imputer object with a strategy (mean, median, or mode)
# imputer = SimpleImputer(strategy='mean')

# # Fit the imputer on the dataset and transform the data
# X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create a Gradient Boosting Classifier
clf = GradientBoostingClassifier(random_state=42)
# clf = HistGradientBoostingClassifier(random_state=42)

print("done_create_gradient_boosting")

# Train the model
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

print("done_predict")
