"""
Abstract base agent interface for SNAPT.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
import numpy as np


class BaseAgent(ABC):
    @abstractmethod
    def select_action(self, observation: np.ndarray, valid_actions: List[int]) -> Dict:
        """
        Select an action given an observation and list of valid actions.
        Returns dict with at least 'action' key.
        May also include 'log_prob' and 'value' for training.
        """
        pass

    def get_action_probs(self, observation: np.ndarray) -> np.ndarray:
        """Get raw action probabilities (for visualization)."""
        raise NotImplementedError
