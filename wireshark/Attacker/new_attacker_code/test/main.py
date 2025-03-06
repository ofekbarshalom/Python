import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import os


# Function to calculate Time_Diff and merge all tagged traffic CSV files
def merge_csv_files():
    csv_files = [
        "Firefox_tagged.csv",
        "Google_tagged.csv",
        "Spotify_tagged.csv",
        "YouTube_tagged.csv",
        "Zoom_tagged.csv"
    ]

    # Merge all CSVs into one DataFrame
    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)

        # Convert Time column to numeric and compute Time_Diff
        df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
        df['Time_Diff'] = df['Time'].diff().fillna(0).clip(lower=0)  # Ensure no negative values

        # Append to list of DataFrames
        dataframes.append(df)

    # Concatenate all DataFrames
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Save merged DataFrame
    merged_df.to_csv("merged_cleaned_data.csv", index=False)
    print("Merged dataset saved as merged_cleaned_data.csv")


# Merge the CSV files before proceeding with model training
merge_csv_files()

# Load the cleaned dataset
data = pd.read_csv("merged_cleaned_data.csv")

# Display the first few rows of the dataset
print("First 5 rows of merged dataset:\n", data.head())
print("\nColumns in merged dataset:", data.columns)

# Encode categorical features (Protocol, Source, Destination)
le_protocol = LabelEncoder()
if 'Protocol' in data.columns:
    data['Protocol'] = le_protocol.fit_transform(data['Protocol'])

le_source = LabelEncoder()
le_dest = LabelEncoder()
if 'Source' in data.columns and 'Destination' in data.columns:
    data['Source'] = le_source.fit_transform(data['Source'])
    data['Destination'] = le_dest.fit_transform(data['Destination'])

# Check the first few rows after encoding
print("\nFirst 5 rows after encoding:\n", data.head())

# Define feature sets and target
features_full = ["Source", "Destination", "Protocol", "Length", "Time_Diff"]  # Scenario 1
features_limited = ["Length", "Time_Diff"]  # Scenario 2
target = "App"

# Check if all required columns are present
for feature in features_full:
    if feature not in data.columns:
        raise ValueError(f"Feature '{feature}' not found in the dataset.")

# Split dataset into 80% training, 20% testing
X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(
    data[features_full], data[target], test_size=0.2, random_state=42
)

X_train_limited, X_test_limited, y_train_limited, y_test_limited = train_test_split(
    data[features_limited], data[target], test_size=0.2, random_state=42
)

# Train models
rf_model_full = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_full.fit(X_train_full, y_train_full)

rf_model_limited = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_limited.fit(X_train_limited, y_train_limited)

# Make predictions
y_pred_scenario_1 = rf_model_full.predict(X_test_full)
y_pred_scenario_2 = rf_model_limited.predict(X_test_limited)

# Compute accuracy
accuracy_scenario_1 = accuracy_score(y_test_full, y_pred_scenario_1) * 100
accuracy_scenario_2 = accuracy_score(y_test_limited, y_pred_scenario_2) * 100

# Generate classification reports
classification_report_scenario_1 = classification_report(y_test_full, y_pred_scenario_1)
classification_report_scenario_2 = classification_report(y_test_limited, y_pred_scenario_2)

# Save results
test_results_df = X_test_full.copy()
test_results_df["Actual_App"] = y_test_full
test_results_df["Predicted_App_Scenario_1"] = y_pred_scenario_1
test_results_df["Predicted_App_Scenario_2"] = y_pred_scenario_2

test_results_df.to_csv("test_results_with_predictions.csv", index=False)

print("Scenario 1 Accuracy:", accuracy_scenario_1)
print("Scenario 2 Accuracy:", accuracy_scenario_2)
print("\nClassification Report for Scenario 1:\n", classification_report_scenario_1)
print("\nClassification Report for Scenario 2:\n", classification_report_scenario_2)

# Create Actual vs Predicted table in the required format
def generate_actual_vs_predicted_table(actual, predicted, scenario):
    actual_counts = actual.value_counts().sort_index()
    predicted_counts = pd.Series(predicted).value_counts().sort_index()

    table_data = {
        "Application": actual_counts.index,
        "Actual": [f"{(actual_counts[app] / len(actual)) * 100:.0f}%" if app in actual_counts else "0%"
                   for app in actual_counts.index],
        "Predicted": [f"{(predicted_counts[app] / len(predicted)) * 100:.0f}%" if app in predicted_counts else "0%"
                      for app in actual_counts.index]
    }

    table_df = pd.DataFrame(table_data)
    print(f"\nActual vs Predicted Table for Scenario {scenario}:\n")
    print(table_df.to_string(index=False))


# Display the actual vs predicted tables
generate_actual_vs_predicted_table(y_test_full, y_pred_scenario_1, 1)
generate_actual_vs_predicted_table(y_test_limited, y_pred_scenario_2, 2)

#################### Scenario 1: Actual vs. Predicted Application Counts (With Source/Destination) ####################
app_order = ['Zoom', 'YouTube', 'Firefox', 'Google', 'Spotify']

actual_counts = test_results_df["Actual_App"].value_counts().reindex(app_order, fill_value=0)
predicted_counts = test_results_df["Predicted_App_Scenario_1"].value_counts().reindex(app_order, fill_value=0)

x = np.arange(len(app_order))
width = 0.4

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width / 2, actual_counts, width, label="Actual", color='blue')
ax.bar(x + width / 2, predicted_counts, width, label="Predicted", color='orange')

ax.set_xlabel("Applications")
ax.set_ylabel("Count")
ax.set_title("Scenario 1: Actual vs Predicted Application Counts (With Source/Destination)")
ax.set_xticks(x)
ax.set_xticklabels(app_order, rotation=45, ha="right")
ax.legend()

ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("1.png")
plt.show()

# Scenario 2: Actual vs. Predicted Application Counts (Without Source/Destination)
actual_counts = test_results_df["Actual_App"].value_counts().reindex(app_order, fill_value=0)
predicted_counts = test_results_df["Predicted_App_Scenario_2"].value_counts().reindex(app_order, fill_value=0)

fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(x - width / 2, actual_counts, width, label="Actual", color='red')
ax.bar(x + width / 2, predicted_counts, width, label="Predicted", color='green')

ax.set_xlabel("Applications")
ax.set_ylabel("Count")
ax.set_title("Scenario 2: Actual vs Predicted Application Counts (Without Source/Destination)")
ax.set_xticks(x)
ax.set_xticklabels(app_order, rotation=45, ha="right")
ax.legend()

ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("2.png")
plt.show()
