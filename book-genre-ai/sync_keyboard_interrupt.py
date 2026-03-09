#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import shutil

# Backup original files
for nb_path in ['company_a/company_a_visualization.ipynb', 
                'company_u/company_u_visualization.ipynb']:
    shutil.copy(nb_path, nb_path + '.backup')
    print(f"Backed up {nb_path}")

# Read the working emotional arc cell from company_n
with open('company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    cn = json.load(f)

# Find the emotional arc cell
n_emotional_cell = None
n_cell_idx = -1
for idx, cell in enumerate(cn['cells']):
    source = ''.join(cell['source'])
    if 'from nrclex import NRCLex' in source and 'except KeyboardInterrupt' in source:
        n_emotional_cell = cell.copy()
        n_cell_idx = idx
        print(f"Found company_n emotional arc cell with KeyboardInterrupt handler at index {idx}")
        break

if not n_emotional_cell:
    print("ERROR: Could not find emotional arc cell with KeyboardInterrupt in company_n")
    exit(1)

# Apply to company_a
print("\nProcessing company_a...")
with open('company_a/company_a_visualization.ipynb', 'r', encoding='utf-8') as f:
    ca = json.load(f)

found_a = False
for idx, cell in enumerate(ca['cells']):
    source = ''.join(cell['source'])
    if 'from nrclex import NRCLex' in source:
        print(f"  Replacing company_a emotional arc cell at index {idx}")
        ca['cells'][idx] = n_emotional_cell.copy()
        found_a = True
        break

if found_a:
    with open('company_a/company_a_visualization.ipynb', 'w', encoding='utf-8') as f:
        json.dump(ca, f, ensure_ascii=False)
    print("  ✓ Updated")

# Apply to company_u
print("\nProcessing company_u...")
with open('company_u/company_u_visualization.ipynb', 'r', encoding='utf-8') as f:
    cu = json.load(f)

found_u = False
for idx, cell in enumerate(cu['cells']):
    source = ''.join(cell['source'])
    if 'from nrclex import NRCLex' in source:
        print(f"  Replacing company_u emotional arc cell at index {idx}")
        cu['cells'][idx] = n_emotional_cell.copy()
        found_u = True
        break

if found_u:
    with open('company_u/company_u_visualization.ipynb', 'w', encoding='utf-8') as f:
        json.dump(cu, f, ensure_ascii=False)
    print("  ✓ Updated")

if found_a and found_u:
    print("\n✓ KeyboardInterrupt handlers successfully applied to all notebooks")
else:
    if not found_a:
        print("\n✗ Failed to update company_a")
    if not found_u:
        print("\n✗ Failed to update company_u")
