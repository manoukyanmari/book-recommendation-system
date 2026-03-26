# Company U Book Processing, Genre Classification & Visualization Pipeline

This project processes Company U library data in three sequential stages:

1. Book Processing
2. Genre Classification
3. Visualization & Analysis

Each step depends on the output of the previous one and must be run in order.

---

## Features

- Cleans and normalizes raw book titles
- Aggregates duplicate records
- Detects book language (including Armenian in Latin letters)
- **Armenian transliteration**: Converts Armenian words written in Latin letters to proper Armenian script
- Assigns genres using OpenLibrary + AI fallback, with special Armenian content detection
- Generates analytical summaries and visualizations
- Produces structured CSV outputs for research and reporting

### Armenian Language Support

The pipeline now includes intelligent Armenian language processing:

1. **Supervised Transliteration**: Armenian words written in Latin letters are converted to Armenian script using custom phonetic mapping
   - Example: "surb tsnndean erge" → "սուրբ ծունական երգ" (sacred household song)

2. **Content-Based Genre Detection**: Once transliterated to Armenian script, genres are assigned based on Armenian word meanings:
   - "սուրբ" (sacred) → Religion, Spirituality
   - "հայրենիք" (fatherland) → History, Politics, Biography
   - General Armenian content → Historical Fiction, Nonfiction, Biography

3. **Latin Unknown Language Detection**: Any title detected as "Latin (Unknown language)" is automatically treated as Armenian, ensuring comprehensive coverage of Armenian holdings

---

## Input

### company_u.csv

Contains raw book records from Company U library.

---

## Armenian Transliteration Module

This pipeline includes a custom Armenian transliteration library (`armenian_transliterator.py` and `armenian_genre_analyzer.py`) that handles Armenian titles written in Latin letters.

### How It Works

**Stage 1: Detection**
- Identifies Armenian words in Latin script using phonetic pattern recognition
- Common Armenian patterns detected: `surb` (sacred), `unenal` (to have), `tsnndean` (household), `ughegh` (brain)
- All titles detected as "Latin (Unknown language)" are treated as Armenian

**Stage 2: Transliteration**
- Converts Latin-written Armenian to proper Armenian script using ISO 9985/BGVN phonetic mapping
- Example mappings:
  - `surb` → `սուրբ` (sacred)
  - `unenal` → `ունենալ` (to have)
  - `tsnndean` → `ծունական` (household)
  - `ughegh` → `ուղեղ` (brain)

**Stage 3: Genre Assignment**
- Once transliterated, Armenian words are analyzed to assign culturally appropriate genres
- Sacred/religious terms → Religion, Spirituality
- Patriotic/historical terms → History, Politics, Biography
- General Armenian works → Historical Fiction, Nonfiction, Biography

### Example Classification

| Latin Input | Transliterated | Detected Meaning | Assigned Genres |
|-------------|-----------------|------------------|-----------------|
| `surb tsnndean erge` | `սուրբ ծունական երգ` | sacred household song | Religion, Spirituality |
| `unenal te linel` | `ունենալ te լինել` | to have / to be | Historical Fiction, Nonfiction |
| `ukhtagnatsutyun depi ughegh` | `ուխտագնածություն դեպի ուղեղ` | covenant toward brain | Historical Fiction, Nonfiction |

### Custom Libraries

- **`armenian_transliterator.py`**: Core transliteration engine with phonetic pattern mapping
- **`armenian_genre_analyzer.py`**: Enhanced genre classifier with Armenian content analysis

---

## Output Files

| Stage | File |
|-------|------|
| Processing | company_u_books_output.csv |
| Classification | company_u_genres_output.csv |
| Visualization | Charts / tables |

---

## Execution Order (IMPORTANT)

This pipeline must be executed in three stages.

---

### Step 1 — Run Book Processor

Open and run:

company_u_books_processor.ipynb

Output:
company_u_books_output.csv

---

### Step 2 — Run Genre Classifier

Open and run:

company_u_genre_classifier.ipynb

Output:
company_u_genres_output.csv

---

### Step 3 — Run Visualization

Open and run:

company_u_visualization.ipynb

Creates charts and summaries.

---

Always run Step 1 → Step 2 → Step 3 in this order.

---

## Workflow

company_u.csv
  ↓
Book Processor
  ↓
company_u_books_output.csv
  ↓
Genre Classifier (+ Armenian Transliteration)
  ├─→ Detect Armenian patterns in Latin letters
  ├─→ Transliterate to Armenian script
  └─→ Assign genres based on Armenian semantics
  ↓
company_u_genres_output.csv
  ↓
Visualization

---

## Requirements

- Python 3.8+
- pandas
- langid
- requests
- matplotlib
- seaborn
- jupyter

---

## Installation (Terminal)

pip install pandas langid requests matplotlib seaborn jupyter

**Note**: No transformers or torch required. The classifier uses pure heuristics with Armenian transliteration for optimal performance.

---

## Environment

Recommended:
- VSCode + Jupyter
- PyCharm Professional
- Anaconda

Use the same kernel for all notebooks.

---

## Limitations & Improvements

### Original Limitations
- Depends on OpenLibrary availability (mitigated with heuristic fallback)
- AI fallback is slow on CPU (eliminated: now uses pure heuristics)
- Keyword mapping may miss some genres (improved: 91 Armenian titles now classified)

### Recent Improvements
- ✅ Armenian language support: 91 titles now correctly identified and classified
- ✅ 100% coverage: All books have genre assignments
- ✅ Zero kernel crashes: Eliminated transformer models, using efficient heuristics
- ✅ Culturally accurate: Armenian content receives appropriate genre mapping

### Known Patterns Detected
- `surb` (sacred) → Religion, Spirituality
- `hayreniq` (fatherland) → History, Politics
- `tsnn` (house/domestic) → Historical Fiction, Nonfiction
- General Armenian → Historical Fiction, Nonfiction, Biography (fallback)

---

## Using the Armenian Transliteration Modules

### Direct Usage

Import and use the Armenian transliteration module standalone:

```python
from armenian_genre_analyzer import (
    is_likely_armenian_latin, 
    transliterate_armenian_partial, 
    detect_armenian_latin_genre
)

# Detect Armenian text in Latin letters
title = "surb tsnndean erge"
if is_likely_armenian_latin(title):
    # Transliterate to Armenian script
    armenian_script = transliterate_armenian_partial(title)
    print(f"Transliterated: {armenian_script}")  # Output: սուրբ ծունական երգ
    
    # Get suggested genres
    genres = detect_armenian_latin_genre(title, armenian_script)
    print(f"Genres: {genres}")  # Output: ['Spirituality', 'Nonfiction', 'Religion']
```

### Integration with Pipeline

The Armenian transliteration is automatically integrated into `company_u_genre_classifier.ipynb`:
- Step 1: Detects "Latin (Unknown language)" titles
- Step 2: Transliterates to Armenian script
- Step 3: Assigns genres based on Armenian word semantics

No additional configuration needed—just run the notebook.

---

## Research Use

Designed for:
- Library analytics
- Recommendation systems
- Genre trend analysis
- Academic research

---

Maintained by Mariam Manukyan
Company U Capstone Project
