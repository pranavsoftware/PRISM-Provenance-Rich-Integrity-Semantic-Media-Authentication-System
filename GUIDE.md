# PRISM Authentication System - Faculty Testing Guide

## Quick Start

**Total Runtime**: ~30-45 minutes on GPU, ~2-3 hours on CPU

### Minimum Requirements
- **RAM**: 16GB (32GB recommended)
- **Storage**: 50GB free (for dataset + models + outputs)
- **GPU**: Optional but recommended (NVIDIA CUDA-capable GPU)
- **Python**: 3.8+
- **Jupyter**: Installed and working

---

## Pre-Test Checklist

- [ ] **Dataset available**: Download LAV-DF from Kaggle (or Cell 7 auto-downloads)
- [ ] **Kaggle credentials**: `~/.kaggle/kaggle.json` (for automatic download)
- [ ] **GPU available**: Check with `nvidia-smi` in terminal
- [ ] **Python environment**: Virtual environment recommended
- [ ] **Storage space**: 50GB free for dataset + outputs
- [ ] **Internet connection**: Required for dataset download

---

## Phase 1: Initial Setup (5-10 minutes)

### Step 1.1: Verify Environment
```python
# Run in Jupyter cell to verify:
import torch
import numpy as np

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
print(f"NumPy version: {np.__version__}")
```

**Expected output**: PyTorch installed, GPU detected (if available)

---

### Step 1.2: Run Cells 1-5 (Packages & Configuration)
- **Cell 1**: Markdown intro (no execution)
- **Cell 2**: Setup header (no execution)
- **Cell 3**: Package installation
  - ✓ Install duration: 2-5 minutes
  - ✓ All packages should install successfully
  - ⚠ If any package fails: Note it, continue (fallback implementations provided)
- **Cell 4**: Import verification
  - ✓ All imports successful
  - ✓ Device detected (GPU or CPU)
  - ⚠ If any import fails: Critical error, stop and fix
- **Cell 5**: Configuration setup
  - ✓ Creates directories (figures/, video_auth_db/, provenance_chains/)
  - ✓ Prints configuration summary
  - ✓ Random seed set (42)

**Verification checklist**:
- [ ] No import errors
- [ ] Device type identified
- [ ] All directories created
- [ ] Configuration printed

---

## Phase 2: Data Loading (5-15 minutes)

### Step 2.1: Download Dataset (Cell 6-7)
- **Cell 6**: Dataset header
- **Cell 7**: Download from Kaggle
  - ✓ Requires Kaggle API key
  - ⚠ Download time: 10-20 minutes depending on internet
  - ✓ Creates: video_auth_db/ directory with LAV-DF files
  - ✓ Prints: Dataset statistics (total videos, authentic/fake count)

**What to watch for**:
- If download fails: Manually place LAV-DF dataset in video_auth_db/
- Expected result: ~2000+ videos (1000+ authentic, 1000+ deepfake)

### Step 2.2: Load Frames & Audio (Cell 8)
- **Duration**: 5-10 minutes
- **Process**:
  - Extracts 15 frames per video at 112×112 resolution
  - Extracts 5-second audio clips at 16kHz
  - Builds train/val/test splits (70/15/15)
- **Output**:
  - Dataset statistics table
  - Sample frame visualization
  - Verification: frames shape (N, 15, 112, 112, 3)

**Verification checklist**:
- [ ] Dataset shape correct
- [ ] Class distribution balanced
- [ ] Train/val/test splits printed
- [ ] Sample visualization displayed

---

## Phase 3: Feature Extraction (20-40 minutes)

### Step 3.1: Extract 5 Pillars (Cells 9-14)
- **Cells 9-10**: Video Hashing
  - ✓ Duration: <1 minute (class definition)
  - ✓ Output: VideoHasher object initialized
  - ✓ Verify: "VideoHasher initialized" printed

- **Cells 11-12**: Audio Fingerprinting
  - ✓ Duration: <1 minute
  - ✓ Output: AudioFingerprinter object with Resemblyzer status
  - ✓ Verify: Speaker embedding loaded (if available)

- **Cells 13-14**: Geometric Signature
  - ✓ Duration: <1 minute
  - ✓ Output: Face detection method confirmed (InsightFace → MediaPipe → Haar)
  - ✓ Verify: "Face Detection: Using [method]" printed

- **Cells 15-16**: Motion Analysis
  - ✓ Duration: <1 minute
  - ✓ Output: MotionSignatureExtractor initialized
  - ✓ Verify: Correct initialization message

