
# Company A's Book Genre & Language Enrichment Pipeline

This project processes book sales data, detects languages, assigns genres using Open Library and AI classification, and generates an enriched CSV file with analytical summaries.

The pipeline is optimized with caching, parallel requests, and batch inference for performance and stability in large datasets.

---

## Overview

For each book title, the system:

- Deduplicates repeated titles
- Aggregates sales volume
- Detects language
- Retrieves subject metadata from Open Library
- Maps subjects to predefined genres
- Applies AI-based fallback classification when metadata is missing
- Generates summary statistics

---

## Features

- Duplicate title aggregation
- Unicode + statistical language detection
- Open Library subject enrichment
- Disk-backed API caching
- Automatic retries for network failures
- Batch AI classification
- Parallel metadata fetching
- Sales-weighted genre analytics
- Robust CSV parsing

---

## Input

### company_a.csv

| Column | Description              |
|--------|--------------------------|
| Title  | Book title               |
| Number | Sales count (SalesCount) |

---

## Output

### company_a_genres_output.csv

| Column   | Description             |
|----------|-------------------------|
| Title    | Normalized book title   |
| Number   | Aggregated sales volume |
| Language | Detected language       |
| Genres   | Top predicted genres    |

---

## Requirements

- pandas
- langid
- requests
- transformers
- torch
- tqdm

---

## Run

python main.py

---

## License

For academic and internal use.
