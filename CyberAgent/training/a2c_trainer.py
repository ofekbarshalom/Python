"""
A2C coevolutionary training loop for SNAPT.
Trains attacker and defender simultaneously using Advantage Actor-Critic.
"""

import numpy as np
from tqdm import tqdm
from environment.snapt_env import SNAPTEnv
from agents.a2c_agent import A2CAgent
from agents.random_agent import RandomAgent
from training.utils import TrainingLogger
from config import (
    A2C_ROLLOUTS, A2C_VALUE_COEF, A2C_ENTROPY_COEF,
    TRAINING_ITERATIONS, EVAL_INTERVAL, EVAL_GAMES,
    DEFAULT_DEVICES, DEFAULT_EDGES
)


class A2CTrainer:
    def __init__(self, device_configs=None, edges=None):
        self.device_configs = device_configs or DEFAULT_DEVICES
        self.edges = edges or DEFAULT_EDGES
        self.env = SNAPTEnv(self.device_configs, self.edges)

        self.attacker = A2CAgent(self.env.attacker_obs_size, self.env.attacker_action_size)
        self.defender = A2CAgent(self.env.defender_obs_size, self.env.defender_action_size)
        self.logger = TrainingLogger()

    def train(self, num_iterations: int = TRAINING_ITERATIONS,
              rollouts_per_update: int = A2C_ROLLOUTS):
        """
        Coevolutionary A2C training.
        Each iteration: play rollouts_per_update games, accumulate gradients, update.
        """
        random_def = RandomAgent(self.env.defender_action_size)
        random_atk = RandomAgent(self.env.attacker_action_size)

        for iteration in tqdm(range(num_iterations), desc="A2C Training"):
            atk_rewards = []
            all_atk_trajectories = []
            all_def_trajectories = []
            all_rewards = []

            for _ in range(rollouts_per_update):
                result = self.env.play_game(
                    self.attacker, self.defender, collect_trajectory=True
                )
                atk_rewards.append(result['reward'])
                all_atk_trajectories.append(result['atk_trajectory'])
                all_def_trajectories.append(result['def_trajectory'])
                all_rewards.append(result['reward'])

            # Update attacker
            atk_loss = sum(
                self.attacker.compute_loss(traj, reward, A2C_VALUE_COEF, A2C_ENTROPY_COEF)
                for traj, reward in zip(all_atk_trajectories, all_rewards)
            ) / rollouts_per_update
            self.attacker.update(atk_loss)

            # Update defender (reward is negated for zero-sum)
            def_loss = sum(
                self.defender.compute_loss(traj, -reward, A2C_VALUE_COEF, A2C_ENTROPY_COEF)
                for traj, reward in zip(all_def_trajectories, all_rewards)
            ) / rollouts_per_update
            self.defender.update(def_loss)

            mean_reward = np.mean(atk_rewards)
            self.logger.log('atk_reward', mean_reward, iteration)
            self.logger.log('atk_loss', atk_loss.item(), iteration)

            # Periodic evaluation against random opponent
            if iteration % EVAL_INTERVAL == 0:
                eval_reward_vs_random = self._evaluate(self.attacker, random_def)
                eval_reward_vs_trained = self._evaluate(self.attacker, self.defender)
                random_vs_trained = self._evaluate(random_atk, self.defender)

                self.logger.log('eval_vs_random_def', eval_reward_vs_random, iteration)
                self.logger.log('eval_vs_trained_def', eval_reward_vs_trained, iteration)
                self.logger.log('random_vs_trained_def', random_vs_trained, iteration)

        return self.attacker, self.defender

    def _evaluate(self, attacker, defender, num_games: int = EVAL_GAMES) -> float:
        rewards = []
        for _ in range(num_games):
            result = self.env.play_game(attacker, defender)
            rewards.append(result['reward'])
        return np.mean(rewards)
