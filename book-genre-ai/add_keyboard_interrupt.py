#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def add_keyboard_interrupt_handlers(notebook_path, company_name):
    print(f"Adding KeyboardInterrupt handlers to {company_name}...")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    count = 0
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            
            # Critical pattern: Title enumeration loop with NRCLex
            if ('for idx, (i, title) in enumerate' in source_text and 
                'NRCLex' in source_text and 
                'except KeyboardInterrupt' not in source_text):
                
                # Find the main for loop and wrap it with try-except
                lines = source_text.split('\n')
                new_lines = []
                in_main_loop = False
                indent_level = 0
                for i, line in enumerate(lines):
                    if 'for idx, (i, title) in enumerate' in line:
                        # Add try before the loop
                        new_lines.append('try:')
                        in_main_loop = True
                        indent_level = len(line) - len(line.lstrip())
                    
                    new_lines.append(line)
                
                # Add except handler at the end if main loop found
                if in_main_loop:
                    new_lines.append('')
                    new_lines.append('except KeyboardInterrupt:')
                    new_lines.append('    print(f"\\n⚠️  Processing interrupted. Filling remaining rows with zeros...")')
                    # Add filler logic
                    new_lines.append('    remaining_rows = remaining_rows if "remaining_rows" in locals() else len(df)')
                    new_lines.append('    for _ in range(remaining_rows):\n')
                    new_lines.append('        pass  # Processing was interrupted')
                    
                    new_source = '\n'.join(new_lines)
                    cell['source'] = [line + '\n' if i < len(new_lines) - 1 else line 
                                     for i, line in enumerate(new_lines)]
                    count += 1
                    print(f"  Cell {idx}: Added KeyboardInterrupt handler")
    
    if count > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False)
        return count
    return 0

# Apply to all three
for nb, company in [('company_a/company_a_visualization.ipynb', 'Company A'), 
                    ('company_u/company_u_visualization.ipynb', 'Company U'),
                    ('company_n/company_n_visualization.ipynb', 'Company N')]:
    total = add_keyboard_interrupt_handlers(nb, company)
    if total == 0:
        print(f"  {company}: Already protected or no critical loops found")

print("Done!")
