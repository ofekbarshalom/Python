"""
Action probability heatmap visualization (replicates Figure 6).
Shows what each trained agent prefers to do from the initial game state.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict
from environment.snapt_env import SNAPTEnv
from config import DEFAULT_DEVICES, DEFAULT_EDGES


def plot_action_heatmap(attackers: Dict, defenders: Dict,
                        device_configs=None, edges=None,
                        save_path: str = None):
    """
    Plot heatmaps of action probabilities from the initial state.

    Args:
        attackers: {name: agent} dict
        defenders: {name: agent} dict
    """
    device_configs = device_configs or DEFAULT_DEVICES
    edges = edges or DEFAULT_EDGES
    env = SNAPTEnv(device_configs, edges)
    env.reset()

    atk_obs = env.network.get_attacker_observation()
    def_obs = env.network.get_defender_observation()
    n_devices = env.num_devices

    # Collect attacker probabilities
    atk_names = list(attackers.keys())
    atk_probs = np.zeros((len(atk_names), n_devices))
    for i, name in enumerate(atk_names):
        probs = attackers[name].get_action_probs(atk_obs)
        atk_probs[i] = probs

    # Collect defender probabilities
    def_names = list(defenders.keys())
    def_probs = np.zeros((len(def_names), n_devices * 2))
    for i, name in enumerate(def_names):
        probs = defenders[name].get_action_probs(def_obs)
        def_probs[i] = probs

    # Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Attacker heatmap
    atk_labels = [f"Attack d{i}" for i in range(n_devices)]
    sns.heatmap(atk_probs, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=atk_labels, yticklabels=atk_names,
                ax=ax1, vmin=0, vmax=1, cbar_kws={'label': 'Probability'})
    ax1.set_title('Attacker Move Probabilities\n(Initial State)')
    ax1.set_xlabel('Action')
    ax1.set_ylabel('Algorithm')

    # Defender heatmap
    def_labels = ([f"Detect d{i}" for i in range(n_devices)] +
                  [f"Secure d{i}" for i in range(n_devices)])
    sns.heatmap(def_probs, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=def_labels, yticklabels=def_names,
                ax=ax2, vmin=0, vmax=1, cbar_kws={'label': 'Probability'})
    ax2.set_title('Defender Move Probabilities\n(Initial State)')
    ax2.set_xlabel('Action')
    ax2.set_ylabel('Algorithm')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
