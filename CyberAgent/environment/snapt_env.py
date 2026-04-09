"""
SNAPT (Simple Network APT) game environment.
Two-player alternating game between an Attacker and Defender.
"""

import numpy as np
from typing import Optional, Dict, List
from config import (
    PLAYER_MOVES, DETECT_PROB, PROB_DECREASE,
    WIN_THRESHOLD, DEFAULT_DEVICES, DEFAULT_EDGES, SecurityState
)
from environment.network import Network


class SNAPTEnv:
    def __init__(self, device_configs=None, edges=None):
        self.device_configs = device_configs or DEFAULT_DEVICES
        self.edges = edges or DEFAULT_EDGES
        self.network = Network(self.device_configs, self.edges)
        self.num_devices = self.network.num_devices
        self.attacker_action_size = self.num_devices  # attack device i
        self.defender_action_size = self.num_devices * 2  # detect i, secure i
        self.attacker_obs_size = self.num_devices * 3  # one-hot states
        self.defender_obs_size = self.num_devices * 2  # probs + values
        self.current_move = 0
        self.last_compromised_device: Optional[int] = None

    def reset(self):
        self.network.reset()
        self.current_move = 0
        self.last_compromised_device = None
        return self._get_observations()

    def _get_observations(self):
        return (
            self.network.get_attacker_observation(),
            self.network.get_defender_observation()
        )

    def get_valid_attacker_actions(self) -> List[int]:
        """Returns list of valid action indices for attacker."""
        attackable = self.network.get_attackable_devices()
        if not attackable:
            return list(range(self.num_devices))  # all valid if none attackable (no-op)
        return attackable

    def get_valid_defender_actions(self) -> List[int]:
        """All defender actions are always valid (may just have no effect)."""
        return list(range(self.defender_action_size))

    def step_attacker(self, action: int) -> bool:
        """
        Attacker selects a device to exploit.
        Returns True if the exploit succeeded.
        """
        self.last_compromised_device = None
        device = self.network.devices[action]

        # Can only exploit if device is attackable
        attackable = self.network.get_attackable_devices()
        if action not in attackable:
            self.current_move += 1
            return False

        success = device.attempt_exploit()
        if success and device.is_compromised:
            self.last_compromised_device = action
        self.current_move += 1
        return success

    def step_defender(self, action: int) -> bool:
        """
        Defender action: 0..N-1 = detect device i, N..2N-1 = secure device i.
        Returns True if the action had effect.
        """
        is_detect = action < self.num_devices
        device_idx = action if is_detect else action - self.num_devices
        device = self.network.devices[device_idx]
        self.current_move += 1

        if is_detect:
            # Detection only works on device compromised in the previous attacker turn
            if self.last_compromised_device == device_idx and device.is_compromised:
                return device.attempt_detect(DETECT_PROB)
            return False
        else:
            return device.secure(PROB_DECREASE)

    def is_done(self) -> bool:
        return self.current_move >= PLAYER_MOVES * 2

    def get_reward(self) -> float:
        return self.network.get_attacker_reward()

    def attacker_wins(self) -> bool:
        return self.get_reward() >= WIN_THRESHOLD

    def play_game(self, attacker_agent, defender_agent, collect_trajectory=False) -> Dict:
        """
        Play a full game. Returns result dict with reward, winner, and optional trajectories.
        """
        atk_obs, def_obs = self.reset()

        atk_trajectory = []  # (obs, action, log_prob, value)
        def_trajectory = []

        for turn in range(PLAYER_MOVES):
            # Attacker's turn
            valid_atk = self.get_valid_attacker_actions()
            atk_result = attacker_agent.select_action(atk_obs, valid_atk)
            if collect_trajectory:
                atk_trajectory.append((atk_obs.copy(), atk_result))
            self.step_attacker(atk_result['action'])

            # Defender's turn
            def_obs = self.network.get_defender_observation()
            valid_def = self.get_valid_defender_actions()
            def_result = defender_agent.select_action(def_obs, valid_def)
            if collect_trajectory:
                def_trajectory.append((def_obs.copy(), def_result))
            self.step_defender(def_result['action'])

            # Update observations
            atk_obs = self.network.get_attacker_observation()
            def_obs = self.network.get_defender_observation()

        reward = self.get_reward()
        return {
            'reward': reward,
            'attacker_wins': reward >= WIN_THRESHOLD,
            'atk_trajectory': atk_trajectory if collect_trajectory else None,
            'def_trajectory': def_trajectory if collect_trajectory else None,
        }
