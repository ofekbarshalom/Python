import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler
import matplotlib


# Function to load and merge single-app datasets (for training)
def load_regular_datasets():
    csv_files = [
        "Labeled_Attacker_firefox_traffic.csv",
        "Labeled_Attacker_google_traffic.csv",
        "Labeled_Attacker_spotify_traffic.csv",
        "Labeled_Attacker_Youtube_traffic.csv",
        "Labeled_Attacker_zoom_traffic.csv"
    ]

    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)

        # Convert time column to numeric and compute Time_Diff
        df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
        df['Time_Diff'] = df['Time'].diff().fillna(0).clip(lower=0)

        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    return merged_df


# Load the regular datasets for training
data = load_regular_datasets()

# Encode categorical 'Protocol' column
if 'Protocol' in data.columns:
    le = LabelEncoder()
    data['Protocol'] = le.fit_transform(data['Protocol'])

# Debug: Show known protocols from training
print("Known Protocols in Training:", list(le.classes_))

# Define feature sets and target (REMOVE PROTOCOL TO AVOID ISSUES)
features_full = ["Length", "Time_Diff"]  # Removed 'Protocol' due to encoding errors
features_limited = ["Length", "Time_Diff"]
target = "App"

# Add 20% of mixed traffic into training to improve generalization
train_data, extra_train_data = train_test_split(data, test_size=0.2, random_state=42)
mixed_train_data = pd.concat([train_data, extra_train_data.sample(frac=0.2, random_state=42)])

# Split dataset into 80% training, 20% validation (on regular + mixed traffic)
X_train_full, X_val_full, y_train_full, y_val_full = train_test_split(
    mixed_train_data[features_full], mixed_train_data[target], test_size=0.2, random_state=42
)

X_train_limited, X_val_limited, y_train_limited, y_val_limited = train_test_split(
    mixed_train_data[features_limited], mixed_train_data[target], test_size=0.2, random_state=42
)

# Balance the training data to avoid bias
ros = RandomOverSampler(random_state=42)
X_train_full_balanced, y_train_full_balanced = ros.fit_resample(X_train_full, y_train_full)
X_train_limited_balanced, y_train_limited_balanced = ros.fit_resample(X_train_limited, y_train_limited)

# Train models
rf_model_full = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_full.fit(X_train_full_balanced, y_train_full_balanced)

rf_model_limited = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model_limited.fit(X_train_limited_balanced, y_train_limited_balanced)

# Testing on Mixed Datasets
mixed_files = [
    "Balanced_Mixed_Firefox_with_Spotify.csv",
    "Balanced_Mixed_Google_with_Spotify.csv",
    "Balanced_Mixed_Youtube_with_Spotify.csv",
    "Balanced_Mixed_Zoom_with_Spotify.csv"
]

test_results_list = []

for mixed_file in mixed_files:
    print(f"\nTesting on: {mixed_file}")

    # Load the mixed dataset
    mixed_data = pd.read_csv(mixed_file)

    # Calculate Time_Diff for mixed traffic
    mixed_data['Time'] = pd.to_numeric(mixed_data['Time'], errors='coerce')
    mixed_data['Time_Diff'] = mixed_data['Time'].diff().fillna(0).clip(lower=0)

    # Ensure dataset is not empty before proceeding
    if mixed_data.empty:
        print(f"⚠ Skipping {mixed_file} (No valid data)")
        continue

    # Split features and target
    X_test_full = mixed_data[features_full]
    y_test_full = mixed_data[target]

    X_test_limited = mixed_data[features_limited]
    y_test_limited = mixed_data[target]

    # Make predictions
    y_pred_scenario_1 = rf_model_full.predict(X_test_full)
    y_pred_scenario_2 = rf_model_limited.predict(X_test_limited)

    # Compute accuracy
    accuracy_scenario_1 = accuracy_score(y_test_full, y_pred_scenario_1) * 100
    accuracy_scenario_2 = accuracy_score(y_test_limited, y_pred_scenario_2) * 100

    print(f"Scenario 1 Accuracy on {mixed_file}: {accuracy_scenario_1:.2f}%")
    print(f"Scenario 2 Accuracy on {mixed_file}: {accuracy_scenario_2:.2f}%")

    # Generate classification reports safely
    report_scenario_1 = classification_report(y_test_full, y_pred_scenario_1, zero_division=1)
    report_scenario_2 = classification_report(y_test_limited, y_pred_scenario_2, zero_division=1)

    print(f"\nScenario 1 Classification Report on {mixed_file}:\n", report_scenario_1)
    print(f"\nScenario 2 Classification Report on {mixed_file}:\n", report_scenario_2)

    # Save results
    test_results_df = X_test_full.copy()
    test_results_df["Actual_App"] = y_test_full
    test_results_df["Predicted_App_Scenario_1"] = y_pred_scenario_1
    test_results_df["Predicted_App_Scenario_2"] = y_pred_scenario_2

    test_results_list.append((mixed_file, test_results_df))

# Visualizing Results
app_order = ['Zoom', 'YouTube', 'Firefox', 'Google', 'Spotify']

for mixed_file, test_results_df in test_results_list:
    print(f"\nGenerating graph for: {mixed_file}")

    if not test_results_df.empty:
        x = np.arange(len(app_order))  # Numeric positions for bars
        width = 0.35  # Adjust bar width for proper spacing

        actual_counts = test_results_df["Actual_App"].value_counts().reindex(app_order, fill_value=0)
        predicted_counts = test_results_df["Predicted_App_Scenario_1"].value_counts().reindex(app_order, fill_value=0)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(x - width/2, actual_counts, width, label="Actual", color="blue")
        ax.bar(x + width/2, predicted_counts, width, label="Predicted", color="orange")

        ax.set_xlabel("Applications")
        ax.set_ylabel("Count")
        ax.set_title(f"Actual vs Predicted Counts ({mixed_file})")
        ax.set_xticks(x)
        ax.set_xticklabels(app_order, rotation=45, ha="right")
        ax.legend()

        filename = f"Actual_vs_Predicted_{mixed_file.replace('.csv', '.png')}"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        print(f" Saved: {filename}")

        plt.show()
    else:
        print(f" No valid predictions for {mixed_file}, skipping graph.")

# Final Debug Prints
print("\n Model Finished Successfully! If there are still issues, check protocol mapping.")
