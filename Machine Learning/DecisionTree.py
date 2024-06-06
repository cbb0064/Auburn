# Train a decision tree classifier using the data file. You CAN NOT use
# any decision tree library functions to do it, i.e., you must construct the tree from
# scratch. You also CAN NOT touch the test file in this part. Vary the cut-off
# depth from 2 to 10 and report the training accuracy for each cut-off depth k.
# Based on your results, select an optimal k.

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define a class to represent a single decision node
class DecisionNode:
    def __init__(self, feature=None, value=None, left=None, right=None, result=None):
        self.feature = feature
        self.value = value
        self.left = left
        self.right = right
        self.result = result

# Define a function to compute the gini impurity of a dataset
def compute_gini_impurity(data):
    classes, counts = np.unique(data['income'], return_counts=True)
    num_instances = len(data)
    p = counts / num_instances
    gini = 1 - np.sum(p ** 2)
    return gini

# Define a function to compute the entropy of a dataset
def compute_entropy(data):
    classes, counts = np.unique(data['income'], return_counts=True)
    num_instances = len(data)
    p = counts / num_instances
    entropy = -np.sum(p * np.log2(p))
    return entropy

# Define a function to compute the information gain of a split
def compute_information_gain(data, feature, value):
    data_value = data[data[feature] == value]
    data_not_value = data[data[feature] != value]
    entropy_data = compute_entropy(data)
    weighted_entropy = (len(data_value) / len(data) * compute_entropy(data_value) +
                        len(data_not_value) / len(data) * compute_entropy(data_not_value))
    information_gain = entropy_data - weighted_entropy
    return information_gain

# Define a function to split a dataset on a feature and a value
def split_data(data, feature, value):
    mask = data[feature] == value
    data_value = data[mask]
    data_not_value = data[~mask]
    return data_value, data_not_value

# Define a function to build the decision tree
def build_tree(data, criterion='gini', max_depth=None, current_depth=0):
    if len(data['income'].unique()) == 1:
        return DecisionNode(result=data['income'].iloc[0])

    if max_depth is not None and current_depth >= max_depth:
        return DecisionNode(result=data['income'].mode()[0])

    best_gain = 0
    best_feature = None
    best_value = None
    for feature in data.columns:
        if feature == 'income':
            continue
        for value in data[feature].unique():
            data_value, data_not_value = split_data(data, feature, value)
            if criterion == 'gini':
                gini_value = compute_gini_impurity(data_value)
                gini_not_value = compute_gini_impurity(data_not_value)
                gain = (compute_gini_impurity(data) - (len(data_value) / len(data) * gini_value +
                        len(data_not_value) / len(data) * gini_not_value))
            else:
                gain = compute_information_gain(data, feature, value)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_value = value

    if best_gain == 0:
        return DecisionNode(result=data['income'].mode()[0])

    left_data, right_data = split_data(data, best_feature, best_value)
    left = build_tree(left_data, criterion, max_depth, current_depth + 1)
    right = build_tree(right_data, criterion, max_depth, current_depth + 1)

    return DecisionNode(feature=best_feature, value=best_value, left=left, right=right)

# Make predictions for a single instance
def predict(tree, instance):
    if tree.result is not None:
        return tree.result
    if instance[tree.feature] == tree.value:
        return predict(tree.left, instance)
    else:
        return predict(tree.right, instance)

# Compute Accuracy
def compute_accuracy(tree, X, y):
    predictions = [predict(tree, instance) for _, instance in X.iterrows()]
    return np.mean(predictions == y)

