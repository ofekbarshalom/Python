import time
import subprocess
import sys
import select

TARGET_IP = "192.168.1.100"

OUTPUT_FILE = "pings_results_c.txt"

rtt_times = []
ping_count = 0

print(f"Sending pings to {TARGET_IP}... Press 'q' and Enter to stop.\n")

while True:
    print("Press 'q' + Enter to quit, or wait for next ping...", flush=True)
    i, _, _ = select.select([sys.stdin], [], [], 0)
    if i:
        user_input = sys.stdin.readline().strip()
        if user_input.lower() == 'q':
            print("Exiting ping loop.")
            break

    try:
        result = subprocess.run(
            ["ping", "-c", "1", TARGET_IP],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        output = result.stdout
        ping_count += 1

        if "time=" in output:
            time_ms = float(output.split("time=")[1].split(" ")[0])
            rtt_times.append(time_ms)
            print(f"Ping {ping_count}: {time_ms} ms")
        else:
            print(f"Ping {ping_count}: Failed (no reply)")
            rtt_times.append(None)

    except Exception as e:
        print(f"Ping {ping_count}: Error - {e}")
        rtt_times.append(None)

    time.sleep(5)

# Write to file
with open(OUTPUT_FILE, "w") as f:
    for i, rtt in enumerate(rtt_times, start=1):
        if rtt is not None:
            f.write(f"Ping {i}: {rtt:.2f} ms\n")
        else:
            f.write(f"Ping {i}: failed\n")

    valid_rtts = [r for r in rtt_times if r is not None]
    if valid_rtts:
        avg_rtt = sum(valid_rtts) / len(valid_rtts)
        f.write(f"avg_rtt: {avg_rtt:.2f} ms\n")
        print(f"\nAverage RTT: {avg_rtt:.2f} ms")
    else:
        f.write("avg_rtt: failed\n")
        print("\nNo successful pings.")
