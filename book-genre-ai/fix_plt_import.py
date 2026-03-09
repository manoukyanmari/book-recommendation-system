#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

# Fix plt import in problematic cells
for company in ['company_n', 'company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    print(f"Processing {company}...")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Find the visualization cell (with plt.figure(figsize=(16, 12)))
    for idx, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        if 'fig = plt.figure(figsize=(16, 12))' in source and 'import matplotlib.pyplot as plt' not in source:
            print(f"  Found visualization cell at {idx} - adding plt import")
            
            # Insert import at the very beginning
            cell_source = nb['cells'][idx]['source']
            new_source = []
            inserted = False
            
            for line in cell_source:
                if line.strip() and not line.startswith('#') and not inserted:
                    # First non-comment, non-empty line - insert imports before it
                    new_source.append('import matplotlib.pyplot as plt\n')
                    new_source.append('import numpy as np\n')
                    new_source.append('\n')
                    inserted = True
                new_source.append(line)
            
            # If we haven't inserted yet (all lines are comments/empty), add at end of header comments
            if not inserted:
                new_source.insert(0, 'import matplotlib.pyplot as plt\n')
                new_source.insert(1, 'import numpy as np\n')
                new_source.insert(2, '\n')
            
            nb['cells'][idx]['source'] = new_source
            
            with open(nb_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, ensure_ascii=False)
            print(f"    Added imports")
            break

print("Done!")
