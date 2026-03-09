#!/usr/bin/env python3
import json

print("COMPREHENSIVE FIX VERIFICATION\n")
print("="*80)

fixes_to_check = {
    'KeyboardInterrupt handlers': 'except KeyboardInterrupt',
    'Socket timeout protection': 'socket.setdefaulttimeout',
    'K_range definition': 'K_range = range(3, 11)',
    'df_sorted definition': 'df_sorted = df.sort_values',
    'total_volume definition': 'total_volume = df',
    'Cluster initialization': "if 'cluster' not in df.columns",
    'Sentiment correlation': 'sentiment_correlation = df',
    'plt import in visualizations': 'import matplotlib.pyplot as plt'
}

for company in ['company_n', 'company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"\n{company.upper()}:")
    print("-" * 80)
    
    for fix_name, search_text in fixes_to_check.items():
        # Count occurrences across all cells
        total_count = 0
        for cell in nb['cells']:
            source = ''.join(cell['source'])
            total_count += source.count(search_text)
        
        status = "OK" if total_count > 0 else "MISSING"
        print(f"  [{status}] {fix_name}: {total_count} occurrence(s)")

print("\n" + "="*80)
