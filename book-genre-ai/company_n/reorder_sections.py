import json

with open('company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find all section markers
sections = {
    'structural': None,
    'lang_dist': None,
    'genre_vol': None,
    'lexical': None,
    'semantic': None,
    'topic': None,
    'distribution': None,
    'summary': None,
}

for i, cell in enumerate(cells):
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        if '## 1. Structural Feature Engineering' in source:
            sections['structural'] = i
        elif '## Language Distribution Chart' in source:
            sections['lang_dist'] = i
        elif '## Genre Volume Analysis' in source:
            sections['genre_vol'] = i
        elif '## 2. Lexical Analysis' in source:
            sections['lexical'] = i
        elif '## 3. Semantic' in source:
            sections['semantic'] = i
        elif '## 4. Topic Modeling' in source:
            sections['topic'] = i
        elif '## 5. DISTRIBUTION ANALYSIS' in source:
            sections['distribution'] = i
        elif '## Summary Statistics' in source:
            sections['summary'] = i

print("Section markers found at:")
for name, idx in sections.items():
    if idx is not None:
        print(f"  {name}: cell {idx}")

# Extract sections based on current positions
setup = cells[0:sections['structural']]
structural = cells[sections['structural']:sections['lang_dist']]
lang_dist = cells[sections['lang_dist']:sections['genre_vol']]
genre_vol = cells[sections['genre_vol']:sections['lexical']]
lexical = cells[sections['lexical']:sections['semantic']]
semantic = cells[sections['semantic']:sections['topic']]
topic = cells[sections['topic']:sections['distribution']]
distribution = cells[sections['distribution']:sections['summary']]
summary = cells[sections['summary']:]

# Reorder to: setup → lang_dist → genre_vol → structural → lexical → semantic → topic → distribution → summary
nb['cells'] = setup + lang_dist + genre_vol + structural + lexical + semantic + topic + distribution + summary

with open('company_n_visualization.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✅ Cells reordered successfully!")
print(f"New order:")
print(f"  Setup: {len(setup)} cells")
print(f"  Language Distribution: {len(lang_dist)} cells")
print(f"  Genre Volume: {len(genre_vol)} cells")
print(f"  Structural: {len(structural)} cells")
print(f"  Lexical: {len(lexical)} cells")
print(f"  Semantic: {len(semantic)} cells")
print(f"  Topic: {len(topic)} cells")
print(f"  Distribution: {len(distribution)} cells")
print(f"  Summary: {len(summary)} cells")
print(f"  Total: {sum([len(setup), len(lang_dist), len(genre_vol), len(structural), len(lexical), len(semantic), len(topic), len(distribution), len(summary)])} cells")
