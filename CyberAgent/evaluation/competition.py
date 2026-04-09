"""
Round-robin competition framework for evaluating trained agents.
Replicates Table 7 from the paper.
"""

import numpy as np
import pandas as pd
from typing import Dict
from environment.snapt_env import SNAPTEnv
from config import COMPETITION_GAMES, DEFAULT_DEVICES, DEFAULT_EDGES


def run_competition(attackers: Dict, defenders: Dict,
                    num_games: int = COMPETITION_GAMES,
                    device_configs=None, edges=None) -> pd.DataFrame:
    """
    Run round-robin competition between all attacker-defender pairs.

    Args:
        attackers: dict of {name: agent}
        defenders: dict of {name: agent}
        num_games: games per matchup

    Returns:
        DataFrame where cell (i,j) = attacker i wins out of num_games vs defender j
    """
    device_configs = device_configs or DEFAULT_DEVICES
    edges = edges or DEFAULT_EDGES
    env = SNAPTEnv(device_configs, edges)

    atk_names = list(attackers.keys())
    def_names = list(defenders.keys())
    results = np.zeros((len(atk_names), len(def_names)))

    for i, atk_name in enumerate(atk_names):
        for j, def_name in enumerate(def_names):
            wins = 0
            for _ in range(num_games):
                result = env.play_game(attackers[atk_name], defenders[def_name])
                if result['attacker_wins']:
                    wins += 1
            results[i][j] = wins

    df = pd.DataFrame(results, index=atk_names, columns=def_names)
    df['Mean'] = df.mean(axis=1)
    means_row = df.mean(axis=0)
    df.loc['Mean'] = means_row

    return df
