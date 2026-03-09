#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

def add_socket_timeout(notebook_path, company_name):
    print(f"Adding socket timeout to {company_name}...")
    
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        count = 0
        for idx, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                source_text = ''.join(cell['source'])
                # Look for emotional arc analysis cell (has NRCLex import)
                if 'from nrclex import NRCLex' in source_text and 'socket.setdefaulttimeout' not in source_text:
                    # Add socket import and timeout
                    lines = source_text.split('\n')
                    last_import = -1
                    for i, line in enumerate(lines):
                        if line.startswith('import ') or line.startswith('from '):
                            last_import = i
                    
                    if last_import >= 0:
                        # Insert socket import if needed
                        if 'import socket' not in source_text:
                            lines.insert(last_import + 1, 'import socket')
                            last_import += 1
                        
                        # Insert timeout setting
                        if 'socket.setdefaulttimeout(10)' not in source_text:
                            lines.insert(last_import + 1, 'socket.setdefaulttimeout(10)')
                        
                        cell['source'] = [line + '\n' if i < len(lines) - 1 else line 
                                         for i, line in enumerate(lines)]
                        count += 1
                        print(f"  Cell {idx}: Added socket timeout")
        
        if count > 0:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, ensure_ascii=False)
            print(f"  Total: {count} cells fixed")
        else:
            print("  No changes needed")
            
    except Exception as e:
        print(f"  Error: {e}")

# Apply to both
for nb, company in [('company_a/company_a_visualization.ipynb', 'Company A'), 
                    ('company_u/company_u_visualization.ipynb', 'Company U')]:
    add_socket_timeout(nb, company)

print("Done!")
