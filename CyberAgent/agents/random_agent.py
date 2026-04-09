"""
Random baseline agent - selects uniformly from valid actions.
"""

import numpy as np
from typing import List, Dict
from agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, action_size: int):
        self.action_size = action_size

    def select_action(self, observation: np.ndarray, valid_actions: List[int]) -> Dict:
        action = np.random.choice(valid_actions)
        return {'action': action}

    def get_action_probs(self, observation: np.ndarray) -> np.ndarray:
        probs = np.ones(self.action_size) / self.action_size
        return probs
