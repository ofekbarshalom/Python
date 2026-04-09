"""
Training reward curves visualization.
Shows how attacker reward evolves during training for each algorithm.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple


def smooth(values: List[float], window: int = 50) -> np.ndarray:
    """Apply rolling average smoothing."""
    if len(values) < window:
        return np.array(values)
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode='valid')


def plot_training_curves(logs: Dict[str, List[Tuple[int, float]]],
                         title: str = "Training Reward Over Time",
                         ylabel: str = "Attacker Reward",
                         save_path: str = None,
                         window: int = 50):
    """
    Plot training curves for multiple algorithms.

    Args:
        logs: {algorithm_name: [(step, value), ...]}
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {'A2C': '#e74c3c', 'CEM': '#3498db', 'Random': '#95a5a6'}

    for name, data in logs.items():
        steps, values = zip(*data) if data else ([], [])
        steps = list(steps)
        values = list(values)
        color = colors.get(name, None)

        # Raw values (faded)
        ax.plot(steps, values, alpha=0.15, color=color)

        # Smoothed values
        smoothed = smooth(values, window)
        smoothed_steps = steps[window - 1:] if len(steps) >= window else steps
        ax.plot(smoothed_steps, smoothed, label=name, linewidth=2, color=color)

    ax.set_xlabel('Training Iteration')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


def plot_comparison_curves(a2c_logs: Dict, cem_logs: Dict,
                           save_path: str = None):
    """
    Plot side-by-side: reward vs random defender, and reward vs trained defender.
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    for ax, key, title in [
        (axes[0], 'eval_vs_random_def', 'Attacker Reward vs Random Defender'),
        (axes[1], 'eval_vs_trained_def', 'Attacker Reward vs Trained Defender'),
    ]:
        for name, logs, color in [
            ('A2C', a2c_logs, '#e74c3c'),
            ('CEM', cem_logs, '#3498db'),
        ]:
            if key in logs:
                steps, values = zip(*logs[key]) if logs[key] else ([], [])
                ax.plot(steps, values, label=name, linewidth=2, color=color, marker='o', markersize=3)

        ax.set_xlabel('Training Iteration')
        ax.set_ylabel('Mean Attacker Reward')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
