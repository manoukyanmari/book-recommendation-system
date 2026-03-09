#!/usr/bin/env python3
import json

def fix_notebook_cluster(notebook_path):
    """Add cluster initialization to cells that use it"""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    fixes_applied = 0
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            
            # Add cluster initialization to cells that use df['cluster']
            if ("df[df['cluster']" in source_text or "df['cluster'] ==" in source_text) and i >= 48:
                if "if 'cluster' not in df.columns:" not in source_text:
                    lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
                    if lines and not any("if 'cluster' not in df.columns:" in line for line in lines[:3]):
                        init_code = "# Ensure cluster column exists\nif 'cluster' not in df.columns:\n    df['cluster'] = -1\n\n"
                        lines.insert(0, init_code)
                        cell['source'] = lines
                        fixes_applied += 1
    
    # Save the modified notebook
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    return fixes_applied

# Apply to both notebooks
notebooks = [
    'company_a/company_a_visualization.ipynb',
    'company_u/company_u_visualization.ipynb'
]

for nb_path in notebooks:
    try:
        fixes = fix_notebook_cluster(nb_path)
        print("Fixed {} - Applied {} cluster initializations".format(nb_path, fixes))
    except Exception as e:
        print("Error fixing {}: {}".format(nb_path, str(e)))

print("\nDone!")
