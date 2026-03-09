import json

with open("company_u/company_u_visualization.ipynb") as f:
    nb = json.load(f)

cells = nb['cells']

# Find key sections
summary_indices = []
for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        if '## Summary Statistics' in source:
            summary_indices.append(i)
            print(f"Found Summary Statistics at cell {i}")

# There should be 2 Summary Statistics sections - one misplaced in middle, one at end
if len(summary_indices) >= 2:
    early_summary_idx = summary_indices[0]
    late_summary_idx = summary_indices[1]
    
    print(f"Early Summary at {early_summary_idx}, Late Summary at {late_summary_idx}")
    
    # Remove the early one (it and its code cell)
    before = cells[:early_summary_idx]
    after = cells[early_summary_idx+2:]  # Skip early summary and its code
    
    nb['cells'] = before + after
    
    with open("company_u/company_u_visualization.ipynb", 'w') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    
    print(f"Removed early Summary Statistics - now {len(nb['cells'])} cells")
else:
    print(f"Found {len(summary_indices)} Summary Statistics sections - expected 2")
