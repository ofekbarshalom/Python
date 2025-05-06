# Ransomware Detection Script - Cross-Platform (Linux/Windows)

# ------------------------------------------------------------
# This script uses entropy calculations based on Shannon's Information Theory:
# Shannon, C. E. "A Mathematical Theory of Communication", Bell System Technical Journal, 1948.
# https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf

# It also uses ransomware detection indicators inspired by:
# Nolen Scaife et al. "CryptoDrop: Stopping Ransomware Attacks on User Data", ICDCS 2016.
# https://people.cs.vt.edu/~saverese/papers/scaife-icdcs16.pdf
# ------------------------------------------------------------

# ------------------------------------------------------------
# System Efficiency Analysis Based on Three Key Criteria:
#
# A. Memory Usage – How much data is stored in memory?
# - We store a mapping for each file, including entropy and size => O(n), where n is the number of files.
# - Our memory usage is efficient: O(n), since we only store lightweight metadata per file.
#
# B. Runtime Complexity – How long does one scan or detection take?
# - Full initial scan: O(n), since we read all files and compute entropy.
# - On file change: O(1) to detect event (via watchdog/inotify), O(log(n)) to look up data in the dictionary.
# - Very efficient runtime due to event-driven architecture (not polling).
#
# C. I/O Complexity – How many disk reads are performed?
# - One read per file during initial scan => O(n).
# - Afterward: disk reads only on actual file events (not periodic scanning).
# - No polling overhead – system responds only to real-time file events.
# ------------------------------------------------------------
#
# ------------------------------------------------------------
# Code Overview and Scoring System:
#
# This script monitors a specified directory for suspicious file changes
# that may indicate ransomware activity. It does this by calculating the
# entropy and size of files over time and comparing them to their original state.
#
# Main detection logic is based on a scoring system:
# - If a file's entropy increases significantly (e.g., > 1.0 or over 7.5 absolute), +7 points
# - If the file size grows sharply (e.g., >60% or doubles), +2 points
# - If the file has a suspicious extension (anything not .txt), +7 points
# - If the file is small and entropy increases moderately (e.g., >0.5 and >6.5), +7 points
#
# If a file’s total score reaches 7 or higher, it is flagged as potentially malicious.
# Alerts are printed to the terminal with details on entropy, size, and score.
#
# The script uses:
# - inotify_simple (Linux) or watchdog (Windows) to detect file changes in real time
# - Shannon entropy to detect randomness typical of encryption
# - Metadata tracking per file for efficient, incremental monitoring
# ------------------------------------------------------------
#
# ------------------------------------------------------------
# Requirements for running this script:
#
# Required Python Modules:
#
# - Windows: watchdog
#     Install with: pip install watchdog
#
# - Linux: inotify_simple
#     Install with: sudo pip install inotify_simple
#
# Running the Script:
# - Windows: python Ransomware_Detection.py
# - Linux: python3 Ransomware_Detection.py
#
# When prompted, enter the full absolute path to the folder you want to monitor.
#
# Example (Linux):
#     /home/hacker/Downloads/test_files
#
# Example (Windows):
#     C:\Users\YourUsername\Downloads\test_files
# ------------------------------------------------------------

import os
import time
import platform
from math import log2

# Calculate Shannon entropy of binary data
def calculate_entropy(data):
    if not data:
        return 0
    freq = [data.count(b) / len(data) for b in set(data)]
    return -sum(p * log2(p) for p in freq)

