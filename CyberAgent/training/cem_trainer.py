"""
CEM (Cross-Entropy Method) coevolutionary training loop for SNAPT.
Trains attacker and defender using population-based evolutionary strategy.
"""

import numpy as np
from tqdm import tqdm
from environment.snapt_env import SNAPTEnv
from agents.cem_agent import CEMAgent
from agents.random_agent import RandomAgent
from training.utils import TrainingLogger
from config import (
    CEM_N, CEM_K, CEM_G, TRAINING_ITERATIONS, EVAL_INTERVAL, EVAL_GAMES,
    DEFAULT_DEVICES, DEFAULT_EDGES
)


class CEMTrainer:
    def __init__(self, device_configs=None, edges=None):
        self.device_configs = device_configs or DEFAULT_DEVICES
        self.edges = edges or DEFAULT_EDGES
        self.env = SNAPTEnv(self.device_configs, self.edges)

        self.attacker = CEMAgent(self.env.attacker_obs_size, self.env.attacker_action_size)
        self.defender = CEMAgent(self.env.defender_obs_size, self.env.defender_action_size)
        self.logger = TrainingLogger()

    def train(self, num_iterations: int = TRAINING_ITERATIONS):
        """
        CEM coevolutionary training.
        Each iteration:
        1. Sample N attacker and N defender weight vectors
        2. Play all NxN pairings (G games each)
        3. Rank and select top K elites
        4. Update distributions toward elites
        """
        random_def = RandomAgent(self.env.defender_action_size)
        random_atk = RandomAgent(self.env.attacker_action_size)

        for iteration in tqdm(range(num_iterations), desc="CEM Training"):
            # Sample populations
            atk_samples = self.attacker.sample_population()
            def_samples = self.defender.sample_population()

            # Create agents for each sample
            atk_agents = [self.attacker.create_agent_from_params(p) for p in atk_samples]
            def_agents = [self.defender.create_agent_from_params(p) for p in def_samples]

            # Play all pairings: reward_matrix[i][j] = attacker i's reward vs defender j
            reward_matrix = np.zeros((CEM_N, CEM_N))
            for i, atk_agent in enumerate(atk_agents):
                for j, def_agent in enumerate(def_agents):
                    total_reward = 0.0
                    for _ in range(CEM_G):
                        result = self.env.play_game(atk_agent, def_agent)
                        total_reward += result['reward']
                    reward_matrix[i][j] = total_reward / CEM_G

            # Rank attackers by mean reward (descending = best attacker first)
            atk_mean_rewards = reward_matrix.mean(axis=1)
            atk_ranking = np.argsort(-atk_mean_rewards)
            atk_elites = [atk_samples[idx] for idx in atk_ranking[:CEM_K]]

            # Rank defenders by mean reward they allowed (ascending = best defender first)
            def_mean_rewards = reward_matrix.mean(axis=0)
            def_ranking = np.argsort(def_mean_rewards)
            def_elites = [def_samples[idx] for idx in def_ranking[:CEM_K]]

            # Update distributions
            self.attacker.update_distribution(atk_elites)
            self.defender.update_distribution(def_elites)

            # Log
            best_atk_reward = atk_mean_rewards[atk_ranking[0]]
            mean_atk_reward = atk_mean_rewards.mean()
            self.logger.log('best_atk_reward', best_atk_reward, iteration)
            self.logger.log('mean_atk_reward', mean_atk_reward, iteration)

            # Periodic evaluation
            if iteration % EVAL_INTERVAL == 0:
                eval_vs_random = self._evaluate(self.attacker, random_def)
                eval_vs_trained = self._evaluate(self.attacker, self.defender)
                random_vs_trained = self._evaluate(random_atk, self.defender)

                self.logger.log('eval_vs_random_def', eval_vs_random, iteration)
                self.logger.log('eval_vs_trained_def', eval_vs_trained, iteration)
                self.logger.log('random_vs_trained_def', random_vs_trained, iteration)

        return self.attacker, self.defender

    def _evaluate(self, attacker, defender, num_games: int = EVAL_GAMES) -> float:
        rewards = []
        for _ in range(num_games):
            result = self.env.play_game(attacker, defender)
            rewards.append(result['reward'])
        return np.mean(rewards)
