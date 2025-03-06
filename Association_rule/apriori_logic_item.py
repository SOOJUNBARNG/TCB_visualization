# itemsets: The unique combinations of items (sets of items) that were found to be frequent in the transactions.
# support: The proportion of transactions that contain the itemset. It indicates how frequently the itemset appears in the dataset. For example, a support of 0.2 means that the itemset appears in 20% of the transactions.
# confidence (if generated via association_rules): This measures the likelihood of occurrence of an item in a transaction, given that another item (or itemset) is present. It’s calculated as the support of the itemset divided by the support of the antecedent.
# lift (if generated via association_rules): This is the ratio of the observed support of an itemset to the expected support if the items were independent. A lift greater than 1 indicates that the items are positively correlated; a lift less than 1 indicates a negative correlation.
# leverage (if generated via association_rules): This measures the difference between the observed frequency of itemsets and the expected frequency if the items were independent.
# conviction (if generated via association_rules): This measures how much more likely the consequent is to occur when the antecedent occurs compared to when it does not. A conviction greater than 1 indicates a positive association.


import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Load CSV file into DataFrame
csv_file_path = r"C:\Users\powwe\Documents\MF_data_analysis_divison\External\result.csv"
transactions_df = pd.read_csv(csv_file_path)

# Group by Transaction ID and collect items into a list
# ここでニーズと商品で分けて調達が可能となる
grouped_df = (
    transactions_df.groupby("id")["tcb_treatment_detail_name"]
    .apply(list)
    .reset_index(name="tcb_item_name")
)  # tcb_treatment_detail_name # tcb_item_name

# Convert transactions into a format suitable for the Apriori algorithm
basket = grouped_df["tcb_item_name"].str.join(sep=",").str.get_dummies(sep=",")

# Apriori algorithm execution
frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)

# Generate association rules
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=0.1)

# Convert support to integer percentage
column_list = [
    "antecedent support",
    "consequent support",
    "support",
    "confidence",
    "lift",
    "leverage",
    "conviction",
    "zhangs_metric",
]
for column in column_list:

    rules[column] = (rules[column] * 100).astype(int)

# Remove frozenset and convert to string
rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(list(x)))
rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(list(x)))

# Save results to CSV
rules.to_csv("apriori_logic_item.csv", index=False)
