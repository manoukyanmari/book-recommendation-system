#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

for company in ['company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    print(f"Fixing {company}...")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the outlier analysis cell
    for idx, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        
        if 'OUTLIER DETECTION' in source and 'df_sorted[' in source and 'df_sorted = df.sort_values' not in source:
            print(f"  Found outlier cell at {idx}")
            
            # Add the definitions
            cell_source = nb['cells'][idx]['source']
            new_source = []
            inserted = False
            
            for i, line in enumerate(cell_source):
                if line.strip() == '# Z-score method' and not inserted:
                    # Insert the definitions before this line
                    new_source.append('# Prepare sorted data for analysis\n')
                    new_source.append('df_sorted = df.sort_values(\'Number\', ascending=False).copy()\n')
                    new_source.append('total_volume = df[\'Number\'].sum()\n')
                    new_source.append('\n')
                    inserted = True
                new_source.append(line)
            
            if inserted:
                nb['cells'][idx]['source'] = new_source
                
                with open(nb_path, 'w', encoding='utf-8') as f:
                    json.dump(nb, f, ensure_ascii=False)
                
                print(f"  Added definitions")
            break
