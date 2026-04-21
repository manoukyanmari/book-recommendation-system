
# Company A's Book Genre & Language Enrichment Pipeline

Welcome! This pipeline helps you understand your library's collection by automatically detecting which language each book is in and assigning relevant genres—even when that information isn't available in Open Library.

It's designed for checkout data and works by looking up what it can find, then using smart AI to fill in the gaps. The result: a richer, more organized view of your collection.

---

## What This Pipeline Does

**Simple version**: Takes your messy book list → adds languages & genres → gives you back a clean, enriched CSV.

**What happens inside:**
1. Deduplicates repeated titles (same book, multiple copies)
2. Aggregates checkout frequency (total times borrowed)
3. Detects language (English, French, Armenian, etc.)
4. Looks up genre info from Open Library API
5. Uses AI classification as a backup when Open Library doesn't have data
6. Generates a summary report showing what you learned

---

## Before You Start

### You Need These
- **company_a.csv** in this folder (with columns: Title, Number)
- Python 3.8+ installed on your machine
- Virtual environment activated (venv or conda)

### Install Dependencies
```bash
pip install pandas langid requests transformers torch tqdm
```

The pipeline will tell you if anything is missing and won't run until dependencies are ready.

---

## How to Run It

### Step 1: Prepare Your Data
Make sure `company_a.csv` is in this folder with exactly these columns:
- `Title` — the book name
- `Number` — how many times it was checked out

**Example:**
```
Title,Number
The Hunger Games,45
1984,32
Dune,28
```

### Step 2: Run the Genre Classifier
Open this notebook and run cells **in order** (top to bottom):

**File**: `company_a_genre_classifier.ipynb`

**Using VS Code**:
1. Click "Select Kernel" (top right) → choose your Python environment
2. Run Cell 1: *import statements & setup* (~2 seconds)
3. Run Cell 2: *process all books* (~2-10 minutes depending on dataset size & Open Library responsiveness)
4. Run Cell 3: *save results* (<1 second)
5. Final Cell: *display sample output* (instant)

**What to expect:**
```
Processing: 100%|████████| 234/234 [02:15<00:00, 1.73 books/s]
Writing output...
Saved: company_a_genres_output.csv
```

### Step 3: Check Your Output
Look for the new file: `company_a_genres_output.csv`

**Sample output** (first 3 rows):
```
Title,Number,Language,Genres
The Hunger Games,45,English,"dystopian, young-adult, science-fiction"
1984,32,English,"dystopian, political, classics"
Dune,28,English,"science-fiction, epic, fantasy"
```

---

## Understanding the Results

### Columns in Your Output

| Column | What It Means |
|--------|---|
| **Title** | Normalized book title (cleaned for consistency) |
| **Number** | Total checkout count from your data |
| **Language** | Detected language (English, French, Spanish, Armenian, etc.) |
| **Genres** | Top 3 genres assigned by Open Library or AI |

### What's Happening Behind the Scenes

**Caching**: Open Library API responses are saved locally (`openlibrary_cache.json`) so re-running is fast and doesn't re-query the same books.

**AI Fallback**: If Open Library doesn't have data for a book, the system uses zero-shot classification (distilbart-mnli-12-1) to predict genres from the title alone.

**Language Detection**: Uses both Unicode analysis and statistical methods for accuracy across multiple writing systems.

---

## Customization

### Change the Number of Genres
Want more or fewer genres per book? Open `company_a_genre_classifier.ipynb` and find this line:
```python
TOP_K_GENRES = 3  # Change 3 to how many you want
```
Then re-run the notebook.

### Clear the Cache (Start Fresh)
If you want to re-query Open Library instead of using saved data:
```bash
# Delete the cache file
rm openlibrary_cache.json
```
Then re-run the notebook.

### Filter by Language
After running the classifier, you can filter the output in another notebook:
```python
import pandas as pd

df = pd.read_csv("company_a_genres_output.csv")
english_books = df[df['Language'] == 'English']
english_books.to_csv("company_a_english_only.csv", index=False)
```

---

## Visualizing Your Data

**File**: `company_a_visualization.ipynb`

This notebook creates charts showing:
- Genre distribution (what types of books dominate?)
- Language breakdown (multilingual collection analysis)
- Checkout patterns by genre (what do patrons borrow most?)
- Top books by checkout frequency

Run it the same way as the classifier—cells in order, top to bottom.

