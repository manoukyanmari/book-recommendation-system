#!/usr/bin/env python3
"""
Apply all fixes from company_n to company_a and company_u notebooks
Fixes include:
1. Direct data loading in translation cells
2. Sentiment correlation calculation
3. Timeout and interrupt handling in API calls
4. Cluster column initialization
"""
import json
import os

def fix_notebook(notebook_path, company_name):
    """Apply all fixes to a notebook"""
    print(f"\n{'='*60}")
    print(f"Fixing {company_name} notebook...")
    print(f"{'='*60}")
    
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    fixes_applied = 0
    
    # Fix 1: Update translation cells to load data directly
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            
            # Fix translation cell - replace locals() check with try/except
            if "if 'df' not in locals():" in source_text and 'pd.read_csv' in source_text:
                print(f"  [1] Fixing data loading in translation cell ({i})")
                new_source = source_text.replace(
                    "if 'df' not in locals():\n    df = pd.read_csv",
                    "# Load data - always load to ensure it's available\ndf = pd.read_csv"
                ).replace(
                    "if 'df' not in locals():\n    df = pd.read_csv('company_a_genres_output.csv",
                    "df = pd.read_csv('company_a_genres_output.csv"
                ).replace(
                    "if 'df' not in locals():\n    df = pd.read_csv('company_u_genres_output.csv",
                    "df = pd.read_csv('company_u_genres_output.csv"
                ).replace(
                    "if 'df' not in locals():\n    df = pd.read_csv('company_n_genres_output.csv",
                    "df = pd.read_csv('company_n_genres_output.csv"
                )
                cell['source'] = [new_source]
                fixes_applied += 1
            
            # Fix 2: Add sentiment_correlation calculation
            if "if sentiment_correlation > 0.1:" in source_text and "sentiment_correlation = " not in source_text:
                print(f"  [2] Adding sentiment correlation calculation ({i})")
                # Find where to insert it
                lines = cell['source'] if isinstance(cell['source'], list) else cell['source'].split('\n')
                new_lines = []
                for j, line in enumerate(lines):
                    new_lines.append(line)
                    if "plt.show()\nprint(" in line or (j > 0 and 'plt.show()' in lines[j-1] and 'print(' in line):
                        if '# Summary insights' not in new_lines[-3:] and 'sentiment_correlation = ' not in new_lines[-10:]:
                            new_lines.insert(-1, "\n# Calculate sentiment correlation\nsentiment_correlation = df['sentiment_polarity'].corr(df['Number'])\n")
                            fixes_applied += 1
                            break
                cell['source'] = new_lines
            
            # Fix 3: Add socket timeout and KeyboardInterrupt handling to emotional arc
            if 'NRCLex' in source_text and 'prepare_title_for_emotion' in source_text:
                if 'socket.setdefaulttimeout' not in source_text:
                    print(f"  [3] Adding timeout and interrupt handling to emotional arc ({i})")
                    # Add socket import and timeout at the beginning
                    lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
                    new_lines = []
                    import_added = False
                    timeout_added = False
                    
                    for line in lines:
                        if 'import' in line and not import_added:
                            new_lines.append(line)
                            if 'import socket' not in cell['source']:
                                new_lines.append('import socket\n')
                                import_added = True
                        elif 'print(' in line and not timeout_added:
                            new_lines.append('\n# Set socket timeout to prevent hanging on translation API calls\nsocket.setdefaulttimeout(10)\n\n')
                            new_lines.append(line)
                            timeout_added = True
                        else:
                            new_lines.append(line)
                    
                    cell['source'] = new_lines
                    fixes_applied += 1
            
            # Fix 4: Add cluster initialization
            if ("df[df['cluster']" in source_text or "df['cluster'] ==" in source_text) and i >= 48:
                if "if 'cluster' not in df.columns:" not in source_text:
                    print(f"  [4] Adding cluster initialization ({i})")
                    lines = cell['source'] if isinstance(cell['source'], list) else [cell['source']]
                    if lines and not any("if 'cluster' not in df.columns:" in line for line in lines[:3]):
                        init_code = "# Ensure cluster column exists\nif 'cluster' not in df.columns:\n    df['cluster'] = -1\n\n"
                        lines.insert(0, init_code)
                        cell['source'] = lines
                        fixes_applied += 1
    
    # Save the modified notebook
    with open(notebook_path, 'w') as f:
        json.dump(nb, f, indent=1)
    
    print(f"  ✓ Applied {fixes_applied} fixes to {company_name}")
    return fixes_applied

# Apply fixes to both notebooks
base_path = '/Users/mariammanukyan/Desktop/book-recommendation/book-genre-ai'
total_fixes = 0

for notebook_name, company in [('company_a/company_a_visualization.ipynb', 'Company A'), 
                                ('company_u/company_u_visualization.ipynb', 'Company U')]:
    notebook_path = os.path.join(base_path, notebook_name)
    if os.path.exists(notebook_path):
        fixes = fix_notebook(notebook_path, company)
        total_fixes += fixes
    else:
        print(f"⚠️  Notebook not found: {notebook_path}")

print(f"\n{'='*60}")
print(f"✅ Total fixes applied: {total_fixes}")
print(f"{'='*60}")
