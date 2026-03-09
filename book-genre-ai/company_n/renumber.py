import json

with open('company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

updates = {
    'Language Distribution Chart': '1. Language Distribution Chart',
    'Genre Volume Analysis': '2. Genre Volume Analysis',
    '## 1. Structural Feature Engineering': '## 3. Structural Feature Engineering',
    '## 3. Lexical Analysis': '## 4. Lexical Analysis',
    '### 3.1.': '### 4.1.',
    '### 3.2.': '### 4.2.',
    '### 3.3.': '### 4.3.',
    '## 4. Semantic': '## 5. Semantic',
    '### 4.1. Sentiment': '### 5.1. Sentiment',
    '### 4.2. Emotional': '### 5.2. Emotional',
    '## 5. Topic Modeling': '## 6. Topic Modeling',
    '## 6. DISTRIBUTION ANALYSIS': '## 7. DISTRIBUTION ANALYSIS',
    'Summary Statistics': '8. Summary Statistics',
}

for cell in nb['cells']:
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source']) if isinstance(cell['source'], list) else cell['source']
        for old, new in updates.items():
            if old in source:
                new_source = source.replace(old, new)
                cell['source'] = new_source.split('\n')
                print(f"Updated: {old} -> {new}")

with open('company_n_visualization.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Renumbering complete!")
