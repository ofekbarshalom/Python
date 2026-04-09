"""
Network graph for the SNAPT environment.
Wraps a list of devices with adjacency information and observation generation.
"""

import numpy as np
from typing import List, Tuple
from config import SecurityState
from environment.device import Device


class Network:
    def __init__(self, device_configs: List[Tuple], edges: List[Tuple[int, int]]):
        """
        Args:
            device_configs: list of (SecurityState, value, vuln_prob) per device
            edges: list of (i, j) undirected edges
        """
        self.device_configs = device_configs
        self.edges = edges
        self.num_devices = len(device_configs)
        self.devices = [Device(s, v, p) for s, v, p in device_configs]
        self.adjacency = self._build_adjacency()

    def _build_adjacency(self) -> dict:
        adj = {i: set() for i in range(self.num_devices)}
        for i, j in self.edges:
            adj[i].add(j)
            adj[j].add(i)
        return adj

    def reset(self):
        for d in self.devices:
            d.reset()

    def get_attackable_devices(self) -> List[int]:
        """
        Attacker can target devices that are Vulnerable,
        or connected to a Vulnerable device (lateral movement).
        """
        attackable = set()
        for i, device in enumerate(self.devices):
            if device.is_vulnerable:
                attackable.add(i)
                for neighbor in self.adjacency[i]:
                    attackable.add(neighbor)
        # Also include compromised devices' neighbors (for further lateral movement)
        for i, device in enumerate(self.devices):
            if device.is_compromised:
                for neighbor in self.adjacency[i]:
                    attackable.add(neighbor)
        # Remove already compromised devices (can't exploit further)
        attackable = {i for i in attackable if not self.devices[i].is_compromised}
        return sorted(attackable)

    def get_attacker_observation(self) -> np.ndarray:
        """
        One-hot encoding of each device's state.
        For N devices: vector of length 3*N.
        Order: [d0_S, d0_V, d0_C, d1_S, d1_V, d1_C, ...]
        """
        obs = []
        for device in self.devices:
            obs.extend([
                1.0 if device.state == SecurityState.SECURE else 0.0,
                1.0 if device.state == SecurityState.VULNERABLE else 0.0,
                1.0 if device.state == SecurityState.COMPROMISED else 0.0,
            ])
        return np.array(obs, dtype=np.float32)

    def get_defender_observation(self) -> np.ndarray:
        """
        Defender knows exploit probabilities and values.
        Vector of length 2*N: [p0, p1, ..., pN, v0, v1, ..., vN]
        """
        probs = [d.vuln_prob for d in self.devices]
        values = [d.value for d in self.devices]
        return np.array(probs + values, dtype=np.float32)

    def get_attacker_reward(self) -> float:
        """Sum of values of all compromised devices."""
        return sum(d.value for d in self.devices if d.is_compromised)

    def __repr__(self):
        return f"Network({self.devices})"
