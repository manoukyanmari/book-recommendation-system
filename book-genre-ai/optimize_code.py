#!/usr/bin/env python3
import json
import re

def optimize_translation_cell(source):
    """Enhance caching and reduce API calls"""
    if 'translator.translate' not in source:
        return source
    
    # Add persistent JSON-based cache
    optimization = """# Enhanced caching to reduce API calls
import os
cache_file = 'translation_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as f:
        try:
            translation_cache = json.load(f)
        except:
            translation_cache = {}
else:
    translation_cache = {}

# Save cache periodically
def save_cache():
    import json
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(translation_cache, f, ensure_ascii=False)
"""
    
    # Check if this optimization already exists
    if 'translation_cache.json' in source:
        return source
    
    # Insert optimization after imports
    lines = source.split('\n')
    new_lines = []
    inserted = False
    
    for i, line in enumerate(lines):
        if 'translator = Translator()' in line and not inserted:
            new_lines.append(line)
            new_lines.append(optimization)
            inserted = True
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def optimize_tfidf_cell(source):
    """Limit TF-IDF features for speed"""
    if 'TfidfVectorizer' not in source:
        return source
    
    if 'max_features' in source:
        return source  # Already optimized
    
    # Replace TfidfVectorizer initialization
    pattern = r'TfidfVectorizer\((.*?)\)'
    
    def replace_tfidf(match):
        params = match.group(1)
        if 'max_features' not in params:
            # Add max_features limit
            if params.strip().endswith(')'):
                return f"TfidfVectorizer({params[:-1]}, max_features=200)"
            else:
                return f"TfidfVectorizer({params}, max_features=200)"
        return match.group(0)
    
    return re.sub(pattern, replace_tfidf, source)

def optimize_nrclex_cell(source):
    """Add batch processing hint for NRCLex"""
    if 'NRCLex' not in source or 'for ' not in source:
        return source
    
    # Add note about vectorization
    if 'BATCH' in source:
        return source  # Already optimized
    
    optimization = """# Note: NRCLex processes sequentially. For large datasets (>500 rows),
# consider sampling titles first or running in batches."""
    
    if optimization in source:
        return source
    
    # Insert at start of NRCLex loop
    lines = source.split('\n')
    new_lines = []
    inserted = False
    
    for line in lines:
        if 'for idx, (i, title) in enumerate' in line and not inserted:
            new_lines.append(optimization)
            new_lines.append(line)
            inserted = True
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def optimize_notebooks():
    """Apply performance optimizations to all notebooks"""
    
    for company in ['company_n', 'company_a', 'company_u']:
        nb_path = f'{company}/{company}_visualization.ipynb'
        print(f"Optimizing {company}...")
        
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        optimizations_applied = 0
        
        for idx, cell in enumerate(nb['cells']):
            if cell['cell_type'] == 'code':
                source = ''.join(cell['source'])
                original = source
                
                # Apply optimizations
                source = optimize_translation_cell(source)
                if source != original:
                    optimizations_applied += 1
                    original = source
                
                source = optimize_tfidf_cell(source)
                if source != original:
                    optimizations_applied += 1
                    original = source
                
                source = optimize_nrclex_cell(source)
                if source != original:
                    optimizations_applied += 1
                
                # Update cell if modified
                if source != ''.join(cell['source']):
                    nb['cells'][idx]['source'] = source.split('\n')
                    # Ensure proper line endings
                    nb['cells'][idx]['source'] = [line + '\n' if i < len(nb['cells'][idx]['source']) - 1 else line 
                                                 for i, line in enumerate(nb['cells'][idx]['source'])]
        
        if optimizations_applied > 0:
            with open(nb_path, 'w', encoding='utf-8') as f:
                json.dump(nb, f, ensure_ascii=False)
            print(f"  Applied {optimizations_applied} optimization(s)")
        else:
            print(f"  Already optimized")

if __name__ == '__main__':
    optimize_notebooks()
    print("\nOptimization complete!")
