#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

for company in ['company_n', 'company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    print(f"Processing {company}...")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the visualization cell (the one with K_vals)
    for idx, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if 'K_vals = list(K_range)' in source:
            print(f"  Found visualization cell at {idx}")
            
            # Insert safety checks at the beginning of the cell
            cell_source = nb['cells'][idx]['source']
            new_source = []
            checks_added = False
            
            for line in cell_source:
                # Add checks after the figure setup
                if 'gs = fig.add_gridspec' in line and not checks_added:
                    new_source.append(line)
                    new_source.append('\n')
                    new_source.append('# Ensure required variables are available from clustering cell\n')
                    new_source.append('try:\n')
                    new_source.append('    # These should come from the clustering cell\n')
                    new_source.append('    _ = inertias\n')
                    new_source.append('    _ = silhouette_scores\n')
                    new_source.append('    _ = optimal_k\n')
                    new_source.append('    _ = cluster_info\n')
                    new_source.append('except NameError:\n')
                    new_source.append('    print("ERROR: Clustering cell must be run before visualization.")\n')
                    new_source.append('    print("Please run: Topic Modeling cell (cell above) first.")\n')
                    new_source.append('    raise\n')
                    new_source.append('\n')
                    checks_added = True
                else:
                    new_source.append(line)
            
            if checks_added:
                nb['cells'][idx]['source'] = new_source
                print(f"    Added dependency checks")
            break
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)

print("Done!")