- **Cells 17-18**: Audio-Visual Sync
  - ✓ Duration: <1 minute
  - ✓ Output: AVSyncDetector initialized
  - ✓ Verify: "Lip-sync analysis" confirmed

**Verification checklist**:
- [ ] All 5 extractors initialized successfully
- [ ] No errors during class definitions
- [ ] Face detection method confirmed
- [ ] All initialization messages printed

### Step 3.2: PRISM Fusion Engine (Cell 16)
- **Duration**: <1 minute
- **Output**: PRISMFusionEngine + VideoAuthDatabase initialized
- **Verify**: "PRISM ready — fingerprint dim = 473"

---

## Phase 4: Training (15-30 minutes)

### Step 4.1: Compute Fingerprints (Cell 20)
- **Duration**: 5-15 minutes (depends on video loading speed)
- **Process**:
  - Computes 473-dim fingerprint for each video
  - Registers in database
  - Prints progress every 200 videos
- **Expected output**:
  ```
  [2000/2000]  rate: 15.3 vid/s   ETA 0s
  ✓ Fingerprints computed in 132s
  Anomaly score stats (last 5 dims):
    hash:   mean=0.2341  std=0.1823
    audio:  mean=0.3120  std=0.2012
    ...
  ✓ 2000 fingerprints saved
  ```

**Verification checklist**:
- [ ] Fingerprint computation completes
- [ ] All 2000 videos processed
- [ ] Anomaly statistics printed
- [ ] Data split information displayed

### Step 4.2: Train CNN (Cell 21)
- **Duration**: 10-25 minutes (depends on GPU)
  - GPU: ~10-15 minutes
  - CPU: ~60+ minutes
- **Process**:
  - Training with mix-up augmentation
  - Validation every epoch
  - Early stopping on plateau
- **Expected output**:
  ```
  Epoch   5/50  loss=0.4231/0.3821  acc=0.8234/0.8412  best=0.8412
  Epoch  10/50  loss=0.2156/0.2543  acc=0.9012/0.9165  best=0.9165
  ...
  ✓ Best CMPA-AuthCNN  val_acc = 0.9234
  ```

**What to watch for**:
- Training loss decreases over epochs
- Validation loss follows similar trend
- No NaN or inf values
- Best validation accuracy should be >0.90

**If training stalls**:
- Validation accuracy not changing for 12+ epochs → Early stopping
- This is expected behavior

### Step 4.3: Train Ensemble (Cell 22)
- **Duration**: 5-10 minutes
- **Process**:
  - Random Forest: 300-500 trees
  - GBM: 300 boosting rounds
  - Learned stacking: LogisticRegression on validation set
- **Expected output**:
  ```
  RF  val_acc = 0.9087
  GBM val_acc = 0.8923
  CNN val_acc = 0.9234  val_AUC = 0.9876
  Stack val_acc = 0.9312
  ```

**Verification checklist**:
- [ ] RF, GBM trained successfully
- [ ] CNN extracts probabilities
- [ ] Stacking meta-learner trained
- [ ] All accuracies > 0.85

---

## Phase 5: Evaluation (10-20 minutes)

### Step 5.1: Test Metrics (Cell 23)
- **Duration**: 2-3 minutes
- **Output**: Comprehensive performance metrics
- **Expected results**:
  ```
  CMPA-CNN        acc=0.9234   prec=0.9145   rec=0.9312   F1=0.9228   AUC=0.9876
  RF              acc=0.9087   prec=0.8945   rec=0.9234   F1=0.9088   AUC=0.9723
  GBM             acc=0.8923   prec=0.8734   rec=0.9012   F1=0.8872   AUC=0.9567
  PRISM-Ensemble  acc=0.9312   prec=0.9234   rec=0.9401   F1=0.9317   AUC=0.9923 ← Best
  ```

**Performance targets**:
- | Metric | Minimum | Target | Excellent |
  |--------|---------|--------|-----------|
  | Accuracy | 0.85 | 0.92 | >0.95 |
  | AUC-ROC | 0.90 | 0.98 | >0.99 |
  | F1-score | 0.85 | 0.92 | >0.95 |
  | Precision | 0.85 | 0.92 | >0.95 |
  | Recall | 0.85 | 0.92 | >0.95 |

### Step 5.2: Ablation Study (Cell 24)
- **Duration**: 2-3 minutes
- **Shows importance** of each pillar
- **Expected output**:
  ```
  Drop Hash   → acc=0.902  (Δ = -2.9%)  ← Important
  Drop Audio  → acc=0.894  (Δ = -3.7%)  ← Most important
  Drop Geo    → acc=0.918  (Δ = -1.4%)  ← Least important
  Drop Motion → acc=0.910  (Δ = -2.1%)
  Drop Sync   → acc=0.925  (Δ = -0.6%)
  ```

