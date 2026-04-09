"""
Device representation for the SNAPT environment.
Each device has a security state, value, and vulnerability probability.
"""

import random
from config import SecurityState, MAX_SECURES, PROB_DECREASE


class Device:
    def __init__(self, initial_state: SecurityState, value: float, vuln_prob: float):
        self.initial_state = initial_state
        self.initial_value = value
        self.initial_vuln_prob = vuln_prob
        self.state = initial_state
        self.value = value
        self.vuln_prob = vuln_prob
        self.times_secured = 0

    def reset(self):
        self.state = self.initial_state
        self.value = self.initial_value
        self.vuln_prob = self.initial_vuln_prob
        self.times_secured = 0

    def attempt_exploit(self) -> bool:
        """Attempt to exploit this device. Returns True if successful."""
        if random.random() < self.vuln_prob:
            self.escalate_state()
            return True
        return False

    def escalate_state(self):
        """S -> V -> C (one step per successful exploit)."""
        if self.state == SecurityState.SECURE:
            self.state = SecurityState.VULNERABLE
        elif self.state == SecurityState.VULNERABLE:
            self.state = SecurityState.COMPROMISED

    def attempt_detect(self, p_d: float) -> bool:
        """Attempt detection. Returns True if successful."""
        if random.random() < p_d:
            self.revert_state()
            return True
        return False

    def revert_state(self):
        """Revert: C -> V (detection rolls back one level)."""
        if self.state == SecurityState.COMPROMISED:
            self.state = SecurityState.VULNERABLE

    def secure(self, delta_s: float) -> bool:
        """Reduce vulnerability probability. Returns False if already at max secures."""
        if self.times_secured >= MAX_SECURES:
            return False
        self.vuln_prob = max(0.0, self.vuln_prob - delta_s)
        self.times_secured += 1
        return True

    @property
    def is_compromised(self) -> bool:
        return self.state == SecurityState.COMPROMISED

    @property
    def is_vulnerable(self) -> bool:
        return self.state == SecurityState.VULNERABLE

    @property
    def is_secure(self) -> bool:
        return self.state == SecurityState.SECURE

    def __repr__(self):
        return f"Device({self.state.value}, v={self.value}, p={self.vuln_prob:.2f})"