# Step 1: Load the data
column_names = ["age", "class_of_worker", "detailed_industry_recode", "detailed_occupation_recode",
                "education", "wage_per_hour", "enroll_in_edu_inst_last_week", "marital_status",
                "major_industry_code", "major_occupation_code", "race", "hispanic_origin", "sex",
                "member_of_a_labor_union", "reason_for_unemployment", "full_or_part_time_employment_stat",
                "capital_gains", "capital_losses", "dividends_from_stocks", "tax_filer_stat",
                "region_of_previous_residence", "state_of_previous_residence",
                "detailed_household_and_family_stat", "detailed_household_summary_in_household",
                "instance_weight", "migration_code_change_in_MSA", "migration_code_change_in_reg",
                "migration_code_move_within_reg", "live_in_this_house_one_year_ago", "migration_prev_res_in_sunbelt",
                "num_persons_worked_for_the_employer", "family_members_under_18", "country_of_birth_father",
                "country_of_birth_mother", "country_of_birth_self", "citizenship",
                "own_business_or_self_employed", "fill_inc_questionnaire_for_veteran_admin", "veterans_benefits",
                "weeks_worked_in_year", "year", "income"]

data = pd.read_csv('census-income.data', header=None, names=column_names)

# Step 2: Preprocess the data
# Preprocess categorical columns using LabelEncoder
categorical_columns = data.select_dtypes(include=['object']).columns
data[categorical_columns] = data[categorical_columns].apply(LabelEncoder().fit_transform)

# Bin continuous variables
data['age'] = pd.cut(data['age'], bins=4, labels=False)
data['wage_per_hour'] = pd.cut(data['wage_per_hour'], bins=4, labels=False)
data['capital_gains'] = pd.cut(data['capital_gains'], bins=4, labels=False)
data['capital_losses'] = pd.cut(data['capital_losses'], bins=4, labels=False)
data['dividends_from_stocks'] = pd.cut(data['dividends_from_stocks'], bins=4, labels=False)
data['num_persons_worked_for_the_employer'] = pd.cut(data['num_persons_worked_for_the_employer'], bins=4, labels=False)
data['weeks_worked_in_year'] = pd.cut(data['weeks_worked_in_year'], bins=4, labels=False)
data['instance_weight'] = pd.cut(data['instance_weight'], bins=4, labels=False)

# Split the data
X = data.drop('income', axis=1)
y = data['income']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the trees, compute the training accuracies and select the optimal depth
best_accuracy = 0
best_depth = None
for max_depth in range(2, 11):
    tree = build_tree(pd.concat([X_train, y_train], axis=1), max_depth=max_depth)
    accuracy = compute_accuracy(tree, X_train, y_train)
    print(f"Depth: {max_depth}, Training Accuracy: {accuracy:.4f}")
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_depth = max_depth

print(f"Optimal Depth: {best_depth}")

# Load the test data
test_data = pd.read_csv('census-income.test', header=None, names=column_names)

# Preprocess the test data
test_data[categorical_columns] = test_data[categorical_columns].apply(LabelEncoder().fit_transform)
test_data['age'] = pd.cut(test_data['age'], bins=4, labels=False)
test_data['wage_per_hour'] = pd.cut(test_data['wage_per_hour'], bins=4, labels=False)
test_data['capital_gains'] = pd.cut(test_data['capital_gains'], bins=4, labels=False)
test_data['capital_losses'] = pd.cut(test_data['capital_losses'], bins=4, labels=False)
test_data['dividends_from_stocks'] = pd.cut(test_data['dividends_from_stocks'], bins=4, labels=False)
test_data['num_persons_worked_for_the_employer'] = pd.cut(test_data['num_persons_worked_for_the_employer'], bins=4, labels=False)
test_data['weeks_worked_in_year'] = pd.cut(test_data['weeks_worked_in_year'], bins=4, labels=False)
test_data['instance_weight'] = pd.cut(test_data['instance_weight'], bins=4, labels=False)

X_test = test_data.drop('income', axis=1)
y_test = test_data['income']

# Build the tree with the optimal cut-off depth
optimal_tree = build_tree(pd.concat([X_train, y_train], axis=1), max_depth=best_depth)

# Compute the test accuracy
test_accuracy = compute_accuracy(optimal_tree, X_test, y_test)
print(f"Testing Accuracy: {test_accuracy:.4f}")

