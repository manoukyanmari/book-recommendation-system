import json
import re

# Read the notebook
with open('book-genre-ai/company_n/company_n_visualization.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# Function to remove emojis
def remove_emojis(text):
    # Remove emojis and special unicode characters
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"  # Enclosed characters
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols Extended-A
        "\u200d"  # Zero Width Joiner
        "\u2640-\u2642"  # Gender
        "\u2600-\u2B55"  # Misc symbols
        "\u200c-\u200d"  # Zero-width characters
        "\u23e9-\u25b6"  # Media
        "\u231a-\u231b"  # Watches
        "\ufe0f"  # Dingbats
        "\u3030"  # Wavy dash
        "]+"
    , flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Process all cells
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        # Process source
        if isinstance(cell['source'], list):
            cell['source'] = [remove_emojis(line) for line in cell['source']]
        else:
            cell['source'] = remove_emojis(cell['source'])
        
        # Process output if it exists
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    if isinstance(output['text'], list):
                        output['text'] = [remove_emojis(line) for line in output['text']]
                    else:
                        output['text'] = remove_emojis(output['text'])
    
    elif cell['cell_type'] == 'markdown':
        # Process markdown cells
        if isinstance(cell['source'], list):
            cell['source'] = [remove_emojis(line) for line in cell['source']]
        else:
            cell['source'] = remove_emojis(cell['source'])

# Write the notebook back
with open('book-genre-ai/company_n/company_n_visualization.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)

print("All emojis removed successfully!")
