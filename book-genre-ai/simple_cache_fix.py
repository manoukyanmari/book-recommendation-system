#!/usr/bin/env python3
"""
Direct fix for persistent translation cache in company_a and company_u.
This replaces the simple dictionary initialization with persistent JSON-backed storage.
"""

import json

def update_translation_cache_simple(company):
    """Replace translation_cache = {} with persistent cache initialization"""
    nb_path = f'{company}/{company}_visualization.ipynb'
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    updated = False
    
    for idx, cell in enumerate(nb['cells']):
        if cell['cell_type'] != 'code':
            continue
        
        source = ''.join(cell['source'])
        
        # Skip if already has persistent cache code
        if 'cache_file' in source and 'json.load' in source:
            continue
        
        # Find cells with simple translation_cache = {}
        if 'translation_cache = {}' in source and 'prepare_title_for_emotion' in source:
            # This is the cell to update
            # Replace the simple dict initialization with persistent cache code
            
            new_source = source.replace(
                'translation_cache = {}',
                '''# Persistent cache that survives notebook restart
import json
import os

cache_file = 'translation_cache.json'
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            translation_cache = json.load(f)
    except:
        translation_cache = {}
else:
    translation_cache = {}

cache_save_counter = 0
def save_cache_if_needed():
    global cache_save_counter
    cache_save_counter += 1
    if cache_save_counter % 5 == 0:  # Save every 5 cache updates
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(translation_cache, f, ensure_ascii=False, indent=2)
        except:
            pass'''
            )
            
            # Also add cache saving after cache updates
            new_source = new_source.replace(
                'translation_cache[title] = (prepared_title, needs_translation, translated_ok)',
                '''translation_cache[title] = (prepared_title, needs_translation, translated_ok)
    save_cache_if_needed()'''
            )
            
            # Update the cell
            cell['source'] = [line + '\n' for line in new_source.split('\n')[:-1]] + [new_source.split('\n')[-1]]
            updated = True
            print(f"✅ Updated persistent cache in {company}")
            break
    
    if updated:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False)
        return True
    
    return False

print("="*60)
print("Applying persistent translation cache fix...")
print("="*60)

for company in ['company_a', 'company_u']:
    print(f"\n📝 Processing {company}... ", end="")
    try:
        if update_translation_cache_simple(company):
            print("done!")
        else:
            print("(pattern not found - may already be optimized)")
    except Exception as e:
        print(f"error: {e}")

print("\n" + "="*60)
print("✅ Translation cache optimization complete!")
print("="*60)
