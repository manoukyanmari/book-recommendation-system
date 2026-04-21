
# Company N Book Genre & Language Enrichment Pipeline

Automatically analyze Company N's book collection to discover:
- **What genres** patrons are reading most
- **What languages** are represented
- **How popular** each book is (by checkout frequency)

Two steps: Classify genres → Visualize results

All done with smart caching and AI fallback, so it's fast even on large datasets.

---

## Two Simple Steps

1. **Classify**: Analyze all books, detect language, assign genres → CSV file
2. **Visualize**: Create charts and statistics from the CSV → Pretty pictures

Always do both, always in this order.

---

## Input Data

**File**: `company_n.csv`

**Expected columns**:
- `Date` — When the book was checked out (not used for analysis, just stored)
- `Book Names` — The actual book title

**Example**:
```
Date,Book Names
2024-01-15,The Great Gatsby
2024-01-16,To Kill a Mockingbird
2024-01-16,The Great Gatsby
```

**How frequency is calculated**:
- Count how many rows each title appears in
- "The Great Gatsby" appears 2 times → marked as 2 checkouts
- System automatically removes duplicates caused by formatting (different spaces, capitalization, punctuation)

---

## How Duplicates Are Removed (Title Cleanup)

**Problem**: Same book appears with slight variations:
- `"  The Hobbit  "` (extra spaces)
- `"the hobbit"` (lowercase)  
- `"The Hobbit."` (period at end)
- `"the-hobbit"` (dash instead of space)

**Solution**: System cleans all titles the same way:
1. Remove extra spaces
2. Make lowercase
3. Remove punctuation
4. Normalize special characters
5. Count by cleaned title → eliminates duplicates

**Result**: `Company N` books get merged and counted together, 1 row per unique title in output

---

## Output Data

**File created**: `company_n_genres_output.csv`

**Columns**:

| Column | Meaning |
|--------|---------|
| `Title` | The cleaned book title |
| `Number` | How many times checked out |
| `Language` | English, Spanish, Armenian, etc. |
| `Genres` | Top genres (e.g., "Fantasy, Young Adult") |

**Plus at the bottom**:
- Empty row (just for spacing)
- `SUMMARY` row with overall stats (top genres, totals, etc.)

---

## Available Genres

The system can assign these genres:

Fantasy, Science Fiction, Romance, Mystery, Thriller, Historical Fiction, Nonfiction, Biography, Young Adult, Horror

(Change which genres are used by editing the `GENRES_LIST` in the classifier if needed)

---

## How Genres Are Assigned

**First choice: Ask Open Library**
- System searches Open Library for the book
- If found → Uses their genre data
- If not found → Falls back to AI

