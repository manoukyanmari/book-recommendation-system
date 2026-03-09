import json
import os

files = [
    "company_a/company_a_visualization.ipynb",
    "company_u/company_u_visualization.ipynb",
    "genre_visualization.ipynb"
]

for file_path in files:
    print(f"\n{'='*60}")
    print(f"Processing: {file_path}")
    print('='*60)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
    
    with open(file_path) as f:
        nb = json.load(f)
    
    cells = nb['cells']
    print(f"Total cells: {len(cells)}")
    
    # Find key section indices
    structural_idx = None
    lang_dist_idx = None
    genre_vol_idx = None
    lexical_idx = None
    
    for i, cell in enumerate(cells):
        if cell['cell_type'] == 'markdown':
            source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            if '## 1. Structural Feature Engineering' in source:
                structural_idx = i
            elif '## Language Distribution Chart' in source:
                lang_dist_idx = i
            elif '## Genre Volume' in source and '##' in source[:20]:  # Matches both "Genre Volume Analysis" and "Genre Volume Distribution"
                genre_vol_idx = i
            elif '## 2. Lexical Analysis' in source:
                lexical_idx = i
    
    print(f"Structural: {structural_idx}, Lang Dist: {lang_dist_idx}, Genre Vol: {genre_vol_idx}, Lexical: {lexical_idx}")
    
    # Check if reordering is needed
    if lang_dist_idx is None or structural_idx is None:
        print("Cannot find all required sections - skipping")
        continue
    
    # If Lang Dist comes after Structural, reordering is needed
    if lang_dist_idx > structural_idx:
        print("Reordering needed")
        
        # Extract sections
        setup = cells[0:structural_idx]
        structural_and_after = cells[structural_idx:lang_dist_idx]
        
        if genre_vol_idx is not None and genre_vol_idx > lang_dist_idx:
            # Has Genre Volume section
            lang_dist = cells[lang_dist_idx:genre_vol_idx]
            genre_vol = cells[genre_vol_idx:lexical_idx]
            rest = cells[lexical_idx:]
            
            # Reorder: setup → lang_dist → genre_vol → structural → rest
            new_cells = setup + lang_dist + genre_vol + structural_and_after + rest
            
            print(f"Successfully reordered!")
            print(f"  Setup: {len(setup)}, Lang Dist: {len(lang_dist)}, Genre Vol: {len(genre_vol)}, Structural: {len(structural_and_after)}, Rest: {len(rest)}")
        else:
            # No Genre Volume section (like company_a)
            lang_dist = cells[lang_dist_idx:lexical_idx]
            rest = cells[lexical_idx:]
            
            # Reorder: setup → lang_dist → structural → rest
            new_cells = setup + lang_dist + structural_and_after + rest
            
            print(f"Successfully reordered!")
            print(f"  Setup: {len(setup)}, Lang Dist: {len(lang_dist)}, Structural: {len(structural_and_after)}, Rest: {len(rest)}")
        
        nb['cells'] = new_cells
        
        with open(file_path, 'w') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
    else:
        print("Already in correct order")
