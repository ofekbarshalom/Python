import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# File names
files = {
    'Google Traffic': 'google_traffic.csv',
    'Spotify Traffic': 'spotify_traffic.csv'
}

# Colors for each application
colors = {
    'Google Traffic': 'blue',
    'Spotify Traffic': 'green'
}

# Load CSVs
data = {}
for app, file in files.items():
    data[app] = pd.read_csv(file)

# ----- A: Protocol Distribution by App -----
protocol_counts = {}
for app, df in data.items():
    protocol_counts[app] = df['Protocol'].value_counts()

# Combine into one DataFrame
protocol_df = pd.DataFrame(protocol_counts).fillna(0)
protocol_df = protocol_df.sort_index()

# Create side by side bar chart
bar_width = 0.35
index = np.arange(len(protocol_df.index))
fig, ax = plt.subplots()

# Plot bars for each app
for i, (app, color) in enumerate(colors.items()):
    ax.bar(index + i * bar_width, protocol_df[app], bar_width, label=app, color=color)

ax.set_title('A: Protocol Distribution by App')
ax.set_xlabel('Protocol')
ax.set_ylabel('Count')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(protocol_df.index, rotation=45)
ax.legend(loc='upper right')
ax.grid(True)
plt.tight_layout()
plt.savefig('protocol_distribution_by_app.png')
plt.show()

# ----- B: Packet Size Distribution -----
plt.figure(figsize=(10, 6))
bins = np.linspace(0, 2000, 50)  # More bins for better resolution

for app, df in data.items():
    plt.hist(df['Length'], bins=bins, color=colors[app], alpha=0.5, label=app, edgecolor='black')

plt.title('B: Packet Size Distribution')
plt.xlabel('Packet Size (Bytes)')
plt.ylabel('Frequency')
plt.yscale('log')  # Logarithmic scale for better distribution view
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('packet_size_distribution_improved.png')
plt.show()

# ----- C: Flow Size (Number of Packets) -----
flow_sizes = {app: len(df) for app, df in data.items()}
plt.bar(flow_sizes.keys(), flow_sizes.values(), color=[colors['Google Traffic'], colors['Spotify Traffic']])
plt.title('C: Flow Size by App')
plt.xlabel('App')
plt.ylabel('Number of Packets')
plt.grid(True)
plt.tight_layout()
plt.savefig('flow_size_by_app.png')
plt.show()

# ----- D: Flow Volume (Total Bytes) -----
flow_volumes = {app: df['Length'].sum() for app, df in data.items()}
plt.bar(flow_volumes.keys(), flow_volumes.values(), color=[colors['Google Traffic'], colors['Spotify Traffic']])
plt.title('D: Flow Volume by App')
plt.xlabel('App')
plt.ylabel('Total Bytes Transmitted')
plt.grid(True)
plt.tight_layout()
plt.savefig('flow_volume_by_app.png')
plt.show()

print("Analysis Complete! Check the generated graphs.")
