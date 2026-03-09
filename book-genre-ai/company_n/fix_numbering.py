import json

with open('company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

updates = {
    '## 2. Language Distribution Chart': '## Language Distribution Chart',
    '## 4. Genre Volume Analysis': '## Genre Volume Analysis',
    '## 5. Summary Statistics': '## Summary Statistics',
    '## 2. Lexical Analysis': '## 3. Lexical Analysis',
    '### 2.1. Tokenization': '### 3.1. Tokenization',
    '### 2.2. Frequency': '### 3.2. Frequency',
    '### 4.1. Part-of-Speech': '### 3.3. Part-of-Speech',
    '## 3. Semantic': '## 4. Semantic',
    '### 3.1. Sentiment': '### 4.1. Sentiment',
    '### 3.2. Emotional': '### 4.2. Emotional',
    '## 4. Topic Modeling': '## 5. Topic Modeling',
    '## 5. DISTRIBUTION ANALYSIS': '## 6. DISTRIBUTION ANALYSIS',
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

print("Fixed!")
