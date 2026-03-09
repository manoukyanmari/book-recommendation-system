#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Read the working translation cell from company_n
with open('company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    cn = json.load(f)

# Find both cells in company_n
n_translation_cell = None
n_emotional_cell = None

for idx, cell in enumerate(cn['cells']):
    source = ''.join(cell['source'])
    if 'except KeyboardInterrupt' not in source:
        continue
    
    if 'Translator' in source and 'translator.translate' in source:
        n_translation_cell = cell.copy()
        print(f"Found company_n translation cell at index {idx}")
    elif 'from nrclex import NRCLex' in source:
        n_emotional_cell = cell.copy()
        print(f"Found company_n emotional arc cell at index {idx}")

if not n_translation_cell:
    print("ERROR: Could not find translation cell in company_n")
    exit(1)

# Apply translation cell to company_a
print("\nProcessing company_a translation cell...")
with open('company_a/company_a_visualization.ipynb', 'r', encoding='utf-8') as f:
    ca = json.load(f)

for idx, cell in enumerate(ca['cells']):
    source = ''.join(cell['source'])
    if 'Translator' in source and 'translator.translate' in source and 'except KeyboardInterrupt' not in source:
        print(f"  Replacing company_a translation cell at index {idx}")
        ca['cells'][idx] = n_translation_cell.copy()
        with open('company_a/company_a_visualization.ipynb', 'w', encoding='utf-8') as f:
            json.dump(ca, f, ensure_ascii=False)
        print("  ✓ Updated")
        break

# Apply translation cell to company_u
print("\nProcessing company_u translation cell...")
with open('company_u/company_u_visualization.ipynb', 'r', encoding='utf-8') as f:
    cu = json.load(f)

for idx, cell in enumerate(cu['cells']):
    source = ''.join(cell['source'])
    if 'Translator' in source and 'translator.translate' in source and 'except KeyboardInterrupt' not in source:
        print(f"  Replacing company_u translation cell at index {idx}")
        cu['cells'][idx] = n_translation_cell.copy()
        with open('company_u/company_u_visualization.ipynb', 'w', encoding='utf-8') as f:
            json.dump(cu, f, ensure_ascii=False)
        print("  ✓ Updated")
        break

print("\n✓ All translation cells updated")
