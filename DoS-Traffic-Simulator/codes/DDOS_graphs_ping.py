import matplotlib.pyplot as plt
import numpy as np


# Parse RTT values from ping results file
def parse_ping_file(filename):
    rtts = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("Ping") and "failed" not in line:
                try:
                    rtt = float(line.split(":")[1].replace("ms", "").strip())
                    rtts.append(rtt)
                except:
                    continue
    return rtts


# Plot histogram with RTTs
def plot_ping_histogram(rtts, title, filename):
    plt.figure(figsize=(10, 6))
    plt.hist(rtts, bins=10, edgecolor='black', log=True)  # 10 bins, log y-axis
    plt.xlabel("RTT (ms)")  # RTT on x-axis
    plt.ylabel("Number of Pings")  # Count on y-axis
    plt.title(title)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"[+] Saved graph: {filename}")


# Load RTTs
rtts_c = parse_ping_file("pings_results_c")
rtts_p = parse_ping_file("pings_results_p")

# Plot the RTT histograms
plot_ping_histogram(rtts_c, "RTT During C SYN Flood Attack", "Pings_c.png")
plot_ping_histogram(rtts_p, "RTT During Python SYN Flood Attack", "Pings_p.png")

# Calculate statistics
avg_c = np.mean(rtts_c)
std_c = np.std(rtts_c)
avg_p = np.mean(rtts_p)
std_p = np.std(rtts_p)

# Print and save report
print("\nRTT REPORT:")
print(f"[C]      Avg RTT: {avg_c:.2f} ms | STD: {std_c:.2f} ms")
print(f"[Python] Avg RTT: {avg_p:.2f} ms | STD: {std_p:.2f} ms")

with open("ping_rtt_report.txt", "w") as f:
    f.write("RTT Report:\n")
    f.write(f"C Program:\n  Avg RTT: {avg_c:.2f} ms\n  STD: {std_c:.2f} ms\n")
    f.write(f"Python Program:\n  Avg RTT: {avg_p:.2f} ms\n  STD: {std_p:.2f} ms\n\n")
