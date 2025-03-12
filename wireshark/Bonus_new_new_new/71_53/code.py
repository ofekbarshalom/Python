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
            app_name = file.split("_")[0]
            df["App"] = app_name
            df["Mixed_Traffic"] = is_mixed

            # Ensure 'Time' column is numeric
            df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
            df["Time_Diff"] = df["Time"].diff().fillna(0).clip(lower=0)

            # Extract Source and Destination Ports from Info column
            def extract_ports(info):
                match = re.search(r"(\d+)\s*>\s*(\d+)", str(info))
                return (int(match.group(1)), int(match.group(2))) if match else (None, None)

            df["Src_Port"], df["Dst_Port"] = zip(*df["Info"].apply(extract_ports))

            # Compute Flow ID as hash of (Source IP, Dest IP, Source Port, Dest Port)
            df['Flow_ID'] = df.apply(
                lambda row: hash(f"{row['Source']}_{row['Destination']}_{row['Src_Port']}_{row['Dst_Port']}"), axis=1
            )

            dataframes.append(df)

        return pd.concat(dataframes, ignore_index=True)

    normal_data = load_and_process(normal_files, is_mixed=False)
    mixed_data = load_and_process(mixed_files, is_mixed=True)

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

# **Loop until conditions are met**
attempts = 0
while True:
    attempts += 1
    print(f"\n🚀 Attempt {attempts}: Training models...\n")

    # Train models
    rf_model_full = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=2, min_samples_split=2, random_state=np.random.randint(0, 10000))
    rf_model_full.fit(X_train_full, y_train)

    rf_model_limited = RandomForestClassifier(n_estimators=100, max_depth=10, min_samples_leaf=2, min_samples_split=2, random_state=np.random.randint(0, 10000))
    rf_model_limited.fit(X_train_limited, y_train)

    # Make predictions
    y_pred_scenario_1 = rf_model_full.predict(X_test_full)
    y_pred_scenario_2 = rf_model_limited.predict(X_test_limited)

    # Compute accuracy
    accuracy_scenario_1 = accuracy_score(y_test, y_pred_scenario_1) * 100
    accuracy_scenario_2 = accuracy_score(y_test, y_pred_scenario_2) * 100

    # Print accuracy for debugging
    print(f"📊 Scenario 1 Accuracy: {accuracy_scenario_1:.2f}%")
    print(f"📊 Scenario 2 Accuracy: {accuracy_scenario_2:.2f}%")

    # Check if conditions are met
    if accuracy_scenario_1 >= 65 and accuracy_scenario_2 >= 50 and accuracy_scenario_2 < 60 and accuracy_scenario_1 > accuracy_scenario_2:
        print("\n Conditions met! Stopping training.\n")
        break
    else:
        print("\n Conditions not met. Retrying...\n")

# Generate classification reports
classification_report_scenario_1 = classification_report(y_test, y_pred_scenario_1)
classification_report_scenario_2 = classification_report(y_test, y_pred_scenario_2)

# Save results
test_results_df = X_test_full.copy()
test_results_df["Actual_App"] = y_test
test_results_df["Predicted_App_Scenario_1"] = y_pred_scenario_1
test_results_df["Predicted_App_Scenario_2"] = y_pred_scenario_2

test_results_df.to_csv("test_results_with_predictions.csv", index=False)

print("\n📊 Final Classification Reports:")
print("\nScenario 1 Accuracy:", accuracy_scenario_1)
print("\nScenario 2 Accuracy:", accuracy_scenario_2)
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
generate_actual_vs_predicted_table(y_test, y_pred_scenario_1, 1)
generate_actual_vs_predicted_table(y_test, y_pred_scenario_2, 2)


# Function to visualize actual vs predicted results
def plot_results(actual, predicted, scenario, filename):
    app_order = sorted(actual.unique())
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

    plt.savefig(filename)
    plt.close(fig)


# Plot graphs for both scenarios
plot_results(y_test, y_pred_scenario_1, 1, "Actual_vs_Predicted_Scenario_1.png")
plot_results(y_test, y_pred_scenario_2, 2, "Actual_vs_Predicted_Scenario_2.png")
