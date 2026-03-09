#!/usr/bin/env python3
"""
Fix remaining translation cache optimizations for company_a and company_u
"""

import json
import re

def fetch_notebook_translation_cell(company):
    """Get the translation cell to understand its current structure"""
    nb_path = f'{company}/{company}_visualization.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            source = ''.join(cell['source'])
            if 'translate_title_to_english' in source and 'def translate_title_to_english' in source:
                return idx, nb, source

def add_persistent_cache_to_translation(company):
    """Add persistent cache optimizations to translation cell"""
    nb_path = f'{company}/{company}_visualization.ipynb'
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    updated = False
    
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        
        source = ''.join(cell['source'])
        
        # Skip if already has persistent cache
        if "cache_file = 'translation_cache.json'" in source:
            continue
        
        # Find translation cells
        if 'translate_title_to_english' not in source or 'def translate_title_to_english' not in source:
            continue
        
        # This is a translation definition cell - add caching before the function
        lines = source.split('\n')
        insert_pos = 0
        
        # Find start of the function definition
        for i, line in enumerate(lines):
            if 'def translate_title_to_english' in line:
                insert_pos = i
                break
        
        # Create cache initialization code
        cache_init = '''import json
import os

# === PERSISTENT TRANSLATION CACHE ===
cache_file = 'translation_cache.json'
memory_cache = {}

def load_translation_cache():
    """Load cached translations from disk"""
    global memory_cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                memory_cache = json.load(f)
        except:
            memory_cache = {}
    else:
        memory_cache = {}

def save_translation_cache():
    """Save cache to disk to survive notebook restart"""
    global memory_cache
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(memory_cache, f, ensure_ascii=False, indent=2)
    except:
        pass

load_translation_cache()

'''
        
        # Insert cache initialization before function definition
        lines.insert(insert_pos, cache_init)
        
        # Now update the function body to use cache
        updated_source = '\n'.join(lines)
        
        # Replace function implementation to use persistent cache
        old_pattern = r'if title in translation_cache:\s*return translation_cache\[title\]'
        new_impl = '''if title in memory_cache:
        return memory_cache[title]'''
        updated_source = re.sub(old_pattern, new_impl, updated_source)
        
        # Update cache storage references
        updated_source = updated_source.replace(
            'translation_cache[title] = ',
            'memory_cache[title] = '
        )
        
        # Add periodic saves after cache updates
        updated_source = updated_source.replace(
            "memory_cache[title] = translated.strip()",
            """memory_cache[title] = translated.strip()
            if len(memory_cache) % 10 == 0:
                save_translation_cache()"""
        )
        
        # Update cell content
        cell['source'] = [line + '\n' for line in updated_source.split('\n')[:-1]] + [updated_source.split('\n')[-1]]
        updated = True
        break
    
    if updated:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False)
        return True
    
    return False

print("Applying persistent translation cache to company_a and company_u...\n")

for company in ['company_a', 'company_u']:
    print(f"Processing {company}...")
    try:
        if add_persistent_cache_to_translation(company):
            print(f"  ✅ Added persistent translation cache")
        else:
            print(f"  ℹ️  Already optimized or pattern not found")
    except Exception as e:
        print(f"  ⚠️  Error: {e}")

print("\nDone!")