# Read a representative sample of a file for entropy calculation
def read_sample_for_entropy(filepath, chunk_size=4096, total_read_limit=1024 * 1024):
    try:
        file_size = os.path.getsize(filepath)
        with open(filepath, 'rb') as f:
            if file_size <= 2 * 1024 * 1024:
                return f.read()
            else:
                positions = [0, file_size // 2, max(0, file_size - chunk_size)]
                data = b''
                for pos in positions:
                    f.seek(pos)
                    data += f.read(min(chunk_size, total_read_limit // 3))
                return data
    except Exception:
        return b''

# Build a map of initial entropy and file size for all files
def get_entropy_map(directory):
    entropy_map = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            data = read_sample_for_entropy(full_path)
            entropy = calculate_entropy(data)
            size = len(data)
            ext = os.path.splitext(full_path)[1].lower()

            if entropy > 7.5 or ext != ".txt":
                reason = "High entropy" if entropy > 7.5 else "Suspicious extension"
                print(f"\nALERT: {reason} during initial scan: {full_path}")
                handle_suspicious_event(full_path, 7, 0, 0, None, entropy, None, size)

            entropy_map[full_path] = {
                "entropy": entropy,             # latest known entropy
                "initial_entropy": entropy,     # initial clean state entropy
                "size": size,
                "score": 0
            }
    return entropy_map

# Display malware alert for suspicious file
def handle_suspicious_event(file_path, score, e_diff, s_ratio, old_entropy=None, new_entropy=None, old_size=None, new_size=None):
    print(f"\nMALWARE DETECTED: {file_path}")
    if old_entropy is not None:
        print(f"    Entropy: {old_entropy:.2f} -> {new_entropy:.2f} (Δ {e_diff:.2f})")
    if old_size is not None:
        print(f"    Size: {old_size} -> {new_size} (Δ {s_ratio:.0%})")
    print(f"    Threat score: {score} / 7")

# Calculate threat score based on entropy and size changes
def score_file_change(initial_entropy, new_entropy, old_size, new_size, file_path):
    score = 0
    entropy_diff = abs(new_entropy - initial_entropy)
    entropy_ratio = entropy_diff / initial_entropy if initial_entropy else 0
    size_diff = abs(new_size - old_size)
    size_ratio = size_diff / old_size if old_size else 0

    if new_entropy > 7.5 or entropy_diff > 1.0 or entropy_ratio > 0.3:
        score += 7

    # Rule for small files
    if old_size < 1000 and new_entropy > 6.5 and entropy_diff > 0.5:
        score += 7

    if new_size > old_size:
        if size_ratio > 1.0 or size_ratio > 0.6:
            score += 2

    if not file_path.lower().endswith(".txt"):
        score += 7

    return score, entropy_diff, size_ratio

# Process a file change and decide if it's suspicious
def process_file_change(full_path, baseline):
    data = read_sample_for_entropy(full_path)
    new_entropy = calculate_entropy(data)
    new_size = len(data)

    if full_path not in baseline:
        baseline[full_path] = {
            "entropy": new_entropy,
            "initial_entropy": new_entropy,
            "size": new_size,
            "score": 0
        }
        return

    old_entry = baseline[full_path]
    old_entropy = old_entry["entropy"]
    initial_entropy = old_entry["initial_entropy"]
    old_size = old_entry["size"]
    prev_score = old_entry.get("score", 0)

    score, e_diff, s_ratio = score_file_change(initial_entropy, new_entropy, old_size, new_size, full_path)

    if score != prev_score:
        print(f"\nScore changed for: {full_path}")
        print(f"    Entropy: {old_entropy:.2f} -> {new_entropy:.2f} (Δ {e_diff:.2f})")
        print(f"    Size: {old_size} -> {new_size} (Δ {s_ratio:.2%})")
        print(f"    Score: {score} (was {prev_score})")

    if score >= 7:
        handle_suspicious_event(full_path, score, e_diff, s_ratio, old_entropy, new_entropy, old_size, new_size)

    baseline[full_path] = {
        "entropy": new_entropy,
        "initial_entropy": initial_entropy,
        "size": new_size,
        "score": score
    }

# File monitor for Linux using inotify
def monitor_linux(directory, baseline):
    from inotify_simple import INotify, flags
    inotify = INotify()
    watch_flags = flags.MODIFY | flags.CREATE
    watch_descriptors = {}

    for root, dirs, _ in os.walk(directory):
        try:
            wd = inotify.add_watch(root, watch_flags)
            watch_descriptors[wd] = root
        except:
            continue

    print("[Linux] Monitoring file changes...")

    while True:
        for event in inotify.read():
            root = watch_descriptors.get(event.wd, '')
            filename = event.name
            full_path = os.path.join(root, filename)

            if not os.path.isfile(full_path):
                continue

            try:
                process_file_change(full_path, baseline)
            except Exception:
                continue

# File monitor for Windows using watchdog
def monitor_windows(directory, baseline):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def handle_event(self, full_path):
            if not os.path.isfile(full_path):
                return
            try:
                process_file_change(full_path, baseline)
            except Exception:
                pass

        def on_modified(self, event):
            self.handle_event(event.src_path)

        def on_created(self, event):
            self.handle_event(event.src_path)

        def on_moved(self, event):
            self.handle_event(event.dest_path)

    observer = Observer()
    observer.schedule(Handler(), directory, recursive=True)
    observer.start()
    print("[Windows] Monitoring file changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    directory_to_monitor = os.path.abspath(input("Enter directory to monitor: ").strip())

    if not os.path.isdir(directory_to_monitor):
        print("Invalid directory.")
        exit(1)

    print("Calculating initial entropy and size...")
    entropy_map = get_entropy_map(directory_to_monitor)

    system = platform.system()
    if system == 'Linux':
        monitor_linux(directory_to_monitor, entropy_map)
    elif system == 'Windows':
        monitor_windows(directory_to_monitor, entropy_map)
    else:
        print(f"Unsupported OS: {system}")
