#!/usr/bin/env python3
import json

def fix_translation_and_correlation(notebook_path, company_name, csv_name):
    """Fix translation cells and add sentiment correlation"""
    print("\nProcessing {} - {}...".format(company_name, notebook_path))
    
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    fixes_applied = 0
    
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
            lines = cell['source'] if isinstance(cell['source'], list) else source_text.split('\n')
            
            # Fix 1: Replace locals() check with direct data loading
            if "if 'df' not in locals():" in source_text and csv_name in source_text:
                print("  [1] Fixing translation cell - removing locals() check")
                new_lines = []
                skip_next = False
                for j, line in enumerate(lines):
                    if "if 'df' not in locals():" in line:
                        # Skip this line and the next indented lines until we hit df = pd.read_csv
                        skip_next = True
                        continue
                    if skip_next and line.strip().startswith('df = pd.read_csv'):
                        new_lines.append('# Load data - always load to ensure it is available\ndf = pd.read_csv')
                        skip_next = False
                        # Skip the rest of this line content if it's been written
                        continue
                    if skip_next and (not line.startswith('    ') or line.strip().startswith('df =')):
                        skip_next = False
                    if not skip_next:
                        new_lines.append(line)
                
                cell['source'] = new_lines
                fixes_applied += 1
            
            # Fix 2: Add sentiment_correlation calculation if missing
            if "if sentiment_correlation > 0.1:" in source_text and "sentiment_correlation = " not in source_text:
                print("  [2] Adding sentiment correlation calculation")
                new_lines = []
                added = False
                for j, line in enumerate(lines):
                    new_lines.append(line)
                    if 'plt.show()' in line and not added and 'print(' in lines[j+1] if j+1 < len(lines) else False:
                        new_lines.append('\n# Calculate sentiment correlation')
                        new_lines.append("sentiment_correlation = df['sentiment_polarity'].corr(df['Number'])")
                        new_lines.append('\n')
                        added = True
                
                if not added:
                    # Try another pattern
                    for j, line in enumerate(lines):
                        if 'plt.show()' in line:
                            lines.insert(j+1, "\n# Calculate sentiment correlation\nsentiment_correlation = df['sentiment_polarity'].corr(df['Number'])\n")
                            added = True
                            break
                
                if added:
                    cell['source'] = lines
                    fixes_applied += 1
            
            # Fix 3: Add socket timeout to NRCLex cells
            if 'NRCLex' in source_text and 'from nrclex' in source_text and 'socket.setdefaulttimeout' not in source_text:
                print("  [3] Adding socket timeout to emotional arc analysis")
                new_lines = []
                socket_added = False
                timeout_added = False
                
                for line in lines:
                    if 'import socket' not in source_text and not socket_added and ('import' in line and 'matplotlib' in line or 'import' in line and 'numpy' in line):
                        new_lines.append(line)
                        new_lines.append('import socket')
                        socket_added = True
                        continue
                    
                    if 'import matplotlib' in line and not socket_added and 'import socket' not in source_text:
                        new_lines.append('import socket')
                        new_lines.append(line)
                        socket_added = True
                        continue
                    
                    if socket_added and not timeout_added and ('print(' in line or 'def ' in line):
                        new_lines.append('\n# Set socket timeout to prevent hanging on translation API calls')
                        new_lines.append('socket.setdefaulttimeout(10)')
                        new_lines.append('')
                        new_lines.append(line)
                        timeout_added = True
                        continue
                    
                    new_lines.append(line)
                
                if socket_added and timeout_added:
                    cell['source'] = new_lines
                    fixes_applied += 1
    
    # Save the modified notebook
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    print("  Applied {} fixes".format(fixes_applied))
    return fixes_applied

# Apply to both notebooks
notebooks = [
    ('company_a/company_a_visualization.ipynb', 'Company A', 'company_a_genres_output.csv'),
    ('company_u/company_u_visualization.ipynb', 'Company U', 'company_u_genres_output.csv')
]

total = 0
for nb_path, company, csv_name in notebooks:
    try:
        fixes = fix_translation_and_correlation(nb_path, company, csv_name)
        total += fixes
    except Exception as e:
        print("Error: {}".format(str(e)))

print("\n✅ Total fixes applied: {}".format(total))
