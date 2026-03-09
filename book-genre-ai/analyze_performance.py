#!/usr/bin/env python3
import json

with open('company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Identify potential bottlenecks
print("PERFORMANCE ANALYSIS OF company_n NOTEBOOK\n")
print("="*80)

for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        
        # Check for API calls
        if 'translator.translate' in source:
            print(f"\nCell {idx}: Translation loop (potential bottleneck)")
            if 'for ' in source:
                print(f"  - Contains loop operations")
            if 'cache' in source:
                print(f"  - Has caching: YES")
            else:
                print(f"  - Has caching: NO (could improve)")
        
        # Check for NRCLex operations
        if 'NRCLex' in source and 'for ' in source:
            print(f"\nCell {idx}: NRCLex emotion analysis")
            print(f"  - Multiple emotions per title")
        
        # Check for TF-IDF
        if 'TfidfVectorizer' in source:
            print(f"\nCell {idx}: TF-IDF vectorization")
            if 'max_features' in source:
                print(f"  - Limits features: YES (good)")
            else:
                print(f"  - Limits features: NO (could improve)")

print("\n" + "="*80)
