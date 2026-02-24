import matplotlib.pyplot as plt
import numpy as np

# Parse send times from result files
def parse_syn_results(filename):
    send_times = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Total") or line.startswith("Average"):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                send_times.append(int(parts[1]))  # microseconds
    return send_times

# Plot histogram with 10 bins
def plot_histogram(send_times, title, filename):
    plt.figure(figsize=(10, 6))
    plt.hist(send_times, bins=10, edgecolor='black', color='mediumseagreen', log=True)  # log y-axis
    plt.xlabel("Send Time (microseconds)")  # x-axis is time to send a packet
    plt.ylabel("Number of Packets")         # y-axis is packet count per bin
    plt.title(title)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"[+] Saved histogram: {filename}")


# Load data
c_times = parse_syn_results("syns_results_c.txt")
p_times = parse_syn_results("syns_results_p.txt")

# Create histograms with exactly 10 bins
plot_histogram(c_times, "C Program - SYN Packet Send Time Histogram", "Syn_pkts_c.png")
plot_histogram(p_times, "Python Program - SYN Packet Send Time Histogram", "Syn_pkts_p.png")

# Stats
avg_c = np.mean(c_times)
std_c = np.std(c_times)
avg_p = np.mean(p_times)
std_p = np.std(p_times)

# Print and Save Report
print("\nShort Report:")
print(f"[C]     Avg: {avg_c:.2f} ms | STD: {std_c:.2f}")
print(f"[Python] Avg: {avg_p:.2f} ms | STD: {std_p:.2f}")

with open("syn_send_report.txt", "w", encoding="utf-8") as f:
    f.write("SYN Packet Timing Report:\n")
    f.write(f"C Program:\n  Avg: {avg_c:.2f} ms\n  STD: {std_c:.2f} ms\n")
    f.write(f"Python Program:\n  Avg: {avg_p:.2f} ms\n  STD: {std_p:.2f} ms\n\n")
