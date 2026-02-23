import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import re


# Function to calculate Time_Diff and merge all tagged traffic CSV files
def merge_csv_files():
    csv_files = [
        "Firefox_traffic.csv",
        "Google_traffic.csv",
        "Spotify_traffic.csv",
        "Youtube_traffic.csv",
        "Zoom_traffic.csv"
    ]

    # Merge all CSVs into one DataFrame
    dataframes = []
    for file in csv_files:
        # Load the CSV file
        df = pd.read_csv(file)

        # Assign App name based on filename
        app_name = file.split("_")[0]  # Extract "Firefox", "Google", etc.
        df["App"] = app_name

        # Ensure 'Time' column is numeric
        df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
        df["Time_Diff"] = df["Time"].diff().fillna(0).clip(lower=0)

        # Extract Source and Destination Ports from Info column
        def extract_ports(info):
            match = re.search(r"(\d+)\s*>\s*(\d+)", str(info))  # Extract "38886  >  443"
            if match:
                return int(match.group(1)), int(match.group(2))  # (Src_Port, Dst_Port)
            return None, None  # Return None if no match

        df["Src_Port"], df["Dst_Port"] = zip(*df["Info"].apply(extract_ports))

        # Compute Flow ID as hash of (Source IP, Dest IP, Source Port, Dest Port)
        df['Flow_ID'] = df.apply(
            lambda row: hash(f"{row['Source']}_{row['Destination']}_{row['Src_Port']}_{row['Dst_Port']}"), axis=1
        )

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

# Define feature sets and target
features_full = ["Flow_ID", "Length", "Time"]
features_limited = ["Length", "Time"]
target = "App"

# Split dataset into 80% training, 20% testing
X_train_full, X_test_full, y_train_full, y_test_full = train_test_split(
    data[features_full], data[target], test_size=0.2, random_state=42
)

X_train_limited, X_test_limited, y_train_limited, y_test_limited = train_test_split(
    data[features_limited], data[target], test_size=0.2, random_state=42
)

# Train models
rf_model_full = RandomForestClassifier(n_estimators=50,max_depth=6, random_state=42)
rf_model_full.fit(X_train_full, y_train_full)

rf_model_limited = RandomForestClassifier(n_estimators=50,max_depth=6, random_state=42)
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

# Function to format actual vs predicted table
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

# Visualizing Results
app_order = sorted(test_results_df["Actual_App"].unique())  # Dynamically get unique app names


def plot_results(actual, predicted, scenario, filename):
    actual_counts = actual.value_counts().reindex(app_order, fill_value=0)
    predicted_counts = pd.Series(predicted).value_counts().reindex(app_order, fill_value=0)

    x = np.arange(len(app_order))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(x - width / 2, actual_counts, width, label="Actual", color='blue')
    ax.bar(x + width / 2, predicted_counts, width, label=f"Predicted (Scenario {scenario})",
           color='orange' if scenario == 1 else 'green')

    ax.set_xlabel("Applications")
    ax.set_ylabel("Count")
    ax.set_title(f"Actual vs Predicted Counts (Scenario {scenario})")
    ax.set_xticks(x)
    ax.set_xticklabels(app_order, rotation=45, ha="right")
    ax.legend()

    plt.savefig(filename)  # Save as PNG
    plt.show()


# Plot graphs for both scenarios
plot_results(y_test_full, y_pred_scenario_1, 1, "Actual_vs_Predicted_Scenario_1.png")
plot_results(y_test_limited, y_pred_scenario_2, 2, "Actual_vs_Predicted_Scenario_2.png")
