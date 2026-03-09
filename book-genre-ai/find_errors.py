#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find cells using df_sorted or total_volume
for idx, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    
    # Check for usage of df_sorted without definition
    if 'top_1_pct_threshold = df_sorted' in source and 'df_sorted = ' not in source:
        print(f"Cell {idx}: USES df_sorted without defining it")
        print(f"  First 100 chars: {source[:100]}")
