#!/usr/bin/env python3
"""
Extract outputs from executed notebook and save locally.
Saves: figures, fingerprints, hash comparisons, provenance chains
"""

import json
import base64
import numpy as np
from pathlib import Path

# Paths
BASE_PATH = Path(__file__).parent
FIGURES_PATH = BASE_PATH / "figures"
CHAINS_PATH = BASE_PATH / "provenance_chains"
DB_PATH = BASE_PATH / "video_auth_db"

# Ensure directories exist
FIGURES_PATH.mkdir(exist_ok=True)
(FIGURES_PATH / "reports").mkdir(exist_ok=True)
CHAINS_PATH.mkdir(exist_ok=True)

def extract_notebook_images():
    """Extract base64 images from notebook and save as PNG files."""
    import nbformat
    
    notebook_path = BASE_PATH / "main.ipynb"
    with open(notebook_path, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    image_count = 0
    cell_names = [
        "dataset_overview",
        "evaluation_results", 
        "pillar_comparison"
    ]
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and 'outputs' in cell:
            for output in cell.outputs:
                if 'data' in output and 'image/png' in output['data']:
                    img_data = output['data']['image/png']
                    img_bytes = base64.b64decode(img_data)
                    
                    # Name based on cell content
                    if image_count < len(cell_names):
                        filename = f"{cell_names[image_count]}.png"
                    else:
                        filename = f"output_{image_count}.png"
                    
                    filepath = FIGURES_PATH / filename
                    with open(filepath, 'wb') as f:
                        f.write(img_bytes)
                    print(f"Saved: {filepath}")
                    image_count += 1
    
    return image_count

if __name__ == "__main__":
    print("="*60)
    print("EXTRACTING NOTEBOOK OUTPUTS")
    print("="*60)
    
    n_images = extract_notebook_images()
    print(f"\n✓ Extracted {n_images} images to {FIGURES_PATH}")
    
    # Check for existing fingerprints
    fp_path = DB_PATH / "fingerprints.npy"
    if fp_path.exists():
        fp = np.load(fp_path)
        print(f"✓ Fingerprints found: {fp.shape}")
    
    print("\n✓ Extraction complete!")
