import json

with open("company_n/company_n_visualization.ipynb") as f:
    nb = json.load(f)

fixes = []

# List of chart cells to fix with their modifications
# Format: (cell_number, old_figsize, new_figsize_with_layout)
fixes_to_apply = [
    (9, 'figsize=(12, 6)', 'figsize=(12, 5.5), constrained_layout=True'),
    (11, 'figsize=(12, 7)', 'figsize=(12, 6), constrained_layout=True'),
    (15, 'figsize=(14, 8)', 'figsize=(14, 6), constrained_layout=True'),
    (19, 'figsize=(15, 8)', 'figsize=(15, 6), constrained_layout=True'),
    (25, 'figsize=(12, 7)', 'figsize=(12, 6), constrained_layout=True'),
    (31, 'figsize=(14, 8)', 'figsize=(14, 6), constrained_layout=True'),
    (34, 'figsize=(15, 8)', 'figsize=(15, 6), constrained_layout=True'),
    (37, 'figsize=(14, 8)', 'figsize=(14, 6), constrained_layout=True'),
]

for cell_num, old_fig, new_fig in fixes_to_apply:
    cell_idx = cell_num - 1
    if cell_idx < len(nb['cells']):
        cell = nb['cells'][cell_idx]
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if old_fig in source:
                new_source = source.replace(old_fig, new_fig)
                new_source = new_source.replace('plt.tight_layout()\n', '')
                
                if isinstance(cell['source'], list):
                    cell['source'] = new_source.split('\n')
                    cell['source'] = [line + '\n' for line in cell['source'][:-1]] + [cell['source'][-1]]
                else:
                    cell['source'] = new_source
                fixes.append(f"Fixed cell {cell_num}")

with open("company_n/company_n_visualization.ipynb", 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

for fix in fixes:
    print(fix)
print(f"\nTotal fixes applied: {len(fixes)}")
