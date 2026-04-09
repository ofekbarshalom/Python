"""
Extension experiment: test A2C and CEM on different network topologies.
Evaluates scalability beyond the paper's 3-node linear chain.
Usage: python -m experiments.run_extension
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
from training.a2c_trainer import A2CTrainer
from training.cem_trainer import CEMTrainer
from training.utils import set_seed
from agents.random_agent import RandomAgent
from evaluation.metrics import compute_win_rate
from config import (
    SEED, DEFAULT_DEVICES, DEFAULT_EDGES,
    STAR_4_DEVICES, STAR_4_EDGES,
    RING_5_DEVICES, RING_5_EDGES,
)

# Fewer iterations for extension (faster experiments)
EXTENSION_ITERATIONS = 1000


TOPOLOGIES = {
    'Chain-3': (DEFAULT_DEVICES, DEFAULT_EDGES),
    'Star-4': (STAR_4_DEVICES, STAR_4_EDGES),
    'Ring-5': (RING_5_DEVICES, RING_5_EDGES),
}


def main():
    print("=" * 60)
    print("  Extension: Topology Comparison")
    print("=" * 60)

    os.makedirs("figures", exist_ok=True)
    results = {}

    for topo_name, (devices, edges) in TOPOLOGIES.items():
        print(f"\n{'-' * 40}")
        print(f"  Topology: {topo_name} ({len(devices)} nodes)")
        print(f"{'-' * 40}")
        n_devices = len(devices)

        # Train A2C
        print(f"  Training A2C on {topo_name}...")
        set_seed(SEED)
        a2c_trainer = A2CTrainer(device_configs=devices, edges=edges)
        a2c_atk, a2c_def = a2c_trainer.train(num_iterations=EXTENSION_ITERATIONS)

        # Train CEM
        print(f"  Training CEM on {topo_name}...")
        set_seed(SEED)
        cem_trainer = CEMTrainer(device_configs=devices, edges=edges)
        cem_atk, cem_def = cem_trainer.train(num_iterations=EXTENSION_ITERATIONS)

        # Evaluate: each attacker vs each defender
        random_def = RandomAgent(action_size=n_devices * 2)

        a2c_vs_random = compute_win_rate(a2c_atk, random_def, device_configs=devices, edges=edges)
        cem_vs_random = compute_win_rate(cem_atk, random_def, device_configs=devices, edges=edges)
        a2c_vs_cem_def = compute_win_rate(a2c_atk, cem_def, device_configs=devices, edges=edges)
        cem_vs_a2c_def = compute_win_rate(cem_atk, a2c_def, device_configs=devices, edges=edges)

        results[topo_name] = {
            'A2C_vs_Random': a2c_vs_random['win_rate'],
            'CEM_vs_Random': cem_vs_random['win_rate'],
            'A2C_vs_CEM_def': a2c_vs_cem_def['win_rate'],
            'CEM_vs_A2C_def': cem_vs_a2c_def['win_rate'],
        }

        print(f"  A2C attacker win rate vs Random: {a2c_vs_random['win_rate']:.1%}")
        print(f"  CEM attacker win rate vs Random: {cem_vs_random['win_rate']:.1%}")
        print(f"  A2C attacker vs CEM defender:    {a2c_vs_cem_def['win_rate']:.1%}")
        print(f"  CEM attacker vs A2C defender:    {cem_vs_a2c_def['win_rate']:.1%}")

    # ── Plot results ──
    plot_topology_comparison(results)


def plot_topology_comparison(results: dict):
    """Bar chart comparing A2C and CEM across topologies."""
    topologies = list(results.keys())
    x = np.arange(len(topologies))
    width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))

    a2c_random = [results[t]['A2C_vs_Random'] * 100 for t in topologies]
    cem_random = [results[t]['CEM_vs_Random'] * 100 for t in topologies]
    a2c_cem = [results[t]['A2C_vs_CEM_def'] * 100 for t in topologies]
    cem_a2c = [results[t]['CEM_vs_A2C_def'] * 100 for t in topologies]

    ax.bar(x - 1.5 * width, a2c_random, width, label='A2C vs Random Def', color='#e74c3c', alpha=0.8)
    ax.bar(x - 0.5 * width, cem_random, width, label='CEM vs Random Def', color='#3498db', alpha=0.8)
    ax.bar(x + 0.5 * width, a2c_cem, width, label='A2C vs CEM Def', color='#e74c3c', alpha=0.5)
    ax.bar(x + 1.5 * width, cem_a2c, width, label='CEM vs A2C Def', color='#3498db', alpha=0.5)

    ax.set_xlabel('Network Topology')
    ax.set_ylabel('Attacker Win Rate (%)')
    ax.set_title('A2C vs CEM: Performance Across Network Topologies')
    ax.set_xticks(x)
    ax.set_xticklabels(topologies)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig("figures/topology_comparison.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("\nTopology comparison saved to figures/topology_comparison.png")


if __name__ == "__main__":
    main()
