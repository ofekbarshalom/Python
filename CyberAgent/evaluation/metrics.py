"""
Metrics computation for SNAPT evaluation.
"""

import numpy as np
from typing import List, Dict
from environment.snapt_env import SNAPTEnv
from config import DEFAULT_DEVICES, DEFAULT_EDGES


def compute_win_rate(attacker, defender, num_games: int = 100,
                     device_configs=None, edges=None) -> Dict:
    """Compute win rate and mean reward for an attacker-defender pair."""
    device_configs = device_configs or DEFAULT_DEVICES
    edges = edges or DEFAULT_EDGES
    env = SNAPTEnv(device_configs, edges)

    wins = 0
    rewards = []
    for _ in range(num_games):
        result = env.play_game(attacker, defender)
        if result['attacker_wins']:
            wins += 1
        rewards.append(result['reward'])

    return {
        'win_rate': wins / num_games,
        'mean_reward': np.mean(rewards),
        'std_reward': np.std(rewards),
        'wins': wins,
        'total': num_games,
    }
