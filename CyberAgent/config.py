"""
Configuration and hyperparameters for SNAPT environment and algorithms.
Based on Table 4 from Shashkov et al. (2023).
"""

from enum import Enum

# ── Device Security States ──
class SecurityState(Enum):
    SECURE = "S"
    VULNERABLE = "V"
    COMPROMISED = "C"

# ── SNAPT Environment Parameters ──
PLAYER_MOVES = 20
TOTAL_MOVES = 40
EXPLOIT_PROB = 0.7       # p_e: base exploit probability
DETECT_PROB = 0.7        # p_d: detection success probability
PROB_DECREASE = 0.1      # δ_s: securing reduces vuln_prob by this amount
MAX_SECURES = 3          # max times a device can be secured
WIN_THRESHOLD = 1.0      # attacker wins if reward >= this

# ── Default 3-Node Network (Figure 1) ──
# Each device: (initial_state, value, vulnerability_probability)
DEFAULT_DEVICES = [
    (SecurityState.VULNERABLE, 0, 0.5),  # d0: internet-facing
    (SecurityState.SECURE, 0, 0.5),       # d1: internal
    (SecurityState.SECURE, 1, 0.5),       # d2: target (has value)
]
DEFAULT_EDGES = [(0, 1), (1, 2)]  # linear chain

# ── Neural Network Architecture ──
HIDDEN_SIZE = 64
NUM_HIDDEN_LAYERS = 2

# ── A2C Hyperparameters (Table 4) ──
A2C_LR = 0.001           # Adam learning rate
A2C_GAMMA = 0.99         # discount factor
A2C_ROLLOUTS = 10        # games per update batch (G)
A2C_VALUE_COEF = 0.5     # value loss weight
A2C_ENTROPY_COEF = 0.01  # entropy bonus weight

# ── CEM Hyperparameters (Table 4) ──
CEM_N = 8                # population size
CEM_K = 4                # elite size
CEM_G = 1                # competitions per pairing
CEM_EPSILON = 1e-6       # variance floor

# ── Training ──
TRAINING_ITERATIONS = 2000
EVAL_INTERVAL = 100       # evaluate every N iterations
EVAL_GAMES = 20           # games per evaluation
SEED = 42

# ── Evaluation ──
COMPETITION_GAMES = 100   # games per matchup in final evaluation

# ── Extension: Additional Topologies ──
STAR_4_DEVICES = [
    (SecurityState.VULNERABLE, 0, 0.5),  # hub
    (SecurityState.SECURE, 0.5, 0.5),
    (SecurityState.SECURE, 0.5, 0.5),
    (SecurityState.SECURE, 1, 0.5),
]
STAR_4_EDGES = [(0, 1), (0, 2), (0, 3)]

RING_5_DEVICES = [
    (SecurityState.VULNERABLE, 0, 0.5),
    (SecurityState.SECURE, 0.3, 0.5),
    (SecurityState.SECURE, 0.5, 0.5),
    (SecurityState.SECURE, 0.7, 0.5),
    (SecurityState.SECURE, 1, 0.5),
]
RING_5_EDGES = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
