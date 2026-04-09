"""
Training utilities: seeding and logging.
"""

import os
import random
import numpy as np
import torch
import json


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


class TrainingLogger:
    """Logs training metrics to memory and optionally to file."""

    def __init__(self, log_dir: str = "results"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.metrics = {}

    def log(self, key: str, value: float, step: int):
        if key not in self.metrics:
            self.metrics[key] = []
        self.metrics[key].append((step, value))

    def save(self, filename: str):
        path = os.path.join(self.log_dir, filename)
        serializable = {}
        for key, values in self.metrics.items():
            serializable[key] = [(int(s), float(v)) for s, v in values]
        with open(path, 'w') as f:
            json.dump(serializable, f, indent=2)

    def get_values(self, key: str):
        if key not in self.metrics:
            return [], []
        steps, values = zip(*self.metrics[key])
        return list(steps), list(values)
