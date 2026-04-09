"""
Competition results table visualization.
Formats results like Table 7 from the paper.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def format_competition_table(df: pd.DataFrame, title: str = "SNAPT Competition Results",
                             save_path: str = None):
    """
    Display competition results as a formatted table figure.

    Args:
        df: DataFrame from competition.run_competition()
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    # Create table
    cell_text = []
    for idx in df.index:
        row = []
        for col in df.columns:
            val = df.loc[idx, col]
            row.append(f"{val:.1f}")
        cell_text.append(row)

    table = ax.table(
        cellText=cell_text,
        rowLabels=list(df.index),
        colLabels=list(df.columns),
        cellLoc='center',
        loc='center',
    )
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1.2, 1.5)

    # Style header
    for j in range(len(df.columns)):
        table[(0, j)].set_facecolor('#4a90d9')
        table[(0, j)].set_text_props(color='white', fontweight='bold')
    for i in range(len(df.index)):
        table[(i + 1, -1)].set_facecolor('#d4e6f1')

    # Bold best attacker in each column, underline best defender in each row
    data_df = df.drop('Mean', axis=0).drop('Mean', axis=1) if 'Mean' in df.index else df
    for j, col in enumerate(data_df.columns):
        best_idx = data_df[col].idxmax()
        row_pos = list(df.index).index(best_idx) + 1
        table[(row_pos, j)].set_text_props(fontweight='bold')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()


def print_competition_table(df: pd.DataFrame, title: str = "SNAPT Competition Results"):
    """Print competition results as formatted text."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")
    print(f"\nAttacker wins out of 100 games. Rows = Attackers, Cols = Defenders.\n")
    print(df.to_string(float_format=lambda x: f"{x:.1f}"))
    print()
