
# Company N Book Genre & Language Enrichment Pipeline

This pipeline processes Company N transaction-style book data, normalizes and deduplicates titles, detects language, assigns genres using Open Library metadata with an AI fallback, and exports an enriched CSV with summary analytics and visualizations.

It is optimized for repeated runs using disk-backed caching, request retries, parallel Open Library lookups, and batched zero-shot classification.

---

## Overview

The workflow consists of two main stages:

1. Genre & language classification
2. Visualization and analysis

The classification stage must always be executed before visualization.

---

## Input

### `company_n.csv`

Required columns:

| Column     | Description |
|------------|-------------|
| Date       | Transaction date (not used in aggregation) |
| Book Names | Raw book title string |

**How `Number` is computed:**  
`Number` is derived by counting how many rows each title appears in (frequency / sales count proxy).

---

## Title Normalization (Deduplication Key)

Before aggregation, titles are cleaned to prevent duplicate entries caused by formatting differences:

- Trim leading/trailing whitespace
- Collapse multiple spaces
- Convert to lowercase
- Remove punctuation and symbols
- Unicode normalization (`NFKC`)

The cleaned value (`CleanTitle`) is used for grouping and saved as `Title` in the output.

---

## Output

### `company_n_genres_output.csv`

Columns:

| Column   | Description |
|----------|-------------|
| Title    | Normalized book title |
| Number   | Frequency count |
| Language | Detected language |
| Genres   | Top-K predicted genres |

The output ends with:

- One empty row
- One `SUMMARY` row containing:
  - Top genres by title count
  - Top genres by total `Number`

---

## Genre Taxonomy

The system predicts from the following genres:

- Fantasy
- Science Fiction
- Romance
- Mystery
- Thriller
- Historical Fiction
- Nonfiction
- Biography
- Young Adult
- Horror

---

## How Genres Are Assigned

1. **Open Library (Primary Source)**
   - Searches by title
   - Extracts subject metadata
   - Maps subjects to genres using keywords

2. **AI Fallback (When Metadata Is Missing)**
   - Zero-shot classification using `valhalla/distilbart-mnli-12-1`
   - Runs in batches
   - Uses GPU if available, otherwise CPU

---

## Caching

Open Library responses are cached locally:

```
company_n_openlibrary_cache.json
```

This improves performance on repeated runs.

---

## Requirements

Python 3.8+

Packages:

- pandas
- langid
- requests
- transformers
- torch
- matplotlib
- seaborn
- tqdm
- urllib3

---

## Installation (Terminal)

From the project folder:

```bash
python3 -m pip install pandas langid requests transformers torch matplotlib seaborn tqdm
```

If using a virtual environment:

```bash
source .venv/bin/activate
pip install pandas langid requests transformers torch matplotlib seaborn tqdm
```

---

## Execution Order (Important)

This project must be executed in two stages.

---

### Step 1 — Run Genre Classification

Run the classifier notebook first:

```
company_n_genre_classifier.ipynb
```

Run all cells in order.

This generates:

```
company_n_genres_output.csv
```

Do NOT skip this step.

---

### Step 2 — Run Visualization & Analysis

After Step 1 finishes, open and run:

```
company_n_visualization.ipynb
```

This notebook loads `company_n_genres_output.csv` and produces plots and statistics.

---

⚠️ Running the visualization before classification will result in errors.

---

## Workflow

```
company_n.csv
   ↓
company_n_genre_classifier.ipynb
   ↓
company_n_genres_output.csv
   ↓
company_n_visualization.ipynb
```

---

## Configuration

Editable constants in the classifier script:

```python
COMPANY_N_FILE = "company_n.csv"
OUTPUT_COMPANY_N = "company_n_genres_output.csv"
TOP_K_GENRES = 3
OPENLIBRARY_CACHE_FILE = "company_n_openlibrary_cache.json"
```

---

## Performance

Optimizations used:

- Disk-backed caching
- Threaded Open Library requests
- Batched AI classification
- Lazy model loading

---

## Limitations

- Depends on Open Library availability
- AI fallback is slow on CPU
- Genre mapping is keyword-based
- Internet required on first run
- Non-English titles may have reduced accuracy

---

## Example Output

```csv
Title,Number,Language,Genres
the hobbit,12,English,"Fantasy, Young Adult"
...
SUMMARY,8452,,"Top genres by title count: [('Fantasy', 42)]. Top genres by total Number: [('Fantasy', 3240)]."
```

---

## License

For academic and internal use.
Adapt as needed for commercial deployment.
