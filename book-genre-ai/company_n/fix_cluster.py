#!/usr/bin/env python3
import json

with open('company_n_visualization.ipynb', 'r') as f:
    nb = json.load(f)

# Fix cells that use df['cluster'] without initialization
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source_text = ''.join(cell['source'])
        
        # If cell uses df['cluster'] but doesn't initialize it
        if ("df[df['cluster']" in source_text or "df['cluster'] =" in source_text) and i >= 48:
            # Check if it already has initialization
            if "if 'cluster' not in df.columns:" not in source_text:
                lines = cell['source']
                if lines and not any("if 'cluster' not in df.columns:" in line for line in lines[:3]):
                    # Add initialization at the start
                    init_code = "# Ensure cluster column exists\nif 'cluster' not in df.columns:\n    df['cluster'] = -1\n\n"
                    cell['source'].insert(0, init_code)
                    print("Fixed cell {} ID: {}".format(i, cell.get('id', 'NO_ID')))

# Save the modified notebook
with open('company_n_visualization.ipynb', 'w') as f:
    json.dump(nb, f, indent=1)

print("Notebook fixed!")
