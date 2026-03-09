import json

with open("company_n/company_n_visualization.ipynb") as f:
    nb = json.load(f)

cells = nb['cells']
fixes_applied = 0

# Fix plt.subplots calls
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        
        if 'plt.subplots(' in source and 'constrained_layout=True' not in source:
            # Simple replacement: find plt.subplots(...) and add constrained_layout
            lines = source.split('\n')
            for j, line in enumerate(lines):
                if 'plt.subplots(' in line and 'constrained_layout' not in line:
                    # Find the line with plt.subplots and add constrained_layout
                    # Handle different cases
                    if line.rstrip().endswith(')'):
                        # Replace closing ) with , constrained_layout=True)
                        lines[j] = line.rstrip()[:-1] + ', constrained_layout=True)'
                    else:
                        # Multi-line subplots call - need to find closing )
                        pass
                    fixes_applied += 1
            
            new_source = '\n'.join(lines)
            if new_source != source:
                if isinstance(cell['source'], list):
                    # Preserve as list format
                    cell['source'] = new_source.split('\n')
                    cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                else:
                    cell['source'] = new_source

with open("company_n/company_n_visualization.ipynb", 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"Applied {fixes_applied} fixes to company_n notebook")
