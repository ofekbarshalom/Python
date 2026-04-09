"""
Main evaluation script: runs round-robin competition and generates visualizations.
Usage: python -m experiments.run_competition
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.a2c_trainer import A2CTrainer
from training.cem_trainer import CEMTrainer
from training.utils import set_seed
from agents.random_agent import RandomAgent
from evaluation.competition import run_competition
from visualization.competition_table import print_competition_table, format_competition_table
from visualization.heatmap import plot_action_heatmap
from visualization.training_curves import plot_training_curves, plot_comparison_curves
from config import SEED, TRAINING_ITERATIONS


def main():
    print("=" * 60)
    print("  SNAPT Evaluation: A2C vs CEM")
    print("=" * 60)

    os.makedirs("figures", exist_ok=True)

    # ── Train both algorithms ──
    print("\n[1/4] Training A2C...")
    set_seed(SEED)
    a2c_trainer = A2CTrainer()
    a2c_atk, a2c_def = a2c_trainer.train(num_iterations=TRAINING_ITERATIONS)

    print("\n[2/4] Training CEM...")
    set_seed(SEED)
    cem_trainer = CEMTrainer()
    cem_atk, cem_def = cem_trainer.train(num_iterations=TRAINING_ITERATIONS)

    # ── Random baselines ──
    random_atk = RandomAgent(action_size=3)
    random_def = RandomAgent(action_size=6)

    # ── Run competition ──
    print("\n[3/4] Running round-robin competition...")
    attackers = {'A2C': a2c_atk, 'CEM': cem_atk, 'Random': random_atk}
    defenders = {'A2C': a2c_def, 'CEM': cem_def, 'Random': random_def}

    results = run_competition(attackers, defenders)
    print_competition_table(results)

    # ── Generate visualizations ──
    print("\n[4/4] Generating visualizations...")

    # Competition table figure
    format_competition_table(results, save_path="figures/competition_table.png")

    # Action probability heatmap
    plot_action_heatmap(attackers, defenders, save_path="figures/action_heatmap.png")

    # Training curves
    plot_training_curves(
        {
            'A2C': a2c_trainer.logger.metrics.get('atk_reward', []),
            'CEM': cem_trainer.logger.metrics.get('mean_atk_reward', []),
        },
        title="Mean Attacker Reward During Training",
        save_path="figures/training_curves.png"
    )

    # Comparison curves (vs random and vs trained defender)
    plot_comparison_curves(
        a2c_trainer.logger.metrics,
        cem_trainer.logger.metrics,
        save_path="figures/eval_comparison.png"
    )

    print("\nAll figures saved to figures/")
    print("Done!")


if __name__ == "__main__":
    main()
