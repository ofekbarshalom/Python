"""
Advantage Actor-Critic (A2C) agent for SNAPT.
Deep Reinforcement Learning approach using gradient descent.
"""

import numpy as np
import torch
import torch.optim as optim
from typing import List, Dict
from agents.base_agent import BaseAgent
from agents.networks import PolicyNetwork, ValueNetwork
from config import A2C_LR


class A2CAgent(BaseAgent):
    def __init__(self, obs_size: int, action_size: int, lr: float = A2C_LR):
        self.obs_size = obs_size
        self.action_size = action_size
        self.policy = PolicyNetwork(obs_size, action_size)
        self.value = ValueNetwork(obs_size)
        self.optimizer = optim.Adam(
            list(self.policy.parameters()) + list(self.value.parameters()),
            lr=lr
        )

    def select_action(self, observation: np.ndarray, valid_actions: List[int]) -> Dict:
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            probs = self.policy(obs_tensor).squeeze(0)
            val = self.value(obs_tensor).squeeze(0)

        # Mask invalid actions
        mask = torch.zeros(self.action_size)
        for a in valid_actions:
            mask[a] = 1.0
        masked_probs = probs * mask
        prob_sum = masked_probs.sum()
        if prob_sum > 0:
            masked_probs = masked_probs / prob_sum
        else:
            masked_probs = mask / mask.sum()

        dist = torch.distributions.Categorical(masked_probs)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        return {
            'action': action.item(),
            'log_prob': log_prob,
            'value': val,
            'probs': masked_probs.detach().numpy(),
        }

    def compute_loss(self, trajectories: List, final_reward: float,
                     value_coef: float = 0.5, entropy_coef: float = 0.01):
        """
        Compute A2C loss from a game trajectory.
        Terminal reward only: all steps get the same return.
        """
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy = 0.0

        for obs, result in trajectories:
            obs_tensor = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
            probs = self.policy(obs_tensor).squeeze(0)
            val = self.value(obs_tensor).squeeze(0)

            # Recompute log_prob for the chosen action
            action = result['action']
            dist = torch.distributions.Categorical(probs)
            log_prob = dist.log_prob(torch.tensor(action))

            advantage = final_reward - val.detach()
            total_policy_loss -= log_prob * advantage
            total_value_loss += (val - final_reward) ** 2
            total_entropy -= dist.entropy()

        n = max(len(trajectories), 1)
        loss = (total_policy_loss / n
                + value_coef * total_value_loss / n
                + entropy_coef * total_entropy / n)
        return loss

    def update(self, loss: torch.Tensor):
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            list(self.policy.parameters()) + list(self.value.parameters()), 0.5
        )
        self.optimizer.step()

    def get_action_probs(self, observation: np.ndarray) -> np.ndarray:
        obs_tensor = torch.tensor(observation, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            probs = self.policy(obs_tensor).squeeze(0)
        return probs.numpy()