**What to notice**: Each pillar contributes to overall accuracy

### Step 5.3: Visualizations (Cell 25)
- **Duration**: 1-2 minutes
- **Creates**: 9-panel dashboard
- **Outputs**: figures/prism_dashboard.png
- **Contents**:
  1. Training curves (loss & accuracy)
  2. ROC curves (all 4 models)
  3. Confusion matrices (2 variants)
  4. Model accuracy comparison
  5. Ablation importances
  6. Anomaly score distributions
  7. Additional metrics

---

## Phase 6: Advanced Features (10-15 minutes)

### Step 6.1: Two-Stage Inference & Provenance (Cells 26-29)
- **Duration**: 3-5 minutes
- **What it does**:
  - Fast anomaly screening (Stage 1: <5ms)
  - Full PRISM analysis (Stage 2: ~100ms)
  - Blockchain-like provenance chain with tamper detection
- **Expected output**:
  ```
  ✓ Query 1: [AUTHENTIC] certainty=HIGH stage=1 latency=2.3ms
  ✗ Query 2: [DEEPFAKE] certainty=HIGH stage=2 latency=89.4ms
  ...
  Provenance chain: 10 blocks, VALID ✓
  Tamper detection: Trial 1 DETECTED ✓, Trial 2 DETECTED ✓, etc.
  ```

**Verification**:
- [ ] PTS working (both stages used)
- [ ] Latency reasonable (<150ms total)
- [ ] Provenance chain created
- [ ] Tamper detection working

### Step 6.2: Benchmark & Analysis (Cells 30-31)
- **Duration**: 2-3 minutes
- **Outputs**: 
  - Comparison with published results
  - Per-pillar latency breakdown
  - Hash verification proof

### Step 6.3: Head-to-Head Comparison (Cells 32-33)
- **Duration**: 2-3 minutes
- **Shows**: Visual comparison of authentic vs deepfake videos
- **Outputs**: Visualization with sample frames, anomaly scores

### Step 6.4: Comprehensive Verification (Cells 34-35)
- **Duration**: 10-15 minutes
- **Performs**: 
  - Extended classification metrics (20+ metrics)
  - 5-fold cross-validation
  - Threshold sensitivity analysis
  - Feature importance ranking
  - Statistical significance testing (McNemar)
  - 10 detailed plots
- **Output**: figures/benchmark_*.png files

### Step 6.5: Final Authentication Certificate (Cells 36-37)
- **Duration**: 1-2 minutes
- **Performs**: 6 integrity proofs
- **Output**: 
  - provenance_chains/authentication_certificate.json
  - figures/authentication_certificate.png
- **Contains**: SHA-256 checksums, verification status, all metrics

---

## Phase 7: Similarity Search (Optional, 15-20 minutes)

If time permits, test the **main_similarity_search.ipynb**:

### Step 7.1: Setup (Cells 1-6)
- **Duration**: 1-2 minutes
- **Loads**: PRISM fingerprints from Phase 4

### Step 7.2: Deep Embeddings (Cell 8)
- **Duration**: 1-2 minutes
- **Extracts**: 128-dim embeddings from CNN

### Step 7.3: Build FAISS Indices (Cell 10)
- **Duration**: <1 minute
- **Creates**: 3 searchable indices

### Step 7.4: Query & Retrieve (Cell 14)
- **Duration**: 1-2 minutes
- **Expected**: Top-k similar videos retrieved fast (<1ms per query)

### Step 7.5: Performance Evaluation (Cell 20)
- **Duration**: 3-5 minutes
- **Expected**:
  ```
  deep_embed: P@1=0.92  MRR=0.90  Latency=0.7ms
  ```

### Step 7.6: Exact Match vs Similarity (Cell 24)
- **Duration**: 2-3 minutes
- **Shows**:
  - SHA-256 misses all perturbed versions (0%)
  - FAISS finds 65-95% of perturbed versions ✓

---

## Testing Report Template

### System Performance Summary

**Date**: [DATE]  
**Tested by**: [NAME]  
**Hardware**: [CPU/GPU details]  
**Total Runtime**: [HH:MM]  

