#!/usr/bin/env python3
import json

# Fix all cells with plt.figure but no import
for company in ['company_n', 'company_a', 'company_u']:
    nb_path = f'{company}/{company}_visualization.ipynb'
    print(f"Processing {company}...")
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    fixed_count = 0
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'fig = plt.figure' in source and 'import matplotlib.pyplot as plt' not in source:
                print(f"  Cell {idx}: Adding plt import")
                
                # Insert import at the beginning (after any comments)
                cell_source = nb['cells'][idx]['source']
                new_source = []
                inserted = False
                
                for line in cell_source:
                    if line.strip() and not line.startswith('#') and not inserted:
                        # Found first code line, insert imports before it
                        new_source.append('import matplotlib.pyplot as plt\n')
                        new_source.append('import numpy as np\n')
                        new_source.append('\n')
                        inserted = True
                    new_source.append(line)
                
                if not inserted:
                    # All lines were comments/empty, insert after first few lines
                    insert_point = 0
                    for i, line in enumerate(cell_source):
                        if line.strip() and (line.startswith('#') or line.strip().startswith('plt')):
                            insert_point = i + 1
                            break
                    new_source = cell_source[:insert_point] + [
                        'import matplotlib.pyplot as plt\n',
                        'import numpy as np\n',
                        '\n'
                    ] + cell_source[insert_point:]
                
                nb['cells'][idx]['source'] = new_source
                fixed_count += 1
    
    if fixed_count > 0:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False)
        print(f"  Fixed {fixed_count} cells")

print("Done!")
