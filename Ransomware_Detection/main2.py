import os
import time
import platform
from math import log2
from collections import deque
from datetime import datetime, timedelta

# Calculate Shannon entropy of given binary data
def calculate_entropy(data):
    if not data:
        return 0
    freq = [data.count(b) / len(data) for b in set(data)]
    return -sum(p * log2(p) for p in freq)

# Read a representative sample of a file for entropy calculation
def read_sample_for_entropy(filepath, chunk_size=4096, total_read_limit=1024*1024):
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

# Create initial database (baseline) of all file entropies, sizes, and scores
def get_entropy_map(directory):
    entropy_map = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            data = read_sample_for_entropy(full_path)
            entropy = calculate_entropy(data)
            size = len(data)

            if entropy > 7.5:
                print(f"\nALERT: Suspicious file detected during initial scan: {full_path}")
                print(f"    Entropy: {entropy:.2f}, Size: {size} bytes")

            entropy_map[full_path] = {
                "entropy": entropy,
                "size": size,
                "score": 0
            }
    return entropy_map


suspicious_events = deque()

# Display alert for suspicious file change and track bursts
def handle_suspicious_event(file_path, score, e_diff, s_ratio, old_entropy=None, new_entropy=None, old_size=None, new_size=None):
    now = datetime.now()
    suspicious_events.append(now)
    while suspicious_events and (now - suspicious_events[0]) > timedelta(seconds=60):
        suspicious_events.popleft()

    print(f"\nALERT: Suspicious file change detected in: {file_path}")
    if old_entropy is not None:
        print(f"    Entropy: {old_entropy:.2f} -> {new_entropy:.2f}  (Δ {e_diff:.2f})")
    if old_size is not None:
        print(f"    Size: {old_size} -> {new_size}  (Δ {s_ratio:.0%})")
    print(f"    Threat score: {score} / 7")

    if len(suspicious_events) >= 5:
        print(f"\nMULTIPLE SUSPICIOUS CHANGES DETECTED ({len(suspicious_events)} in last 60s)")
        print("POSSIBLE RANSOMWARE ATTACK IN PROGRESS")

def score_file_change(old_entropy, new_entropy, old_size, new_size, file_path):
    score = 0
    entropy_diff = abs(new_entropy - old_entropy)
    entropy_ratio = entropy_diff / old_entropy if old_entropy else 0
    size_diff = abs(new_size - old_size)
    size_ratio = size_diff / old_size if old_size else 0

    if entropy_diff > 1.0:
        score += 2
    elif entropy_ratio > 0.2:
        score += 1

    if new_size > old_size:
        if size_ratio > 1.0:
            score += 2
        elif size_ratio > 0.3:
            score += 1

    if not file_path.lower().endswith(".txt"):
        score += 2

    return score, entropy_diff, size_ratio

def process_file_change(full_path, baseline):
    data = read_sample_for_entropy(full_path)
    new_entropy = calculate_entropy(data)
    new_size = len(data)

    # New file not in baseline
    if full_path not in baseline:
        if new_entropy > 7.5:
            print(f"\nALERT: New file with high entropy: {full_path}")
            print(f"    Entropy: {new_entropy:.2f}, Size: {new_size} bytes")
            suspicious_events.append(datetime.now())
        baseline[full_path] = {"entropy": new_entropy, "size": new_size, "score": 0}
        return

    # File exists in baseline → check for change
    old_entry = baseline[full_path]
    old_entropy = old_entry["entropy"]
    old_size = old_entry["size"]
    prev_score = old_entry.get("score", 0)

    score, e_diff, s_ratio = score_file_change(old_entropy, new_entropy, old_size, new_size, full_path)

    if score != prev_score:
        print(f"        Score changed for: {full_path}")
        print(f"        Entropy: {old_entropy:.2f} -> {new_entropy:.2f} (Δ {e_diff:.2f})")
        print(f"        Size: {old_size} -> {new_size} (Δ {s_ratio:.2%})")
        print(f"        Score: {score} (was {prev_score})")

    if score >= 4:
        handle_suspicious_event(full_path, score, e_diff, s_ratio,old_entropy, new_entropy, old_size, new_size)

    baseline[full_path] = {
        "entropy": new_entropy,
        "size": new_size,
        "score": score
    }

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
