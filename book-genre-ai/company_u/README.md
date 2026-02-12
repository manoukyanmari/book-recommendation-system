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
- Detects book language
- Assigns genres using OpenLibrary + AI fallback
- Generates analytical summaries and visualizations
- Produces structured CSV outputs for research and reporting

---

## Input

### company_u.csv

Contains raw book records from Company U library.

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
Genre Classifier
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
- transformers
- torch
- matplotlib
- seaborn
- jupyter

---

## Installation (Terminal)

pip install pandas langid requests transformers torch matplotlib seaborn jupyter

---

## Environment

Recommended:
- VSCode + Jupyter
- PyCharm Professional
- Anaconda

Use the same kernel for all notebooks.

---

## Limitations

- Depends on OpenLibrary availability
- AI fallback is slow on CPU
- Keyword mapping may miss some genres

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
