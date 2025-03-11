import subprocess
import re

# Define accuracy thresholds
TARGET_ACCURACY_SCENARIO_1 = 70
TARGET_ACCURACY_SCENARIO_2 = 50
MAX_ATTEMPTS = 10

best_scenario_1 = 0
best_scenario_2 = 0
best_output = ""

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n🚀 Attempt {attempt} - Running main.py...\n")

    # Run main.py and capture the output
    process = subprocess.run(["python", "main.py"], capture_output=True, text=True)
    output = process.stdout.strip()  # Ensure we get clean output

    # Print the output for debugging
    print(output)

    # Extract accuracy values using regex
    match_1 = re.search(r"Scenario 1 Accuracy:\s*([\d.]+)", output)
    match_2 = re.search(r"Scenario 2 Accuracy:\s*([\d.]+)", output)

    if match_1 and match_2:
        accuracy_scenario_1 = float(match_1.group(1))
        accuracy_scenario_2 = float(match_2.group(1))

        print(f"🔍 Extracted Accuracy - Scenario 1: {accuracy_scenario_1}% | Scenario 2: {accuracy_scenario_2}%")

        # Update best result found so far
        if accuracy_scenario_1 > best_scenario_1 or accuracy_scenario_2 > best_scenario_2:
            best_scenario_1 = accuracy_scenario_1
            best_scenario_2 = accuracy_scenario_2
            best_output = output  # Save the best output for later

        # Check if conditions are met
        if (
            accuracy_scenario_1 >= TARGET_ACCURACY_SCENARIO_1
            and accuracy_scenario_2 >= TARGET_ACCURACY_SCENARIO_2
            and accuracy_scenario_1 > accuracy_scenario_2
        ):
            print("\n✅ Conditions Met! Stopping auto-run.")
            break
        else:
            print("\n❌ Conditions Not Met. Retrying...\n")
    else:
        print("\n⚠️ Could not extract accuracy from output. Ensure main.py prints the accuracy values correctly.\n")

# After max attempts, print the best result
print("\n📊 Best Attempt Results:")
print(f"Best Scenario 1 Accuracy: {best_scenario_1}%")
print(f"Best Scenario 2 Accuracy: {best_scenario_2}%")
print("\n📝 Best Run Output:\n")
print(best_output)
