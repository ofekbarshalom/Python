# DoS Traffic Simulator

A educational project for comparing **SYN traffic generation and network impact** between a C implementation and a Python implementation.

## ⚠️ Important Notice

Use this project **only in a controlled lab environment** and **only on systems you own or have explicit permission to test**.

Unauthorized denial-of-service testing is illegal and unethical.

## Project Structure

- `codes/attack.c` — C-based SYN packet sender (raw sockets)
- `codes/Attack.py` — Python SYN packet sender using Scapy
- `codes/Monitor.py` — Ping monitor script to track RTT during tests
- `codes/DDOS_graphs_ping.py` — Creates RTT histograms and summary report
- `codes/DDOS_graphs_syn.py` — Creates SYN send-time histograms and summary report
- `output/` — Example output files and generated graphs

## Requirements

Recommended environment: **Linux / Kali / Ubuntu / WSL** (raw sockets + `ping -c` behavior).

- Python 3.9+
- `pip install scapy matplotlib numpy`
- GCC (`gcc`) for the C implementation
- Root/admin privileges for raw packet sending

## Quick Setup

1. Open terminal in project root:

   ```bash
   cd DoS-Traffic-Simulator
   ```

2. Install Python dependencies:

   ```bash
   pip install scapy matplotlib numpy
   ```

3. Update target/attacker IPs as needed:
   - `codes/Attack.py` (`target_ip`, `target_port`)
   - `codes/attack.c` (`target_ip`, `my_ip`, `target_port`)
   - `codes/Monitor.py` (`TARGET_IP`)

## Running the Experiment

### 1) Run C SYN sender

```bash
cd codes
gcc attack.c -o attack
sudo ./attack
```

Expected output file: `syns_results_c.txt`

### 2) Run Python SYN sender

```bash
cd codes
sudo python Attack.py
```

Expected output file: `syns_results_p.txt`

### 3) Run ping monitor (during tests)

```bash
cd codes
python Monitor.py
```

- Script pings every 5 seconds
- Press `q` then Enter to stop
- Output file: `pings_results_c.txt` (or rename/copy per scenario)

### 4) Generate graphs and reports

```bash
cd codes
python DDOS_graphs_syn.py
python DDOS_graphs_ping.py
```

Generated files include:
- `Syn_pkts_c.png`, `Syn_pkts_p.png`
- `Pings_c.png`, `Pings_p.png`
- `syn_send_report.txt`, `ping_rtt_report.txt`

## Output Notes

Some scripts write results into the current working directory. For clean organization, run scripts from `codes/` and then move final artifacts into `output/` if needed.

## Troubleshooting

- **Permission denied / raw socket error**: run with `sudo` (or admin privileges)
- **No module named scapy/matplotlib/numpy**: reinstall dependencies with `pip`
- **Ping command issue on Windows**: script currently uses `ping -c`; use Linux/WSL or adjust to Windows flags
