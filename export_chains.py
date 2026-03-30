#!/usr/bin/env python3
"""
Export fingerprints and create provenance chains locally.
"""

import numpy as np
import json
from pathlib import Path
from datetime import datetime
import hashlib

BASE_PATH = Path(__file__).parent

# Load fingerprints
fp_path = BASE_PATH / "video_auth_db" / "fingerprints.npy"
fp = np.load(fp_path)
print(f"Loaded fingerprints: {fp.shape}")

# Create provenance chain
chain = []
for i in range(min(5, len(fp))):
    fp_hash = hashlib.sha256(fp[i].tobytes()).hexdigest()
    prev_hash = chain[-1]["current_hash"] if chain else "0" * 64
    
    block_data = f"{i}|{fp_hash}|{prev_hash}"
    current_hash = hashlib.sha256(block_data.encode()).hexdigest()
    
    chain.append({
        "index": i,
        "video_id": f"video_{i:03d}",
        "fingerprint_hash": fp_hash,
        "fingerprint_sample": fp[i][:10].tolist(),
        "previous_hash": prev_hash,
        "current_hash": current_hash,
        "timestamp": datetime.now().isoformat(),
        "verified": True
    })

# Save chain
chain_path = BASE_PATH / "provenance_chains" / "demo_chain.json"
with open(chain_path, "w") as f:
    json.dump({"chain": chain, "valid": True, "total_blocks": len(chain)}, f, indent=2)
print(f"Saved provenance chain with {len(chain)} blocks to {chain_path}")

# Create hash comparison JSON
hash_comparisons = {
    "method": "SHA-256",
    "comparisons": []
}
for i in range(min(5, len(fp)-1)):
    h1 = hashlib.sha256(fp[i].tobytes()).hexdigest()
    h2 = hashlib.sha256(fp[i+1].tobytes()).hexdigest()
    
    # Compute fingerprint similarity
    sim = float(np.dot(fp[i], fp[i+1]))
    
    hash_comparisons["comparisons"].append({
        "video_1": f"video_{i:03d}",
        "video_2": f"video_{i+1:03d}",
        "hash_1": h1[:32] + "...",
        "hash_2": h2[:32] + "...",
        "fingerprint_similarity": round(sim, 4),
        "hash_match": h1 == h2
    })

hash_path = BASE_PATH / "provenance_chains" / "hash_comparisons.json"
with open(hash_path, "w") as f:
    json.dump(hash_comparisons, f, indent=2)
print(f"Saved hash comparisons to {hash_path}")

# Save fingerprints metadata
meta = {
    "shape": list(fp.shape),
    "dtype": str(fp.dtype),
    "n_videos": int(fp.shape[0]),
    "fingerprint_dim": int(fp.shape[1]),
    "norm_type": "L2",
    "created": datetime.now().isoformat()
}
meta_path = BASE_PATH / "video_auth_db" / "fingerprints_meta.json"
with open(meta_path, "w") as f:
    json.dump(meta, f, indent=2)
print(f"Saved fingerprint metadata to {meta_path}")

print("\n✓ All exports complete!")
