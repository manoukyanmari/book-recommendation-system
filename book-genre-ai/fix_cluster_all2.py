#!/usr/bin/env python3
import json

def fix_notebook(notebook_path, company_name):
    """Add cluster initialization to ALL cells that use it, regardless of position"""
    print("\nProcessing {} - {}...".format(company_name, notebook_path))
    
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    fixes_applied = 0
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            
            # Add cluster initialization to ANY cell that uses df['cluster'] without creating it
            if ("df[df['cluster']" in source_text or ("df['cluster'] ==" in source_text and "df['cluster'] = -1" not in source_text)):
                # Check if cell already creates or initializes cluster
                if "df['cluster'] = -1" not in source_text and "df['cluster'] = cluster_labels" not in source_text:
                    if "if 'cluster' not in df.columns:" not in source_text:
                        lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
                        if lines and not any("if 'cluster' not in df.columns:" in str(line) for line in lines[:3]):
                            init_code = "# Ensure cluster column exists\nif 'cluster' not in df.columns:\n    df['cluster'] = -1\n\n"
                            lines.insert(0, init_code)
                            cell['source'] = lines
                            fixes_applied += 1
                            print("  Added cluster check to cell {} (using df['cluster'])".format(i))
    
    # Save the modified notebook
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    print("  Applied {} fixes".format(fixes_applied))
    return fixes_applied

# Apply to both notebooks
notebooks = [
    ('company_a/company_a_visualization.ipynb', 'Company A'),
    ('company_u/company_u_visualization.ipynb', 'Company U')
]

total = 0
for nb_path, company in notebooks:
    try:
        fixes = fix_notebook(nb_path, company)
        total += fixes
    except Exception as e:
        print("Error: {}".format(str(e)))

print("\n✅ Total cluster initializations added: {}".format(total))
