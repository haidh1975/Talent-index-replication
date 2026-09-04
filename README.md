# Talent Index Replication Package

> **Manuscript under review** — authors and journal details will be updated upon acceptance.
>
> Working title: *"Novel Methods for Calculating the Talent Index: A Weighted Average and Geometric Area Approach — Application to Vietnam"*

---

## Overview

This repository contains the complete replication package for the paper.  
All data processing, index calculations, sensitivity analyses, and figure generation are
implemented in a single, self-contained Python script that requires no proprietary software.

---

## Repository Contents

| File | Description |
|------|-------------|
| `talent_index_replication.py` | Main replication script — all results, tables, and figures |
| `requirements.txt` | Python package dependencies (pip-installable) |
| `README.md` | This file |
| `LICENSE` | MIT open-source licence |

---

## Quick Start

### 1 — Install dependencies

```bash
pip install -r requirements.txt
```

Python **3.9 or higher** is required.

### 2 — Run the replication script

```bash
python talent_index_replication.py
```

**Expected output (terminal):**

```
============================================================
REPLICATION CODE — Talent Index Paper
============================================================
=== Table 1 Replication: Hypothetical Example ===
  Enable       x=0.60  w=0.15  w*x=0.0900
  ...
  TI1 = 0.5850 | TI2 = 0.3267 | ΔTI = 0.2583

=== Table 3 & 4 Replication: Vietnam 2019–2023 ===
Year   GTCI Rank     TI1    TI2    ΔTI
2019   92/125      0.375  0.136  0.239
...
2023   75/134      0.421  0.171  0.250

=== Sensitivity Analysis: Vietnam 2023 (±5pp, n=5000) ===
  TI1: mean=0.4209  std=0.0038  95% CI=[0.4138, 0.4285]
  TI2: 0.1709  (weight-independent)
  ΔTI: mean=0.2500  std=0.0038  95% CI=[0.2427, 0.2575]

Figure saved: Figure1_Vietnam_DualIndex.png
Figure saved: Figure2_MonteCarlo_Sensitivity.png
All computations complete.
```

**Generated output files** (in the same directory):

| File | Corresponds to |
|------|----------------|
| `Figure1_Vietnam_DualIndex.png` | Figure 1 in the paper |
| `Figure2_MonteCarlo_Sensitivity.png` | Figure 2 in the paper |

---

## Replication Details

### Methods implemented

| Function | Description |
|----------|-------------|
| `compute_TI1(scores, weights)` | Weighted average Talent Index: TI₁ = Σ wᵢxᵢ |
| `compute_TI2(scores)` | Geometric area Talent Index: TI₂ = Σ xᵢxᵢ₊₁ / 6 |
| `compute_delta_TI(TI1, TI2)` | Structural imbalance gap: ΔTI = TI₁ − TI₂ |
| `balanced_TI2(TI1)` | AM-GM baseline: TI₂ for a perfectly balanced profile with mean = TI₁ |
| `sensitivity_analysis(...)` | Monte Carlo sensitivity: 5,000 iterations, ±5 pp weight perturbation |

### Mathematical formulas

**TI₁ (weighted average):**
```
TI₁ = Σᵢ₌₁⁶ wᵢ xᵢ,   where Σ wᵢ = 1, wᵢ > 0
```

**TI₂ (geometric area, normalised):**
```
S    = (√3/4) Σᵢ₌₁⁶ xᵢ xᵢ₊₁     (subscripts modulo 6)
S_max = 3√3/2 ≈ 2.598             (area when all xᵢ = 1)
TI₂  = S / S_max = Σ xᵢ xᵢ₊₁ / 6
```

**Diagnostic gap:**
```
ΔTI = TI₁ − TI₂
```

### Data sources

Pillar score estimates are derived from publicly available GTCI annual reports
(INSEAD, 2019–2023). To replicate with exact official scores, obtain the GTCI
panel dataset directly from INSEAD and update the `VIETNAM_DATA` dictionary
in `talent_index_replication.py`.

---

## Pillar Definitions (GTCI Six-Pillar Framework)

| Pillar | Code | Description |
|--------|------|-------------|
| Enable | x₁ | Regulatory, market, and labour environment |
| Attract | x₂ | Openness to domestic and foreign talent |
| Grow | x₃ | Education and lifelong learning |
| Retain | x₄ | Quality of life and career opportunities |
| VT Skills | x₅ | Vocational and technical competencies |
| GK Skills | x₆ | Global knowledge and professional skills |

Source: Lanvin & Monteiro (2023); Saisana et al. (2023).

---

## Dependencies

| Package | Version tested | Purpose |
|---------|---------------|---------|
| `numpy` | ≥ 1.21 | Numerical computation |
| `pandas` | ≥ 1.3 | Data manipulation |
| `matplotlib` | ≥ 3.4 | Figure generation |

---

## Citation

If you use this replication package, please cite the paper:

```bibtex
@article{[citation_to_be_added],
  title   = {Novel Methods for Calculating the Talent Index:
             A Weighted Average and Geometric Area Approach — Application to Vietnam},
  journal = {[journal_to_be_confirmed]},
  year    = {2025},
  note    = {Under review}
}
```

---

## Licence

This replication package is released under the **MIT Licence**.
See the `LICENSE` file for details.

---

## Contact

For queries related to this replication package, please open an issue on this
repository. Author contact information will be added upon manuscript acceptance.