**Second choice: AI Guess (If Open Library doesn't know)**
- Uses AI model trained to classify text
- Reads the title and figures out the genre
- Works for books Open Library hasn't cataloged

**Result**: Every book gets 1-3 genres (you set how many in configuration)

---

## Caching (Why Second Run Is Faster)

**First time you run**:
- System queries Open Library for each book
- Takes a minute or more (depending on internet speed and dataset size)
- Saves results to: `company_n_openlibrary_cache.json`

**Second time you run**:
- System reads from cache file instead of querying Open Library again
- Takes 5-10 seconds (much faster!)

**To clear cache and start fresh**:
- Delete the file: `company_n_openlibrary_cache.json`
- Next run will rebuild it

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

## Setup Before Running

**1. Activate Python environment** (in Terminal):
```bash
cd /Users/mariammanukyan/Desktop/book-recommendation
source .venv/bin/activate
```
You'll see `(.venv)` prefix if it worked

**2. Install required packages** (if first time):
```bash
pip install pandas langid requests transformers torch matplotlib seaborn tqdm
```

**3. Verify data file exists**:
- Open `book-genre-ai/company_n/` in VS Code
- You should see: `company_n.csv`
- If missing, ask where the data file is

---

## How to Run (Step-by-Step)

### Step 1: Run Genre Classification

**Why**: This analyzes all books, detects languages, and assigns genres. Must run first.

**How**:

1. **Open the notebook**:
   - In VS Code, navigate to: `book-genre-ai/company_n/`
   - Double-click: `company_n_genre_classifier.ipynb`

2. **Run all cells** (click **"Run All"** at top, or press `Ctrl+Shift+Enter`):
   - Processing starts (may take 30 seconds to a few minutes depending on dataset)
   - Watch for progress messages like:
     ```
     Processing titles...
     Querying Open Library...
     Running AI fallback...
     Classification complete!
     ```
   - Finally see: `"Output saved: company_n_genres_output.csv"`

3. **What was created**:
   - File: `company_n_genres_output.csv` (book list with genres)
   - File: `company_n_openlibrary_cache.json` (cached API results for speed)

**If it fails**:
- Error about missing packages? → Run the setup above and try again
- Stuck or very slow? → You can interrupt (`Ctrl+C`) and try again later
- No "Output saved" message? → Scroll up to check for errors

---

### Step 2: Run Visualization & Analysis

**Why**: Creates charts and summary statistics from the classified data.

**How**:

1. **Open the notebook**:
   - Navigate to: `book-genre-ai/company_n/`
   - Double-click: `company_n_visualization.ipynb`

2. **Run all cells** (click **"Run All"** or `Ctrl+Shift+Enter`):
   - Processing starts (usually 5-10 seconds)
   - Watch for output messages
   - Charts and tables appear in the notebook

3. **What you should see**:
   - Genre distribution pie chart
   - Language breakdown bar chart
   - Top books by frequency table
   - Summary statistics

**If it fails**:
- Error: "company_n_genres_output.csv not found" → You skipped Step 1! Run it first.
- Other errors? → Make sure Step 1 completed successfully

---

**Important**: Always do Step 1 first, then Step 2. Don't skip or reverse the order.

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

## Customization (Optional)

Want to change settings? You can **edit constants** in the classifier notebook:

**Open**: `company_n_genre_classifier.ipynb`

**Look for the code cell** with these lines (near the top):
```python
COMPANY_N_FILE = "company_n.csv"              # Input data file
OUTPUT_COMPANY_N = "company_n_genres_output.csv"  # Output filename
TOP_K_GENRES = 3                              # How many genres per book
OPENLIBRARY_CACHE_FILE = "company_n_openlibrary_cache.json"  # Cache file
```

**You can change**:
- `COMPANY_N_FILE`: Use a different input CSV file
- `TOP_K_GENRES`: Predict 2, 3, 4, or 5 genres per book (default: 3)
- `OUTPUT_COMPANY_N`: Name the output file differently

**How to change**:
1. Click in the cell to edit
2. Modify the value (keep the quotes around filenames)
3. Save the notebook file
4. Run all cells again

**Example**:
```python
TOP_K_GENRES = 5  # Now predict 5 genres instead of 3
```

Then run cells → Output will include 5 genres per book instead of 3

---

## How It Works (Behind the Scenes)

**Speed tips**:
- First run: Slower (queries Open Library, builds cache)
- Later runs: Much faster (uses cached results from `company_n_openlibrary_cache.json`)
- Uses parallel requests to Open Library (faster than one-by-one)
- AI fallback runs in batches (uses GPU if available)

**Practical times**:
- 100 books: 10-20 seconds
- 500 books: 30-60 seconds  
- 1000+ books: 1-3 minutes

---

## Known Limitations (And Workarounds)

| Limitation | What Happens | How to Work Around |
|-----------|-------------|------------------|
| Open Library down | Slower classification | System has built-in retries; if still slow, run again later |
| Very old/rare books | Genre may be wrong | Try manual correction in output CSV |
| Non-English titles | Lower accuracy | System still works; accuracy better for popular titles |
| First run slow | Takes longer (no cache yet) | Repeat runs are faster; cache adds speed |
| AI fallback on CPU | Can be slow | Let it finish; GPU is much faster if available |

---

---

## Example: What Your Output Looks Like

**File**: `company_n_genres_output.csv`

```csv
Title,Number,Language,Genres
the hobbit,12,English,"Fantasy, Young Adult"
pride and prejudice,8,English,"Romance, Historical Fiction"
dune,15,English,"Science Fiction, Fantasy"
...
SUMMARY,847,,"Top genres: Fantasy (142 titles, 3240 checkouts). Romance (89 titles, 1950 checkouts). Others..."
```

**Breakdown**:
- **Title**: Cleaned book title
- **Number**: How many times this book was checked out
- **Language**: What language it was detected as
- **Genres**: Top genres assigned (you chose 3 as default, can change)
- **SUMMARY**: Last row shows overall statistics

---

## What This Is For

Use this pipeline when you need to:
- Understand what genres your patrons are reading
- Categorize books automatically (faster than manual tagging)
- Track language diversity in the collection
- Generate report summaries for management
- Prepare data for recommendation systems

---

## Questions or Issues?

**The process feels slow**: First run queries Open Library (normal). Second run uses cache (much faster).

**Output looks wrong**: Rare books may have incorrect genres. Check Open Library directly for these titles.

**Want different genres per book**: Change `TOP_K_GENRES` in the configuration above, then re-run.

**Need a fresh start**: Delete the cache file (`company_n_openlibrary_cache.json`) and run again.

---

## Why This Matters

Understanding your collection isn't about data for data's sake. It's about answers:

- **What are patrons actually reading?** Not what *should* be popular, but what *is*. Real choices reveal real interests.
- **Are we serving all language communities?** Books are gateways. Knowing what languages are in your collection means knowing who you're reaching.
- **Which books drive the most engagement?** Two copies of a book checked out 50 times tells a different story than 50 books checked out once each.

This tool turns transaction logs into insights. It takes the raw data of who borrowed what and reveals patterns that matter.

---

## What You Can Do With This

**For collection decisions**:
- Which genres to expand? Follow the checkout patterns.
- Where to focus budget? Popular books that drive engagement.
- What's underrepresented? Genre gaps and language gaps jump out of the data.

**For library management**:
- Show patrons what's popular right now
- Report to stakeholders on collection diversity
- Justify acquisitions and budget requests with data

**For planning**:
- Discover gaps (is there really no mystery fiction getting checked out?)
- Track changes over time (run this monthly and see trends)

---

## A Word on the Data

The genres come from Open Library, which is crowdsourced and sometimes incomplete. If a rare or new book gets miscategorized, that's Open Library's limitation, not a bug here. The AI fallback helps fill gaps, but it's not magic—it makes educated guesses based on titles.

That said, even imperfect categorization is useful. You get the rough picture, and that's often enough to make good decisions.

---

## Keep Going

This is a starting point. Once you understand your collection:
- Use these insights for reader recommendations
- Plan themed events around popular genres
- Advocate for underrepresented collections
- Share results with your community

The tools are here. The data is yours. What you do with it is up to you.

---

*Built for understanding libraries better.*  
*For Company N, and any library that wants to know their patrons.*
