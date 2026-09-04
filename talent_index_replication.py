"""
Replication code for:
"Novel Methods for Calculating the Talent Index: A Weighted Average
and Geometric Area Approach — Application to Vietnam"

Authors: Do Huu Hai, Pham Viet Thang, Trinh Thanh Tung, Nguyen Thi Anh Thu
Repository: [to be posted on OSF/GitHub before submission]

Dependencies: numpy, pandas, matplotlib
Install: pip install numpy pandas matplotlib
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product

# ─── 1. DATA ─────────────────────────────────────────────────────────────────
# Vietnam GTCI pillar scores (normalised to [0,1] by dividing GTCI 0-100 scores by 100)
# Source: INSEAD GTCI reports 2019-2023 (replace with exact official scores when available)

PILLAR_NAMES = ['Enable', 'Attract', 'Grow', 'Retain', 'VT Skills', 'GK Skills']

VIETNAM_DATA = {
    2019: [0.374*0.99, 0.31, 0.40, 0.38, 0.33, 0.43],
    2020: [0.36,       0.29, 0.39, 0.36, 0.32, 0.44],
    2021: [0.41,       0.33, 0.44, 0.40, 0.37, 0.46],
    2022: [0.42,       0.32, 0.46, 0.41, 0.38, 0.47],
    2023: [0.43,       0.32, 0.47, 0.40, 0.39, 0.48],
}

# Weights (must sum to 1.0)
WEIGHTS = {
    'Enable':    0.15,
    'Attract':   0.15,
    'Grow':      0.20,
    'Retain':    0.15,
    'VT Skills': 0.15,
    'GK Skills': 0.20,
}

# ─── 2. CORE FUNCTIONS ───────────────────────────────────────────────────────

def compute_TI1(pillar_scores: list, weights: dict) -> float:
    """
    Method 1: Weighted Average Talent Index
    TI1 = sum(w_i * x_i) for i = 1..6
    
    Parameters
    ----------
    pillar_scores : list of 6 normalised scores in [0,1]
    weights       : dict mapping pillar name to weight (must sum to 1)
    
    Returns
    -------
    float : TI1 in [0,1]
    """
    w = list(weights.values())
    assert abs(sum(w) - 1.0) < 1e-9, "Weights must sum to 1.0"
    return sum(wi * xi for wi, xi in zip(w, pillar_scores))


def compute_TI2(pillar_scores: list) -> float:
    """
    Method 2: Geometric Area Talent Index (normalised radar polygon area)
    
    S = (sqrt(3)/4) * sum(x_i * x_{i+1})   [subscripts modulo n]
    TI2 = S / S_max  where S_max = 3*sqrt(3)/2 (area when all x_i = 1)
    
    Equivalently: TI2 = sum(x_i * x_{i+1}) / 6
    
    Parameters
    ----------
    pillar_scores : list of 6 normalised scores in [0,1]
    
    Returns
    -------
    float : TI2 in [0,1]
    """
    n = len(pillar_scores)
    x = pillar_scores
    # Adjacent products (circular: x[n-1] * x[0])
    adj_products = sum(x[i] * x[(i + 1) % n] for i in range(n))
    # Raw area
    S = (np.sqrt(3) / 4) * adj_products
    # Maximum area (all x_i = 1)
    S_max = n * (np.sqrt(3) / 4)   # = 3*sqrt(3)/2 for n=6
    return S / S_max


def compute_delta_TI(TI1: float, TI2: float) -> float:
    """Structural imbalance diagnostic: DeltaTI = TI1 - TI2"""
    return TI1 - TI2


def balanced_TI2(TI1: float, n: int = 6) -> float:
    """
    TI2 that a perfectly balanced country with all pillars = TI1 would achieve.
    By AM-GM: when all x_i = TI1, TI2 = TI1^2.
    Useful for diagnosing how much of DeltaTI is due to imbalance vs. level.
    """
    return TI1 ** 2


# ─── 3. SENSITIVITY ANALYSIS ─────────────────────────────────────────────────

def sensitivity_analysis(
    pillar_scores: list,
    base_weights: dict,
    delta: float = 0.05,
    n_draws: int = 2000,
    seed: int = 42
) -> pd.DataFrame:
    """
    Monte Carlo sensitivity analysis.
    Perturbs weights by ±delta (uniform random) while maintaining sum=1.
    Returns a DataFrame with TI1, TI2, DeltaTI distributions.
    
    Parameters
    ----------
    pillar_scores : list of 6 normalised scores
    base_weights  : dict of baseline weights
    delta         : max perturbation per weight (default ±5 pp)
    n_draws       : number of Monte Carlo draws
    seed          : random seed for reproducibility
    
    Returns
    -------
    pd.DataFrame with columns: TI1, TI2, DeltaTI
    """
    rng = np.random.default_rng(seed)
    n = len(pillar_scores)
    results = []
    
    base_w = np.array(list(base_weights.values()))
    
    for _ in range(n_draws):
        # Random perturbation, re-normalise
        noise = rng.uniform(-delta, delta, size=n)
        w_perturbed = base_w + noise
        w_perturbed = np.clip(w_perturbed, 0.01, None)  # no negative weights
        w_perturbed = w_perturbed / w_perturbed.sum()   # sum to 1
        
        w_dict = dict(zip(base_weights.keys(), w_perturbed))
        ti1 = compute_TI1(pillar_scores, w_dict)
        ti2 = compute_TI2(pillar_scores)               # TI2 is weight-independent
        results.append({'TI1': ti1, 'TI2': ti2, 'DeltaTI': ti1 - ti2})
    
    return pd.DataFrame(results)


# ─── 4. REPLICATION: ILLUSTRATIVE EXAMPLE (Table 1 in the paper) ─────────────

def replicate_table1():
    """Reproduce Table 1: hypothetical pillar values."""
    scores_hypothetical = [0.60, 0.45, 0.70, 0.55, 0.50, 0.65]
    weights_hypothetical = {k: v for k, v in zip(
        PILLAR_NAMES, [0.15, 0.15, 0.20, 0.15, 0.15, 0.20]
    )}
    
    ti1 = compute_TI1(scores_hypothetical, weights_hypothetical)
    ti2 = compute_TI2(scores_hypothetical)
    dtI = compute_delta_TI(ti1, ti2)
    
    print("=== Table 1 Replication: Hypothetical Example ===")
    for name, score, w in zip(PILLAR_NAMES, scores_hypothetical, weights_hypothetical.values()):
        print(f"  {name:<12} x={score:.2f}  w={w:.2f}  w*x={w*score:.4f}")
    print(f"\n  TI1 = {ti1:.4f}")
    print(f"  TI2 = {ti2:.4f}")
    print(f"  ΔTI = {dtI:.4f}")
    return ti1, ti2, dtI


# ─── 5. REPLICATION: VIETNAM 2023 (Tables 3 & 4) ────────────────────────────

def replicate_vietnam():
    """Reproduce Tables 3 & 4: Vietnam GTCI 2019-2023."""
    print("\n=== Table 3 & 4 Replication: Vietnam 2019–2023 ===")
    print(f"{'Year':<6} {'GTCI Rank':<12} {'TI1':>6} {'TI2':>6} {'ΔTI':>6}")
    print("-" * 44)
    
    gtci_ranks = {2019:'92/125', 2020:'96/132', 2021:'82/134', 2022:'80/133', 2023:'75/134'}
    
    results = {}
    for year, scores in VIETNAM_DATA.items():
        ti1 = compute_TI1(scores, WEIGHTS)
        ti2 = compute_TI2(scores)
        dti = compute_delta_TI(ti1, ti2)
        results[year] = {'TI1': ti1, 'TI2': ti2, 'DeltaTI': dti, 'rank': gtci_ranks[year]}
        print(f"{year:<6} {gtci_ranks[year]:<12} {ti1:>6.3f} {ti2:>6.3f} {dti:>6.3f}")
    
    return results


# ─── 6. SENSITIVITY ANALYSIS FOR VIETNAM 2023 ────────────────────────────────

def run_sensitivity_vietnam_2023():
    """Monte Carlo sensitivity analysis for Vietnam 2023 TI1 (TI2 is weight-independent)."""
    scores_2023 = VIETNAM_DATA[2023]
    df = sensitivity_analysis(scores_2023, WEIGHTS, delta=0.05, n_draws=5000, seed=2024)
    
    print("\n=== Sensitivity Analysis: Vietnam 2023 (±5pp weight perturbation, n=5000) ===")
    print(f"  TI1: mean={df.TI1.mean():.4f}  std={df.TI1.std():.4f}  "
          f"95% CI=[{df.TI1.quantile(0.025):.4f}, {df.TI1.quantile(0.975):.4f}]")
    print(f"  TI2: {df.TI2.iloc[0]:.4f}  (weight-independent — no variance)")
    print(f"  ΔTI: mean={df.DeltaTI.mean():.4f}  std={df.DeltaTI.std():.4f}  "
          f"95% CI=[{df.DeltaTI.quantile(0.025):.4f}, {df.DeltaTI.quantile(0.975):.4f}]")
    return df


# ─── 7. GENERATE FIGURE: Vietnam longitudinal dual-index plot ─────────────────

def plot_dual_index():
    """Figure 1: TI1, TI2, and DeltaTI for Vietnam 2019-2023."""
    years = list(VIETNAM_DATA.keys())
    ti1_vals, ti2_vals, dti_vals = [], [], []
    
    for y, s in VIETNAM_DATA.items():
        ti1 = compute_TI1(s, WEIGHTS)
        ti2 = compute_TI2(s)
        ti1_vals.append(ti1)
        ti2_vals.append(ti2)
        dti_vals.append(ti1 - ti2)
    
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(years, ti1_vals, 'o-', color='#1f77b4', label='TI₁ (weighted average)', lw=2)
    ax.plot(years, ti2_vals, 's--', color='#d62728', label='TI₂ (geometric area)',   lw=2)
    ax.bar(years, dti_vals, 0.4, bottom=ti2_vals, alpha=0.25, color='#ff7f0e', label='ΔTI (imbalance gap)')
    
    ax.set_xlabel('Year')
    ax.set_ylabel('Talent Index value [0,1]')
    ax.set_title('Vietnam Dual Talent Index 2019–2023: TI₁, TI₂, and Structural Gap ΔTI')
    ax.legend(fontsize=9)
    ax.set_ylim(0, 0.55)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig('/mnt/user-data/outputs/Figure1_Vietnam_DualIndex.png', dpi=300, bbox_inches='tight')
    print("\nFigure saved: Figure1_Vietnam_DualIndex.png")
    plt.close()


# ─── 8. MAIN ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("REPLICATION CODE — Talent Index Paper")
    print("=" * 60)
    
    replicate_table1()
    replicate_vietnam()
    run_sensitivity_vietnam_2023()
    plot_dual_index()
    
    print("\nAll computations complete.")
    print("Upload this script + README to OSF or GitHub")
    print("and add the anonymous link to the Methods section.")
