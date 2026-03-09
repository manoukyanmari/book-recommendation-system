import json

with open('company_n_visualization.ipynb') as f:
    nb = json.load(f)

cells = nb['cells']

# Find key section indices
setup_end = 7  # Everything up to (not including) Structural header
structural_start = 7
lang_dist_idx = 21
genre_vol_idx = 23
lexical_start = 25

print("Current layout:")
print(f"  Setup: cells 0-6 ({len(cells[0:7])} cells)")
print(f"  Structural: cells 7-20 ({len(cells[7:21])} cells)")
print(f"  Language Distribution: cells 21-22 ({len(cells[21:23])} cells)")
print(f"  Genre Volume: cells 23-24 ({len(cells[23:25])} cells)")
print(f"  Lexical onwards: cells 25-51 ({len(cells[25:])} cells)")

# Extract sections
setup = cells[0:7]  # Cells 0-6 (keep as is)
structural_and_after = cells[7:21]  # Structural section headers/content only
lang_dist = cells[21:23]  # Language Distribution 
genre_vol = cells[23:25]  # Genre Volume
rest = cells[25:]  # Lexical onwards

# New order: setup → lang_dist → genre_vol → structural → rest
new_cells = setup + lang_dist + genre_vol + structural_and_after + rest

print(f"\nNew layout:")
print(f"  Setup: {len(setup)} cells")
print(f"  Language Distribution: {len(lang_dist)} cells")
print(f"  Genre Volume: {len(genre_vol)} cells")
print(f"  Structural onwards: {len(structural_and_after)} cells")
print(f"  Rest: {len(rest)} cells")
print(f"  Total: {len(new_cells)} cells (was {len(cells)})")

# Write updated notebook
nb['cells'] = new_cells
with open('company_n_visualization.ipynb', 'w') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✅ Cells reordered successfully!")
