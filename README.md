# Blockchain-Based Audio-Visual Content Authentication System

## PRISM â€” 5-Pillar Deepfake Detection with Blockchain Provenance

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org)
[![Dataset](https://img.shields.io/badge/Dataset-LAV--DF-orange.svg)](https://www.kaggle.com/datasets/elin75/localized-audio-visual-deepfake-dataset-lav-df)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#)

> **Latest Results**: PRISM Ensemble achieves **81.67% accuracy** and **0.877 AUC-ROC** on 300 test videos from the LAV-DF dataset (2,000 videos total, 5-pillar 473-dim fingerprints).

---

## Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Key Novelty](#-key-novelty--innovation)
- [System Architecture](#-system-architecture)
- [The 5-Pillar Framework](#-the-5-pillar-framework)
- [Results & Evaluation](#-results--evaluation)
- [Output Visualizations](#-output-visualizations)
- [Installation](#-installation)
- [Usage](#-usage)
- [File Structure](#-file-structure)
- [Future Scope](#-future-scope)

---

## Overview

This project implements **PRISM (Provenance-Rich Integrity & Semantic Media)** â€” a blockchain-secured video authentication system that combines 5-pillar multi-modal deep learning with cryptographic provenance tracking to detect deepfake manipulations in audio-visual content.

### Problem Statement

| Challenge | Our Solution |
|-----------|--------------|
| Deepfakes are increasingly realistic | Multi-modal analysis across 5 independent pillars |
| Single-feature detectors are easily fooled | 473-dim composite fingerprinting with cross-pillar attention |
| No tamper-proof audit trail | DHPC blockchain-inspired provenance chains |
| Lack of explainability | Per-pillar anomaly scores + ablation analysis |

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/your-repo/blockchain-av-auth.git
cd blockchain-av-auth

# Install dependencies
pip install torch numpy pandas scikit-learn opencv-python librosa kagglehub \
            matplotlib seaborn insightface onnxruntime resemblyzer imagehash

# Run the notebook
jupyter notebook main.ipynb
```

**Dataset**: The system uses the [LAV-DF dataset](https://www.kaggle.com/datasets/elin75/localized-audio-visual-deepfake-dataset-lav-df) (136,304 videos) from Kaggle, downloaded automatically via `kagglehub`. We sample 2,000 balanced videos (1,000 authentic + 1,000 deepfake).

---

## Key Novelty & Innovation

### What Makes This System Unique?

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                       KEY INNOVATIONS                                â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚                                                                     â”‚
â”‚  1.  5-PILLAR PRISM FINGERPRINT (473-dim)                           â”‚
â”‚      â€¢ Fuses 5 independent feature domains into one fingerprint     â”‚
â”‚      â€¢ VideoHash + Audio + Geo-FRTA + Motion + AVSync               â”‚
â”‚      â€¢ 5 per-pillar anomaly scores for explainability               â”‚
â”‚                                                                     â”‚
â”‚  2.  CMPA-AuthCNN (Cross-Modal Pillar Attention)                    â”‚
â”‚      â€¢ Custom network with pillar-level attention mechanism         â”‚
â”‚      â€¢ Anomaly gating learns which pillars are most informative     â”‚
â”‚      â€¢ 15% pillar dropout for robustness                            â”‚
â”‚                                                                     â”‚
â”‚  3.  STACKING ENSEMBLE (CNN + RF + GBM)                             â”‚
â”‚      â€¢ Meta-learner: Logistic Regression over base model probs      â”‚
â”‚      â€¢ Statistically significantly better than CNN alone            â”‚
â”‚        (McNemar p = 0.0072)                                         â”‚
â”‚                                                                     â”‚
â”‚  4.  DHPC BLOCKCHAIN PROVENANCE CHAINS                              â”‚
â”‚      â€¢ SHA-256 hash-linked blocks for tamper evidence               â”‚
â”‚      â€¢ Validated chain integrity with tamper detection demo         â”‚
â”‚      â€¢ Provenance-rich: device, timestamp, fingerprint per block    â”‚
â”‚                                                                     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Comparison with Existing Methods

| Feature | Traditional | Single-Modal DNN | **PRISM (Ours)** |
|---------|-------------|-----------------|------------------|
| Video Analysis | âœ… | âœ… | âœ… |
| Audio Analysis | âŒ | âŒ | âœ… |
| Geometric Analysis | âŒ | Partial | âœ… (InsightFace) |
| Motion Analysis | âŒ | âŒ | âœ… |
| Lip-Sync Analysis | âŒ | âŒ | âœ… |
| Blockchain Security | âŒ | âŒ | âœ… |
| Per-Pillar Explainability | âŒ | âŒ | âœ… |

---

## System Architecture

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      PRISM AUTHENTICATION ARCHITECTURE                       â”‚
â”‚                                                                              â”‚
â”‚  Input â†’ [P1:Hash|P2:Audio|P3:Geo|P4:Motion|P5:Sync] â†’ PRISM Fusion (473d) â”‚
â”‚       â†’ CMPA-AuthCNN + RF + GBM â†’ Stacking Ensemble â†’ Auth/Fake + Chain    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

The system operates in **three phases**:

1. **Feature Extraction** â€” 5 parallel pillar extractors process video frames and audio
2. **Fusion & Classification** â€” PRISM fusion creates 473-dim fingerprint â†’ CMPA-AuthCNN + RF + GBM stacking ensemble
3. **Provenance & Verification** â€” DHPC blockchain chain creation + tamper detection

*For the full architecture diagram and cell-by-cell documentation, see [ARCHITECTURE.md](ARCHITECTURE.md).*

---

## The 5-Pillar Framework

| Pillar | Name | Dim | Technology | Role |
|--------|------|-----|-----------|------|
| P1 | VideoHash | 128 | DCT perceptual hash (pHash) | Detect visual frame manipulation |
| P2 | Audio FP | 128 | MFCC + Resemblyzer speaker embedding | Detect audio splicing/synthesis |
| P3 | Geo-FRTA | 128 | InsightFace RetinaFace landmarks | Detect facial geometry anomalies |
| P4 | Motion Sig | 64 | Farneback optical flow | Detect unnatural motion patterns |
| P5 | AVSync | 20 | Lip-audio temporal correlation | Detect lip-sync mismatches |
| â€” | Anomaly | 5 | Per-pillar anomaly scores | Explainability layer |

**Total**: 468 pillar dimensions + 5 anomaly scores = **473-dim PRISM fingerprint**

### Pillar Feature Importance (Random Forest)

| Pillar | Importance | Contribution |
|--------|-----------|--------------|
| Audio | 0.4963 | 49.6% |
| VideoHash | 0.2574 | 25.7% |
| Geo-FRTA | 0.1057 | 10.6% |
| Motion | 0.1019 | 10.2% |
| AVSync | 0.0262 | 2.6% |
| AnomalyScores | 0.0124 | 1.2% |

---

## Results & Evaluation

### Dataset

| Property | Value |
|----------|-------|
| Source | LAV-DF (136,304 videos from Kaggle) |
| Sampled | 2,000 videos (1,000 auth + 1,000 fake) |
| Frames/Video | 15 (uniformly sampled) |
| Frame Size | 112 Ã— 112 px |
| Audio | 22,050 Hz sample rate |
| Split | Train 1,400 / Val 300 / Test 300 |

### Test Set Performance (300 samples: 150 authentic + 150 deepfake)

| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|-------|----------|-----------|--------|------|---------|
| CMPA-AuthCNN | 75.00% | 0.681 | 0.940 | 0.790 | 0.826 |
| Random Forest | 78.00% | 0.747 | 0.847 | 0.794 | 0.842 |
| GBM | 80.33% | 0.779 | 0.847 | 0.812 | **0.898** |
| **PRISM Ensemble** | **81.67%** | **0.784** | **0.873** | **0.827** | 0.877 |

### Confusion Matrix (PRISM Ensemble)

```
              Predicted
              Auth  Fake
Actual Auth   114    36
       Fake    19   131

Sensitivity (Recall) : 87.33%
Specificity          : 76.00%
MCC                  : 0.6374
```

### 5-Fold Cross-Validation

| Metric | Mean Â± Std | 95% CI |
|--------|-----------|--------|
| Accuracy | 0.781 Â± 0.017 | [0.748, 0.814] |
| F1-Score | 0.799 Â± 0.013 | [0.773, 0.825] |
| AUC-ROC  | 0.839 Â± 0.017 | [0.805, 0.872] |

### Statistical Significance

McNemar's test (CNN vs Ensemble): Ï‡Â² = 7.22, **p = 0.0072** â€” ensemble is statistically significantly better.

### Inference Latency

| Metric | Value |
|--------|-------|
| Mean latency | 417.5 ms |
| Median latency | 398.1 ms |
| P95 latency | 570.4 ms |

---

## Output Visualizations

All figures are generated by the notebook and saved to `figures/`.

### 1. Dataset Overview (`dataset_overview.png`)

![Dataset Overview](figures/dataset_overview.png)

3-panel view: class distribution bar chart (1,000 auth vs 1,000 fake), sample authentic frame, sample deepfake frame. Confirms balanced dataset with no class bias.

### 2. Evaluation Dashboard (`evaluation_results.png`)

![Evaluation Results](figures/evaluation_results.png)

10-panel dashboard including: model accuracy comparison bars, CMPA-AuthCNN training curves (35 epochs with early stop), ROC curves for all 4 models, confusion matrices, per-metric comparison bars, and pillar ablation study.

### 3. Head-to-Head Comparison (`pillar_comparison.png`)

![Pillar Comparison](figures/pillar_comparison.png)

27-panel figure comparing 3 matched authentic/deepfake video pairs across all 5 pillars with per-pillar anomaly scores, fingerprint distances, frame thumbnails, and confidence scores.

### 4. Comprehensive Benchmark (Cell 28 â€” inline)

13-panel dashboard displayed in the notebook: PR curves, ROC with confidence band, score distributions, confusion matrix heatmap, model accuracy comparison, feature importance pie chart, threshold sensitivity analysis, CV stability box plot, anomaly radar chart, ensemble metrics breakdown, latency profile, and summary card.

*See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed explanation of every panel and metric.*

---

## Installation

### Requirements

```bash
# Python 3.8+
pip install -r requirements.txt
```

### Dependencies

```
numpy>=1.21.0
pandas>=1.3.0
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.5.0
librosa>=0.9.0
insightface>=0.7.0
onnxruntime>=1.14.0
resemblyzer>=0.1.3
imagehash>=4.2.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0
kagglehub>=0.1.0
```

---

## Usage

### Run the Complete Pipeline

```bash
# Open and run main.ipynb in Jupyter Notebook/Lab or VS Code
jupyter notebook main.ipynb
```

Run all cells sequentially (Cells 1â€“30). The notebook will:
1. Install packages and download the LAV-DF dataset (~136K videos)
2. Sample 2,000 balanced videos and extract frames/audio
3. Initialize all 5 pillar extractors
4. Compute 473-dim PRISM fingerprints for all videos (~50 min on GPU)
5. Train CMPA-AuthCNN + RF + GBM stacking ensemble
6. Evaluate on test set and generate all visualizations
7. Create and validate a DHPC provenance chain with tamper detection demo

---

## File Structure

```
project/
â”œâ”€â”€ main.ipynb                 # Main notebook (30 cells)
â”œâ”€â”€ ARCHITECTURE.md            # Full architecture & output documentation
â”œâ”€â”€ README.md                  # This file
â”œâ”€â”€ export_chains.py           # Provenance chain export utility
â”œâ”€â”€ extract_outputs.py         # Output extraction utility
â”œâ”€â”€ main_old_backup.ipynb      # Previous notebook version (backup)
â”œâ”€â”€ figures/
â”‚   â”œâ”€â”€ dataset_overview.png   # Class balance + sample frames (Cell 8)
â”‚   â”œâ”€â”€ evaluation_results.png # 10-panel evaluation dashboard (Cell 20)
â”‚   â”œâ”€â”€ pillar_comparison.png  # 27-panel head-to-head comparison (Cell 26)
â”‚   â””â”€â”€ reports/               # Generated reports directory
â”œâ”€â”€ video_auth_db/
â”‚   â”œâ”€â”€ best_auth_cnn.pt       # Trained CMPA-AuthCNN model weights
â”‚   â”œâ”€â”€ faiss_index.bin        # FAISS nearest-neighbour search index
â”‚   â”œâ”€â”€ fingerprints.npy       # 2000Ã—473 float32 fingerprint matrix
â”‚   â”œâ”€â”€ fingerprints_meta.json # Per-video fingerprint metadata
â”‚   â”œâ”€â”€ metadata.csv           # Video metadata (IDs, labels, paths)
â”‚   â””â”€â”€ stats.json             # Database statistics
â””â”€â”€ provenance_chains/
    â”œâ”€â”€ demo_chain.json        # 10-block DHPC provenance chain (validated)
    â””â”€â”€ hash_comparisons.json  # Video hash similarity records
```

---

## Future Scope

1. **Real-time Processing** â€” GPU-optimized pipeline for live video streams; edge deployment
2. **Extended Modalities** â€” 3D facial reconstruction, speech semantic verification, background consistency
3. **Federated Learning** â€” Privacy-preserving distributed training across organizations
4. **Smart Contracts** â€” On-chain provenance verification, decentralized storage, NFT-based certificates

---

## Citation

```bibtex
@misc{avauth2026,
  title={Blockchain-Based Audio-Visual Content Authentication System
         with 5-Pillar PRISM Architecture},
  author={Padma Priya et al.},
  year={2026},
  note={Patent Pending}
}
```

---

## License

MIT License â€” See repository for details.
 
 
 
