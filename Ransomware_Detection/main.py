import os
import time
import platform
from math import log2
from collections import defaultdict


def calculate_entropy(data):
    if not data:
        return 0
    freq = [data.count(b) / len(data) for b in set(data)]
    return -sum(p * log2(p) for p in freq)


def get_entropy_map(directory):
    entropy_map = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                with open(full_path, 'rb') as f:
                    data = f.read(1024 * 1024)
                    entropy_map[full_path] = calculate_entropy(data)
            except Exception:
                continue
    return entropy_map


# ----------- Linux Monitor -----------
def monitor_linux(directory, baseline_entropy):
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
                with open(full_path, 'rb') as f:
                    data = f.read(1024 * 1024)
                    new_entropy = calculate_entropy(data)
                    old_entropy = baseline_entropy.get(full_path)

                    if old_entropy is not None and new_entropy - old_entropy > 1.0:
                        print(f"ALERT: Entropy spike in {full_path} ({old_entropy:.2f} ➜ {new_entropy:.2f})")

                    baseline_entropy[full_path] = new_entropy
            except:
                continue


# ----------- Windows Monitor -----------
def monitor_windows(directory, baseline_entropy):
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            full_path = event.src_path
            try:
                with open(full_path, 'rb') as f:
                    data = f.read(1024 * 1024)
                    new_entropy = calculate_entropy(data)
                    old_entropy = baseline_entropy.get(full_path)

                    if old_entropy is not None and new_entropy - old_entropy > 1.0:
                        print(f"ALERT: Entropy spike in {full_path} ({old_entropy:.2f} ➜ {new_entropy:.2f})")

                    baseline_entropy[full_path] = new_entropy
            except:
                pass

    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    print("[Windows] Monitoring file changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# ----------- Main -----------
if __name__ == '__main__':
    directory_to_monitor = os.path.abspath(input("Enter directory to monitor: ").strip())

    if not os.path.isdir(directory_to_monitor):
        print("Invalid directory.")
        exit(1)

    print("Calculating initial entropy...")
    entropy_map = get_entropy_map(directory_to_monitor)

    system = platform.system()
    if system == 'Linux':
        monitor_linux(directory_to_monitor, entropy_map)
    elif system == 'Windows':
        monitor_windows(directory_to_monitor, entropy_map)
    else:
        print(f"Unsupported OS: {system}")
