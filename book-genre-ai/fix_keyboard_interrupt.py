#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def add_keyboard_interrupt_to_emotional_arc(notebook_path, company_name):
    """Add KeyboardInterrupt handler to emotional arc analysis cell"""
    print(f"Processing {company_name}...")
    
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            
            # Find emotional arc analysis cell (has NRCLex and the enumerate loop)
            if ('from nrclex import NRCLex' in source_text and 
                'for idx, (i, title) in enumerate(df' in source_text and
                'except KeyboardInterrupt' not in source_text):
                
                print(f"  Cell {idx}: Adding KeyboardInterrupt handler to emotional arc analysis")
                
                # Find the try statement
                if 'try:' not in source_text:
                    # Need to add try-except wrapper
                    lines = source_text.split('\n')
                    
                    # Find where to insert try
                    try_line = -1
                    for i, line in enumerate(lines):
                        if 'for idx, (i, title) in enumerate(df' in line:
                            try_line = i
                            break
                    
                    if try_line >= 0:
                        # Insert try and indent following code, then add except
                        new_lines = []
                        for i in range(try_line):
                            new_lines.append(lines[i])
                        
                        # Add try
                        indent = len(lines[try_line]) - len(lines[try_line].lstrip())
                        new_lines.append(' ' * indent + 'try:')
                        
                        # Add indented loop body
                        for i in range(try_line, len(lines)):
                            if lines[i].strip():
                                line_indent = len(lines[i]) - len(lines[i].lstrip())
                                new_lines.append(' ' * (line_indent + 4) + lines[i].lstrip())
                            else:
                                new_lines.append(lines[i])
                        
                        # Add except block
                        new_lines.append('')
                        new_lines.append('except KeyboardInterrupt:')
                        new_lines.append("    print(f\"\\n⚠️  Emotional arc analysis interrupted. Filling remaining rows with zeros...\")")
                        new_lines.append('    remaining_count = len(df) - len(emotion_analysis_titles)')
                        new_lines.append('    for _ in range(remaining_count):')
                        new_lines.append('        emotion_analysis_titles.append("")')
                        new_lines.append('        title_emotions.append({})')
                        new_lines.append('        for emotion in emotion_types:')
                        new_lines.append('            emotions_data[emotion].append(0)')
                        
                        # Convert back to cell format
                        new_source = '\n'.join(new_lines)
                        cell['source'] = [line + '\n' if i < len(new_lines) - 1 else line 
                                         for i, line in enumerate(new_lines)]
                        
                        with open(notebook_path, 'w', encoding='utf-8') as f:
                            json.dump(nb, f, ensure_ascii=False)
                        return True
    
    print(f"  {company_name}: No changes needed")
    return False

# Apply to all three
for nb, company in [('company_a/company_a_visualization.ipynb', 'Company A'), 
                    ('company_u/company_u_visualization.ipynb', 'Company U'),
                    ('company_n/company_n_visualization.ipynb', 'Company N')]:
    add_keyboard_interrupt_to_emotional_arc(nb, company)

print("Done!")
