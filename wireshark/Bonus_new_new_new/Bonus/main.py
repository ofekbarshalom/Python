import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re

# Function to merge only the normal traffic data for training
def merge_csv_files():
    normal_files = [
        "Firefox_traffic.csv",
        "Google_traffic.csv",
        "Youtube_traffic.csv",
        "Zoom_traffic.csv"
    ]

    mixed_files = [
        "Firefox_with_Spotify.csv",
        "Google_with_Spotify.csv",
        "Youtube_with_Spotify.csv",
        "Zoom_with_Spotify.csv"
    ]

    def load_and_process(files, is_mixed):
        dataframes = []
        for file in files:
            df = pd.read_csv(file)

            # Assign App name based on filename
            app_name = file.split("_")[0]  # Extract "Firefox", "Google", etc.
            df["App"] = app_name
            df["Mixed_Traffic"] = is_mixed  # Mark mixed data

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

            dataframes.append(df)

        return pd.concat(dataframes, ignore_index=True)

    # Load normal traffic for training
    normal_data = load_and_process(normal_files, is_mixed=False)
    normal_data.to_csv("normal_cleaned_data.csv", index=False)
    print("Training dataset saved as normal_cleaned_data.csv")

    # Load mixed traffic for testing
    mixed_data = load_and_process(mixed_files, is_mixed=True)
    mixed_data.to_csv("mixed_cleaned_data.csv", index=False)
    print("Testing dataset saved as mixed_cleaned_data.csv")

    return normal_data, mixed_data


# Merge the CSV files before proceeding with model training
normal_data, mixed_data = merge_csv_files()

# Define feature sets
features_full = ["Flow_ID", "Length", "Time"]
features_limited = ["Length", "Time"]
target = "App"

# Training data (normal traffic only)
X_train_full = normal_data[features_full]
X_train_limited = normal_data[features_limited]
y_train = normal_data[target]

# Testing data (mixed traffic only)
X_test_full = mixed_data[features_full]
X_test_limited = mixed_data[features_limited]
y_test = mixed_data[target]

# Train models
rf_model_full = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
rf_model_full.fit(X_train_full, y_train)

rf_model_limited = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
rf_model_limited.fit(X_train_limited, y_train)

# Make predictions
y_pred_scenario_1 = rf_model_full.predict(X_test_full)
y_pred_scenario_2 = rf_model_limited.predict(X_test_limited)

# Compute accuracy
accuracy_scenario_1 = accuracy_score(y_test, y_pred_scenario_1) * 100
accuracy_scenario_2 = accuracy_score(y_test, y_pred_scenario_2) * 100

# Generate classification reports
classification_report_scenario_1 = classification_report(y_test, y_pred_scenario_1)
classification_report_scenario_2 = classification_report(y_test, y_pred_scenario_2)

# Save results
test_results_df = X_test_full.copy()
test_results_df["Actual_App"] = y_test
test_results_df["Predicted_App_Scenario_1"] = y_pred_scenario_1
test_results_df["Predicted_App_Scenario_2"] = y_pred_scenario_2

test_results_df.to_csv("test_results_with_predictions.csv", index=False)

print("Scenario 1 Accuracy:", accuracy_scenario_1)
print("Scenario 2 Accuracy:", accuracy_scenario_2)
print("\nClassification Report for Scenario 1:\n", classification_report_scenario_1)
print("\nClassification Report for Scenario 2:\n", classification_report_scenario_2)

# Function to visualize actual vs predicted results
def plot_results(actual, predicted, scenario, filename):
    app_order = sorted(actual.unique())  # Dynamically get unique app names
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
plot_results(y_test, y_pred_scenario_1, 1, "Actual_vs_Predicted_Scenario_1.png")
plot_results(y_test, y_pred_scenario_2, 2, "Actual_vs_Predicted_Scenario_2.png")