#### Classification Metrics
| Model | Accuracy | Precision | Recall | F1 | AUC-ROC |
|-------|----------|-----------|--------|-----|---------|
| CMPA-CNN | [ ] | [ ] | [ ] | [ ] | [ ] |
| RF | [ ] | [ ] | [ ] | [ ] | [ ] |
| GBM | [ ] | [ ] | [ ] | [ ] | [ ] |
| Ensemble | [ ] | [ ] | [ ] | [ ] | [ ] |

#### Pillar Ablation Results
| Pillar | Accuracy Drop | Importance |
|--------|---------------|-----------|
| Hash | [ ]% | [ ]% |
| Audio | [ ]% | [ ]% |
| Geo | [ ]% | [ ]% |
| Motion | [ ]% | [ ]% |
| Sync | [ ]% | [ ]% |

#### Performance vs Targets
- [ ] Ensemble accuracy ≥ 92%
- [ ] Ensemble AUC-ROC ≥ 0.98
- [ ] Per-model F1 ≥ 0.92
- [ ] Inference latency < 150ms
- [ ] Cross-validation stable (std < 0.02)

#### Features Verified
- [ ] 5-pillar extraction working
- [ ] 473-dim fingerprints computed
- [ ] Both classification models working
- [ ] Ensemble stacking functional
- [ ] Provenance chain tamper-proof
- [ ] Similarity search fast (<1ms)
- [ ] Variant detection working

#### Issues Encountered
1. [ ] None
2. [ ] [Issue description, resolution]
3. [ ] [Issue description, resolution]

#### Recommendations for Future Study
- [ ] Test with more data
- [ ] Increase training epochs
- [ ] Fine-tune hyperparameters
- [ ] Test on different deepfake types
- [ ] Integrate with video platform

---

## Troubleshooting Common Issues

### Issue: CUDA Out of Memory (OOM)
**Symptom**: `RuntimeError: CUDA out of memory`  
**Solutions**:
1. Reduce batch_size in Cell 5: `'batch_size': 16` (from 32)
2. Clear GPU cache: Add `torch.cuda.empty_cache()` before training
3. Use CPU instead: Set `DEVICE = 'cpu'` in Cell 4
4. Restart kernel and retry

### Issue: Slow Fingerprint Computation (Cell 20)
**Symptom**: Takes >30 minutes  
**Solutions**:
1. Use GPU: Install CUDA + `pip install torch[cuda]`
2. Reduce frames per video: Change `'frames_per_video': 5` (from 15)
3. Skip face detection: Set `'use_retinaface': False` in Cell 5
4. Skip audio processing: Set `'use_speaker_embedding': False`

### Issue: Face Detection Failing
**Symptom**: InsightFace errors in Cell 12  
**Solutions**:
1. Falls back automatically to MediaPipe → Haar cascade
2. If all fail: Check frame quality, ensure RGB format
3. Manually skip: Set `'use_retinaface': False`

### Issue: Audio Processing Errors (Cell 11)
**Symptom**: LibROSA errors or audio extraction failures  
**Solutions**:
1. Reinstall LibROSA: `pip install --upgrade librosa`
2. Uses synthetic audio fallback (still trains OK)
3. Check audio files exist and are readable

### Issue: Low Test Accuracy (<85%)
**Symptom**: Each model gets <85% test accuracy  
**Solutions**:
1. Increase training epochs: Change `'epochs': 100` (from 50)
2. Decrease learning rate: Change `'learning_rate': 1e-5` (from 3e-4)
3. Increase batch size: Change `'batch_size': 64` (from 32)
4. Check data: Ensure authentic/fake are truly balanced
5. Verify no data leakage: Train/val/test splits might be wrong

### Issue: Early Stopping Too Early (epoch 5-10)
**Symptom**: Training stops at epoch 10 (early stopping)  
**Solutions**:
1. Increase patience: Change patience to 20 in Cell 21
2. Higher learning rate: Try 5e-4
3. Better data: Quality audio extraction essential
4. Skip augmentation: Set MIXUP_ALPHA = 0 (temporary debug)

### Issue: Model Weights File Not Found
**Symptom**: `FileNotFoundError: best_cmpa_cnn.pt not found`  
**Solutions**:
1. Run Cell 21 to completion (trains and saves model)
2. Manually train shorter: `'epochs': 10` for quick test
3. Check file path in Cell 4

---

## Parameter Tuning Guide

### For Faster Testing (15 minutes total)
```python
# In Cell 5, modify CONFIG:
'max_videos': 500,              # ↓ from 2000
'frames_per_video': 8,          # ↓ from 15
'epochs': 20,                   # ↓ from 50
'batch_size': 64,               # ↑ from 32
```
Expected accuracy: ~85-90% (vs 92-95% with full config)

