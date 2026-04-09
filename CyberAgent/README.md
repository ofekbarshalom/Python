# RedAI — Adversarial Agent-Learning in SNAPT

Reproduction and extension of Shashkov et al. (2023), *"Adversarial Agent-Learning for Cybersecurity: A Comparison of Algorithms"*. We implement **A2C** (deep reinforcement learning) and **CEM** (evolutionary strategy) agents on the **SNAPT** environment - a simplified network APT threat model, and compare them as both attackers and defenders across multiple network topologies.

Course project: *Advanced Topics in Cyber Defense*, Ariel University.
Authors: Ofek Bar Shalom, Meir Shuker.

## Key Findings

- **A2C** produces stronger attackers.
- **CEM** trains more robust defenders on the original 3-node chain.
- As network connectivity grows (Star-4, Ring-5), both algorithms approach near-perfect attack performance and CEM's defensive advantage diminishes.

See [paper/paper.pdf](paper/paper.pdf) for the full write-up.

## Repository Structure

```
RedAI/
├── config.py             # Hyperparameters & environment config
├── requirements.txt
├── agents/               # A2C, CEM, Random agents + networks
├── environment/          # SNAPT env, network, device models
├── training/             # A2C and CEM trainers
├── evaluation/           # Round-robin competition & metrics
├── experiments/          # Entry-point scripts
├── visualization/        # Training curves, heatmaps, tables
├── results/              # Training logs (JSON)
├── checkpoints/          # Saved model weights
├── paper/                # LaTeX source + compiled PDF
└── presentation/
```

## Installation

```bash
pip install -r requirements.txt
```

Requires Python 3.9+ with PyTorch 2.0+.

## Usage

Run the full A2C vs. CEM round-robin competition on the default 3-node chain:

```bash
python -m experiments.run_competition
```

Run the scaling extension on Star-4 and Ring-5 topologies:

```bash
python -m experiments.run_extension
```

Figures are written to `figures/` and training logs to `results/`.

## Configuration

All hyperparameters: SNAPT environment parameters, A2C/CEM settings, training iterations, and topology definitions are live in [config.py](config.py) and mirror Table 4 of the original paper.

## References

- Shashkov et al., *Adversarial Agent-Learning for Cybersecurity* (2023).
- Huang & Zhu, APT modeling (2020).
