import json

with open('company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Correct numbering - remove numbers from first two, renumber the rest
updates = {
    '## 1. Language Distribution Chart': '## Language Distribution Chart',
    '## 2. Genre Volume Analysis': '## Genre Volume Analysis',
    '## 3. Structural Feature Engineering': '## 1. Structural Feature Engineering',
    '### 1.1.': '### 1.1.',  # Keep as is - subsection of section 1
    '### 1.2.': '### 1.2.',  # Keep as is
    '### 1.3.': '### 1.3.',  # Keep as is
    '## 4. Lexical Analysis': '## 2. Lexical Analysis',
    '### 4.1.': '### 2.1.',
    '### 4.2.': '### 2.2.',
    '### 4.3.': '### 2.3.',
    '## 5. Semantic': '## 3. Semantic',
    '### 5.1. Sentiment': '### 3.1. Sentiment',
    '### 5.2. Emotional': '### 3.2. Emotional',
    '## 6. Topic Modeling': '## 4. Topic Modeling',
    '## 7. DISTRIBUTION ANALYSIS': '## 5. DISTRIBUTION ANALYSIS',
    '## 8. Summary Statistics': '## Summary Statistics',
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

print("Fixed ordering!")