### For Better Results (60 minutes total)
```python
'max_videos': 3000,             # ↑ from 2000
'epochs': 100,                  # ↑ from 50
'learning_rate': 1e-4,          # ↓ from 3e-4 (more stable)
'weight_decay': 5e-5,           # ↓ from 1e-4
```
Expected accuracy: ~94-97%

### For Robust Evaluation (90+ minutes total)
```python
'max_videos': 5000,             # ↑↑ from 2000
'epochs': 150,                  # ↑↑ from 50
'batch_size': 16,               # ↓ from 32 (slower but more stable)
# Also run: 5-fold cross-validation (Cell 35)
```
Expected accuracy: >96%

---

## Expected Runtimes by Hardware

### GPU: NVIDIA RTX 3090
- Phase 1-2 (Setup & data): 10 min
- Phase 4 (Training): 15 min
- Phase 5 (Evaluation): 5 min
- Phase 6 (Advanced): 10 min
- **Total**: ~30-40 minutes

### GPU: NVIDIA RTX 2080
- Phase 1-2: 10 min
- Phase 4 (Training): 25 min
- Phase 5-6: 15 min
- **Total**: ~50-60 minutes

### CPU Only (Intel i7 16-core)
- Phase 1-2: 10 min
- Phase 4 (Training): 120 min
- Phase 5-6: 30 min
- **Total**: 2-3 hours

---

## Validation Checklist (Final)

### Correctness
- [ ] Fingerprints shape: (N, 473) ✓
- [ ] Labels shape: (N,) with values 0 or 1 ✓
- [ ] Train/val/test splits non-overlapping ✓
- [ ] All metrics computed correctly ✓
- [ ] No data leakage between splits ✓

### Performance
- [ ] Test accuracy ≥ 85% (minimum)
- [ ] Test accuracy ≥ 92% (target)
- [ ] AUC-ROC ≥ 0.95 ✓
- [ ] Inference latency < 200ms ✓
- [ ] Cross-validation stable (std < 0.05) ✓

### Robustness
- [ ] Ablation study complete ✓
- [ ] Provenance chain tamper-proof ✓
- [ ] Authentication certificate generated ✓
- [ ] All visualizations saved ✓
- [ ] No NaN/Inf values in results ✓

### Documentation
- [ ] main.ipynb.md completed ✓
- [ ] main_similarity_search.ipynb.md completed ✓
- [ ] Testing report filled ✓
- [ ] All outputs documented ✓

---

## Frequently Asked Questions

**Q: How long does the full pipeline take?**  
A: 30-45 minutes on GPU, 2-3 hours on CPU. You can reduce to 15-20 minutes by lowering `max_videos` to 500.

**Q: Do I need a GPU?**  
A: No, but highly recommended. CPU training takes 10x longer (2-3 hours).

**Q: Can I run just main.ipynb OR main_similarity_search.ipynb separately?**  
A: main_similarity_search.ipynb **requires** main.ipynb to be run first (needs fingerprints). main.ipynb is standalone.

**Q: What should my accuracy be?**  
A: Target: 92-95% on test set. Minimum acceptable: 85%. If below 85%, check data quality or increase training epochs.

**Q: Is 5-fold cross-validation run automatically?**  
A: In Phase 6 Comprehensive Verification (Cell 35), yes. Optional but recommended.

**Q: Can I modify the dataset?**  
A: Yes! Change `'max_videos'` in Cell 5 to use fewer videos (faster testing) or more (better model).

**Q: Where are the results saved?**  
A: Check folders: `video_auth_db/`, `figures/`, `provenance_chains/`

**Q: How do I reset and start over?**  
A: Delete folders and restart: `rm -rf video_auth_db/ figures/ provenance_chains/`

---

## Next Steps After Testing

1. **Document Results**: Fill testing report template with metrics
2. **Analyze Performance**: Which pillar contributes most? (From ablation)
3. **Try Variations**: Test with different video types or datasets
4. **Integration**: Connect to video platform or authentication system
5. **Optimization**: Fine-tune hyperparameters for your specific use case
6. **Deployment**: Package as API or web service

---

## Support & Troubleshooting Contact

For issues:
1. Check "Troubleshooting Common Issues" section above
2. Review cell error messages in notebook
3. Check folder permissions (video_auth_db/, figures/, provenance_chains/)
4. Verify GPU availability: `nvidia-smi`
5. Check Python package versions: `pip list | grep torch`

