import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# File names with only the first word capitalized
files = {
    'Google Traffic': 'Google_traffic.csv',
    'Firefox Traffic': 'Firefox_traffic.csv',
    'Spotify Traffic': 'Spotify_traffic.csv',
    'YouTube Traffic': 'YouTube_traffic.csv',
    'Zoom Traffic': 'Zoom_traffic.csv'
}

# Colors for each application
colors = {
    'Google Traffic': 'blue',
    'Firefox Traffic': 'orange',
    'Spotify Traffic': 'green',
    'YouTube Traffic': 'red',
    'Zoom Traffic': 'purple'
}

# Load CSVs
data = {}
for app, file in files.items():
    data[app] = pd.read_csv(file)

# -----  A: Protocol Distribution by App -----
protocol_counts = {}
for app, df in data.items():
    protocol_counts[app] = df['Protocol'].value_counts()

# Combine into one DataFrame
protocol_df = pd.DataFrame(protocol_counts).fillna(0)
protocol_df = protocol_df.sort_index()

# Create side by side bar chart for Protocol Distribution
bar_width = 0.15
index = np.arange(len(protocol_df.index))
fig, ax = plt.subplots(figsize=(12, 6))

# Plot bars for each app
for i, (app, color) in enumerate(colors.items()):
    ax.bar(index + i * bar_width, protocol_df[app], bar_width, label=app, color=color)

ax.set_title('A: Protocol Distribution by App')
ax.set_xlabel('Protocol')
ax.set_ylabel('Count')
ax.set_xticks(index + bar_width * 2)
ax.set_xticklabels(protocol_df.index, rotation=45)
ax.legend(loc='upper right')
ax.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('protocol_distribution_by_app.png')
plt.show()

# ----- B: Destination Port Distribution (IPv4 and IPv6) -----
print("\n--- B: Destination Port Distribution (IPv4 and IPv6) ---")
for app, df in data.items():
    # Get the top 5 destination ports
    dest_ports = df['Destination'].value_counts().nlargest(5)

    # Plot the graph
    plt.figure(figsize=(12, 6))
    plt.bar(dest_ports.index, dest_ports.values, color=colors[app])
    plt.title(f'B: Destination Port Distribution - {app}')
    plt.xlabel('Destination Address')
    plt.ylabel('Frequency')

    # Rotate labels for better readability
    plt.xticks(rotation=45, ha='right')  # Rotate 45 degrees and align right

    # Optional: Wrap long labels (uncomment if needed)
    # labels = [re.sub(r"(.{15})", "\\1\n", label) for label in dest_ports.index]
    # plt.xticks(ticks=range(len(labels)), labels=labels)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# ----- C: TLS Handshake Type (TLS Header Fields) -----
print("\n--- C: TLS Handshake Type ---")
for app, df in data.items():
    tls_handshake = df['Info'].str.extract(r'(Client Hello|Server Hello)')[0].value_counts().nlargest(5)
    plt.figure(figsize=(10, 6))
    plt.bar(tls_handshake.index, tls_handshake.values, color=colors[app])
    plt.title(f'C: TLS Handshake Type - {app}')
    plt.xlabel('Handshake Type')
    plt.ylabel('Frequency')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


# ----- D: Packet Size Distribution -----
plt.figure(figsize=(12, 6))
bins = np.linspace(0, 2000, 50)  # More bins for better resolution

for app, df in data.items():
    plt.hist(df['Length'], bins=bins, color=colors[app], alpha=0.5, label=app, edgecolor='black')

plt.title('D: Packet Size Distribution')
plt.xlabel('Packet Size (Bytes)')
plt.ylabel('Frequency')
plt.yscale('log')  # Logarithmic scale for better distribution view
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('packet_size_distribution.png')
plt.show()

# ----- E: Packet Inter-Arrival Times -----
plt.figure(figsize=(12, 6))

for app, df in data.items():
    # Convert Time column to datetime, auto-detecting the format
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

    # Drop rows where Time could not be parsed
    df = df.dropna(subset=['Time'])

    # Calculate Inter-Arrival Times
    inter_arrivals = df['Time'].diff().dt.total_seconds().dropna()

    # Check if inter_arrivals is not empty to avoid plotting empty data
    if not inter_arrivals.empty:
        # Plot Histogram
        plt.hist(inter_arrivals, bins=50, alpha=0.5, label=app, color=colors[app], edgecolor='black')

plt.title('E: Packet Inter-Arrival Times')
plt.xlabel('Inter-Arrival Time (Seconds)')
plt.ylabel('Frequency')
plt.yscale('log')  # Logarithmic scale for better view
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

# ----- F: Flow Size (Number of Packets) -----
flow_sizes = {app: len(df) for app, df in data.items()}
plt.figure(figsize=(10, 6))
plt.bar(flow_sizes.keys(), flow_sizes.values(), color=[colors[app] for app in flow_sizes.keys()])
plt.title('F: Flow Size by App')
plt.xlabel('App')
plt.ylabel('Number of Packets')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('flow_size_by_app.png')
plt.show()

# ----- G: Flow Volume (Total Bytes) -----
flow_volumes = {app: df['Length'].sum() for app, df in data.items()}
plt.figure(figsize=(10, 6))
plt.bar(flow_volumes.keys(), flow_volumes.values(), color=[colors[app] for app in flow_volumes.keys()])
plt.title('G: Flow Volume by App')
plt.xlabel('App')
plt.ylabel('Total Bytes Transmitted')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('flow_volume_by_app.png')
plt.show()

print("Analysis Complete! Check the generated graphs.")