---

## Troubleshooting

### Problem: "Module not found" error
**Solution**: Make sure you've installed dependencies:
```bash
pip install pandas langid requests transformers torch tqdm
```

### Problem: "Open Library API is slow"
**Solution**: This is normal—first run takes time as it queries the API for each unique title. Subsequent runs use the cache and are much faster.

**Speed it up**: Clear old cache and run only on a subset first to test.

### Problem: Some books getting weird genre assignments
**Solution**: This happens when:
- The book title is unusual or non-English
- Open Library doesn't have data, so AI makes a guess from the title alone
- Very short titles give the AI less information

You can manually override genres in the output CSV if needed for important titles.

### Problem: "TypeError" or "UnicodeDecodeError"
**Solution**: This usually means your company_a.csv has encoding issues. Try:
1. Open company_a.csv in VS Code
2. Click "UTF-8" in the bottom right → select "UTF-8" again to ensure encoding
3. Save and re-run

---

## Performance Notes

- **Small dataset** (100-300 books): ~1 minute
- **Medium dataset** (300-1000 books): ~3-5 minutes
- **Large dataset** (1000+ books): ~10-30 minutes (depends on API response times)

This includes cache hits for repeated titles. First-time queries are slower; re-runs are faster.

---

## What This Output Enables

**Collection Understanding**: See what you actually have (hidden language diversity, genre concentration)

**Smarter Recommendations**: With standardized genres, build recommendation systems or identify gaps

**Patron Insights**: Track what gets borrowed most—help inform purchasing decisions

**Accessibility Improvements**: Standardized genre labels make your catalog easier to browse

---

## Why This Matters for Your Library

Your book checkout data is valuable—it tells a story about what your patrons need. But that story is hidden in raw titles. This pipeline translates titles into structure:

*Before*: "The Hunger Games", "1984", "Dune" → just a list
*After*: Dystopian novels, most borrowed in young-adult genre, English-language dominated

With this structure, you can start answering real questions:
- "What modern science fiction do we have?"
- "Are we serving multilingual communities?"
- "Which genres drive the most checkouts?"

---

## A Word on the Data

The genres assigned here come from two sources:

1. **Open Library API**: A crowdsourced, free library database—comprehensive but sometimes incomplete
2. **AI Classification**: When Open Library is silent, we predict from context

Neither is perfect. Think of this as a strong *starting point*, not gospel truth. You know your collection best. If a genre assignment seems wrong, fix it.

---

## What You Can Do With This

This isn't just data processing—it's the foundation for real improvements:

**For Staff**: You can finally answer patron questions without guessing. "Do we have science fiction in French?" becomes answerable in seconds.

**For Management**: Numbers prove collection strategy. Show which genres drive the most checkouts. Make purchasing decisions data-backed instead of intuition-based.

**For Patrons**: Better browsing. When your catalog can be filtered by standardized genres, people actually find what they want. They come back more often.

**For Growth**: You now have the structure to build smarter recommendation systems, identify collection gaps, and understand hidden demand in your data.

---

## Keep Going

Getting here required real work—parsing messy data, running notebooks, handling failures, clearing caches. That's the unglamorous part of data work. But you did it.

Now the payoff comes. That enriched CSV? It's not the end product. It's the *beginning*.

Run the visualization. See your collection come alive as charts and numbers. Share what you find with your team. They'll be surprised. "Wait, we have *that* many multilingual books?" "Really, that genre gets borrowed three times more than I thought?"

Those moments—when hidden truth surfaces—that's when the work becomes valuable.

---

## A Word on the Data

One more honest thing: this system isn't magic. Open Library is incomplete. AI makes mistakes. Short or unusual titles confuse algorithms. Genre boundaries are fuzzy.

So treat this as a *starting point*, not gospel. You're the expert on your collection. If a classification seems wrong, fix it. If you notice patterns, dig deeper. The tool works best when humans stay in the loop.

---

## The Bigger Picture

Every data enrichment you do is an act of preservation. You're saying: "This collection matters. These checkouts mean something. These patrons' needs are worth understanding."

That's real work. Important work. The kind that makes libraries better.

Start small if you need to—test on a subset first, make sure it feels right for your unique collection. Then scale up. Build momentum. Each run teaches you something new about what you have.

---

## License

For academic and internal use.

---

**Built because understanding what libraries actually have matters.** Your data. Your story.
