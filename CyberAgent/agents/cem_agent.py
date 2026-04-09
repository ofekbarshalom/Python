"""
Cross-Entropy Method (CEM) agent for SNAPT.
Evolutionary Strategy approach - gradient-free optimization.
"""

import numpy as np
import torch
from typing import List, Dict
from agents.base_agent import BaseAgent
from agents.networks import PolicyNetwork
from config import CEM_N, CEM_K, CEM_EPSILON


class CEMAgent(BaseAgent):
    """
    CEM maintains a Gaussian distribution over policy network weights.
    During evaluation, uses the current mean as the policy.
    During training, samples N policies and updates toward the best K.
    """

    def __init__(self, obs_size: int, action_size: int,
                 n: int = CEM_N, k: int = CEM_K, epsilon: float = CEM_EPSILON):
        self.obs_size = obs_size
        self.action_size = action_size
        self.n = n
        self.k = k
        self.epsilon = epsilon

        # Reference network to determine parameter count
        self.policy = PolicyNetwork(obs_size, action_size)
        self.num_params = self.policy.get_num_params()

        # Distribution parameters (diagonal Gaussian)
        self.mu = np.zeros(self.num_params, dtype=np.float32)
        self.sigma_sq = np.ones(self.num_params, dtype=np.float32)

        # Load mean into policy network
        self.policy.set_flat_params(self.mu)

        # Precompute CEM lambda weights (Eq. 5)
        # lambda_i = 1 / (i * H_K) where H_K is K-th harmonic number
        h_k = sum(1.0 / j for j in range(1, k + 1))
        self.lambdas = np.array([1.0 / (i * h_k) for i in range(1, k + 1)], dtype=np.float32)

    def select_action(self, observation: np.ndarray, valid_actions: List[int]) -> Dict:
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            probs = self.policy(obs_tensor).squeeze(0).numpy()

        # Mask invalid actions
        mask = np.zeros(self.action_size)
        for a in valid_actions:
            mask[a] = 1.0
        masked_probs = probs * mask
        prob_sum = masked_probs.sum()
        if prob_sum > 0:
            masked_probs = masked_probs / prob_sum
        else:
            masked_probs = mask / mask.sum()

        action = np.random.choice(self.action_size, p=masked_probs)
        return {'action': action, 'probs': masked_probs}

    def sample_population(self) -> List[np.ndarray]:
        """Sample N weight vectors from the current distribution."""
        samples = []
        for _ in range(self.n):
            sample = np.random.normal(self.mu, np.sqrt(self.sigma_sq))
            samples.append(sample.astype(np.float32))
        return samples

    def create_agent_from_params(self, params: np.ndarray) -> 'CEMAgent':
        """Create a copy of this agent with specific parameters loaded."""
        agent = CEMAgent.__new__(CEMAgent)
        agent.obs_size = self.obs_size
        agent.action_size = self.action_size
        agent.n = self.n
        agent.k = self.k
        agent.epsilon = self.epsilon
        agent.num_params = self.num_params
        agent.mu = self.mu.copy()
        agent.sigma_sq = self.sigma_sq.copy()
        agent.lambdas = self.lambdas.copy()
        agent.policy = PolicyNetwork(self.obs_size, self.action_size)
        agent.policy.set_flat_params(params)
        return agent

    def update_distribution(self, elite_params: List[np.ndarray]):
        """
        Update mu and sigma_sq toward the elite samples (Eq. 5).
        elite_params should be sorted best-first.
        """
        k = len(elite_params)
        new_mu = np.zeros_like(self.mu)
        new_sigma_sq = np.zeros_like(self.sigma_sq)

        for i, params in enumerate(elite_params):
            new_mu += self.lambdas[i] * params
            new_sigma_sq += self.lambdas[i] * (params - self.mu) ** 2

        self.mu = new_mu
        self.sigma_sq = new_sigma_sq + self.epsilon

        # Update the policy network with new mean
        self.policy.set_flat_params(self.mu)

    def get_action_probs(self, observation: np.ndarray) -> np.ndarray:
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            probs = self.policy(obs_tensor).squeeze(0)
        return probs.numpy()
