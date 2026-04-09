"""
Neural network architectures for SNAPT agents.
Feed-forward policy and value networks with 2 hidden layers (Figure 3).
"""

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from config import HIDDEN_SIZE


class PolicyNetwork(nn.Module):
    """Policy network: maps observation to action probabilities."""

    def __init__(self, input_size: int, output_size: int, hidden_size: int = HIDDEN_SIZE):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return F.softmax(self.fc3(x), dim=-1)

    def set_flat_params(self, flat_params: np.ndarray):
        """Load parameters from a flat vector."""
        idx = 0
        for p in self.parameters():
            size = p.numel()
            p.data = torch.tensor(
                flat_params[idx:idx + size].reshape(p.shape),
                dtype=torch.float32
            )
            idx += size

    def get_num_params(self) -> int:
        return sum(p.numel() for p in self.parameters())


class ValueNetwork(nn.Module):
    """Value network: maps observation to scalar value estimate."""

    def __init__(self, input_size: int, hidden_size: int = HIDDEN_SIZE):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
