import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# List of CSV files corresponding to each app
csv_files = {
    "Web-surfing 1": "web_surfing1.csv",
    "Web-surfing 2": "web_surfing2.csv",
    "Audio Streaming": "audio_streaming.csv",
    "Video Streaming": "video_streaming.csv",
    "Video Conference": "video_conference.csv"
}

# Protocols to analyze
protocols = ["DATA", "DNS", "DTLS", "OCSP", "STUN", "TCP", "TLS"]

# Dictionary to store protocol counts per app
protocol_counts = {app: {proto: 0 for proto in protocols} for app in csv_files.keys()}

# Load and analyze each CSV file
for app, file in csv_files.items():
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Count occurrences of each protocol
    protocol_distribution = df['Protocol'].value_counts()

    # Store the counts for each protocol
    for proto in protocols:
        protocol_counts[app][proto] = protocol_distribution.get(proto, 0)

# Convert protocol counts to a DataFrame for easier plotting
protocol_df = pd.DataFrame(protocol_counts)

# Plot Graph A: Protocol Distribution by App
protocol_df.T.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('A: IP Protocol Distribution by App')
plt.xlabel('Application')
plt.ylabel('Count')
plt.legend(title='Protocol', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('protocol_distribution_by_app.png')
plt.show()

# Plot Graph B: Packet Counts Per Protocol Per App
fig, ax = plt.subplots(figsize=(12, 8))
index = np.arange(len(protocol_df.columns))
bar_width = 0.15
opacity = 0.8

# Plotting each protocol as a grouped bar
for i, proto in enumerate(protocols):
    plt.bar(index + i * bar_width, protocol_df.loc[proto], bar_width, alpha=opacity, label=proto)

plt.title('B: Packet Counts Per Protocol Per App')
plt.xlabel('Application')
plt.ylabel('Count')
plt.xticks(index + bar_width * (len(protocols) / 2), protocol_df.columns)
plt.legend(title='Protocol', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('packet_counts_per_protocol_per_app.png')
plt.show()
