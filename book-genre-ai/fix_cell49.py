#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

with open('company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and fix cell 49
cell49_source = nb['cells'][49]['source']

# Find the line with "# Z-score method"
new_source = []
inserted = False
for i, line in enumerate(cell49_source):
    if line.strip() == '# Z-score method' and not inserted:
        # Insert the definitions before this line
        new_source.append('# Prepare sorted data for analysis\n')
        new_source.append('df_sorted = df.sort_values(\'Number\', ascending=False).copy()\n')
        new_source.append('total_volume = df[\'Number\'].sum()\n')
        new_source.append('\n')
        inserted = True
    new_source.append(line)

if inserted:
    nb['cells'][49]['source'] = new_source
    
    with open('company_n/company_n_visualization.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, ensure_ascii=False)
    
    print("Added df_sorted and total_volume definitions to cell 49")
else:
    print("Could not find insertion point")
