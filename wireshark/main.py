import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the exported CSV file from Wireshark
df = pd.read_csv('app_traffic.csv')

# Display the first few rows of the data
print(df.head())

# ----- A: IP Header Fields -----
# Source IP Frequency
src_ip_freq = df['Source'].value_counts().head(10)
src_ip_freq.plot(kind='bar', color='blue', alpha=0.7)
plt.title('Top 10 Source IPs')
plt.xlabel('Source IP')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('top_10_source_ips.png')
plt.show()

# Destination IP Frequency
dst_ip_freq = df['Destination'].value_counts().head(10)
dst_ip_freq.plot(kind='bar', color='green', alpha=0.7)
plt.title('Top 10 Destination IPs')
plt.xlabel('Destination IP')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('top_10_destination_ips.png')
plt.show()

# ----- B: TCP Header Fields -----
# Extract Source and Destination Ports from Info column more reliably
df['Src_Port'] = df['Info'].str.extract(r'Src Port: (\d+)|(\d+)\s->')
df['Dst_Port'] = df['Info'].str.extract(r'Dst Port: (\d+)|->\s(\d+)')

# Clean up extracted ports
df['Src_Port'] = df['Src_Port'].fillna('Unknown')
df['Dst_Port'] = df['Dst_Port'].fillna('Unknown')

# Source Port Frequency
src_port_freq = df['Src_Port'].value_counts().head(10)
src_port_freq.plot(kind='bar', color='purple', alpha=0.7)
plt.title('Top 10 Source Ports')
plt.xlabel('Source Port')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('top_10_source_ports.png')
plt.show()

# Destination Port Frequency
dst_port_freq = df['Dst_Port'].value_counts().head(10)
dst_port_freq.plot(kind='bar', color='orange', alpha=0.7)
plt.title('Top 10 Destination Ports')
plt.xlabel('Destination Port')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('top_10_destination_ports.png')
plt.show()

# ----- C: TLS Header Fields -----
# Extract TLS Version from Info column
df['TLS_Version'] = df['Info'].str.extract(r'TLSv(\d+\.\d+)')

# Clean up extracted versions
df['TLS_Version'] = df['TLS_Version'].fillna('Unknown')

# TLS Version Frequency
tls_version_freq = df['TLS_Version'].value_counts()
tls_version_freq.plot(kind='bar', color='red', alpha=0.7)
plt.title('TLS Version Usage')
plt.xlabel('TLS Version')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('tls_version_usage.png')
plt.show()

# ----- D: Packet Sizes -----
# Plot Packet Size Distribution
plt.hist(df['Length'], bins=30, color='blue', alpha=0.7)
plt.title('Packet Size Distribution')
plt.xlabel('Packet Size (Bytes)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('packet_size_distribution.png')
plt.show()

# ----- E: Packet Inter-Arrival Times -----
# Convert Time column to numeric
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')

# Calculate Inter-Packet Arrival Time
df['Inter_Arrival_Time'] = df['Time'].diff()

# Drop NaN values only from Inter_Arrival_Time
df = df.dropna(subset=['Inter_Arrival_Time'])

# Plot Inter-Packet Arrival Time Distribution
plt.hist(df['Inter_Arrival_Time'], bins=50, color='green', alpha=0.7)
plt.title('Inter-Packet Arrival Time Distribution')
plt.xlabel('Time Difference (Seconds)')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig('inter_packet_arrival_time.png')
plt.show()

# ----- F: Flow Size -----
# Calculate Flow Size
flow_size = len(df)
print(f'Total Flow Size: {flow_size} packets')

# ----- G: Flow Volume -----
# Calculate Flow Volume
flow_volume = df['Length'].sum()
print(f'Total Flow Volume: {flow_volume} bytes')
