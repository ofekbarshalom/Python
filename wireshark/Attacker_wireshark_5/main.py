import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import hashlib
import re

# File names with the first word capitalized
files = {
    'Google Traffic': 'Attacker_google_traffic.csv',
    'Firefox Traffic': 'Attacker_firefox_traffic.csv',
    'Spotify Traffic': 'Attacker_spotify_traffic.csv',
    'YouTube Traffic': 'Attacker_Youtube_traffic.csv',
    'Zoom Traffic': 'Attacker_zoom_traffic.csv'
}

# Colors for each application
colors = {
    'Google Traffic': 'blue',
    'Firefox Traffic': 'orange',
    'Spotify Traffic': 'green',
    'YouTube Traffic': 'red',
    'Zoom Traffic': 'purple'
}


# Improved Function to extract source and destination ports
def extract_ports(info):
    try:
        # Extract source and destination ports using regex
        ports = re.findall(r"(\d+)\s+>\s+(\d+)", info)
        if ports:
            src_port, dst_port = ports[0]
            return src_port, dst_port
        else:
            # Return "Unknown" if no ports found
            return "Unknown", "Unknown"
    except:
        # In case of an exception, return "Unknown"
        return "Unknown", "Unknown"


# Function to calculate flow ID by hashing the 4-tuple
def calculate_flow_id(df):
    flow_ids = []
    for _, row in df.iterrows():
        src_ip = row['Source']
        dst_ip = row['Destination']
        src_port, dst_port = extract_ports(row['Info'])

        # If either port is unknown, mark flow ID as None
        if src_port == "Unknown" or dst_port == "Unknown":
            flow_id = None
        else:
            # Calculate flow ID as the hash of the 4-tuple
            four_tuple = f"{src_ip}-{dst_ip}-{src_port}-{dst_port}"
            flow_id = hashlib.md5(four_tuple.encode()).hexdigest()

        flow_ids.append(flow_id)
    df['flow_id'] = flow_ids
    return df


# Scenario 1: Detailed Information (with Flow ID)
def plot_scenario_1(df, app_name):
    # Drop rows with no flow ID
    df = df.dropna(subset=['flow_id'])

    # Packet Size Over Time (with Flow ID)
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], df['size'], label='Packet Size', color=colors[app_name])
    plt.title(f'{app_name} - Packet Size Over Time (With Flow ID)')
    plt.xlabel('Timestamp')
    plt.ylabel('Packet Size (Bytes)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{app_name}_Packet_Size_Over_Time_Flow_ID.png")
    plt.close()

    # Flow Size Distribution
    flow_counts = df['flow_id'].value_counts()
    plt.figure(figsize=(10, 6))
    plt.hist(flow_counts, bins=50, alpha=0.7, label='Flow Size (Packets)', color=colors[app_name])
    plt.title(f'{app_name} - Flow Size Distribution')
    plt.xlabel('Number of Packets')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{app_name}_Flow_Size_Distribution.png")
    plt.close()

    # Flow Volume Distribution
    flow_volumes = df.groupby('flow_id')['size'].sum()
    plt.figure(figsize=(10, 6))
    plt.hist(flow_volumes, bins=50, alpha=0.7, label='Flow Volume (Bytes)', color=colors[app_name])
    plt.title(f'{app_name} - Flow Volume Distribution')
    plt.xlabel('Bytes Transmitted')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{app_name}_Flow_Volume_Distribution.png")
    plt.close()


# Scenario 2: Limited Information (No Flow ID)
def plot_scenario_2(df, app_name):
    # Packet Size Distribution
    plt.figure(figsize=(10, 6))
    plt.hist(df['size'], bins=50, alpha=0.7, label='Packet Size Distribution', color=colors[app_name])
    plt.title(f'{app_name} - Packet Size Distribution (No Flow ID)')
    plt.xlabel('Packet Size (Bytes)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{app_name}_Packet_Size_Distribution_No_Flow_ID.png")
    plt.close()

    # Calculate packet inter-arrival times
    df['inter_arrival'] = df['Time'].diff()

    # Inter-Arrival Time
    plt.figure(figsize=(10, 6))
    plt.plot(df['Time'], df['inter_arrival'], label='Inter-Arrival Time', color=colors[app_name])
    plt.title(f'{app_name} - Packet Inter-Arrival Time (No Flow ID)')
    plt.xlabel('Timestamp')
    plt.ylabel('Inter-Arrival Time (s)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{app_name}_Inter_Arrival_Time_No_Flow_ID.png")
    plt.close()


# Analyze all CSV files
def analyze_all():
    for app_name, file in files.items():
        print(f"\nAnalyzing {app_name}...")
        df = pd.read_csv(file)

        # Use 'Time' as the timestamp and 'Length' as the packet size
        df = df.sort_values('Time')  # Ensure timestamps are in order
        df['size'] = df['Length']

        # Calculate Flow ID for Scenario 1
        df = calculate_flow_id(df)

        # Scenario 1: Detailed Information (With Flow ID)
        plot_scenario_1(df, app_name)

        # Scenario 2: Limited Information (No Flow ID)
        plot_scenario_2(df, app_name)

    print("\nAll graphs saved in the same directory as the script.")


# Run the analysis
if __name__ == '__main__':
    analyze_all()
