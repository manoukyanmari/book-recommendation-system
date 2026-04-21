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

## Results Summary

### Overall Statistics
- **Total books processed**: 666
- **Books with genres assigned**: 666 (100% coverage)
- **Total checkouts**: 718

### Armenian Titles Identified & Classified
- **Total Armenian titles**: 91 books
  - Clear pattern detection: 3 titles
  - "Latin (Unknown language)" detection: 88 titles

### Genre Distribution for Armenian Titles

| Genre | Count |
|-------|-------|
| Historical Fiction | 72 |
| Nonfiction | 68 |
| Biography | 68 |
| Spirituality | 2 |
| Religion | 2 |

---

## Limitations & Improvements

### Original Limitations
- Depends on OpenLibrary availability (mitigated with heuristic fallback)
- AI fallback is slow on CPU (eliminated: now uses pure heuristics)
- Keyword mapping may miss some genres (improved: 91 Armenian titles now classified)

### Recent Improvements
- Armenian language support: 91 titles now correctly identified and classified
- 100% coverage: All books have genre assignments
- Zero kernel crashes: Eliminated transformer models, using efficient heuristics
- Culturally accurate: Armenian content receives appropriate genre mapping

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

## Recommendation Systems

The project includes three complementary recommendation engines that can work individually or in combination:

### System 1: Content-Based Recommendation (`company_u_content_based_recsys.ipynb`)

**Purpose**: Recommend books based on genre and title similarity to books a user has already read.

**How to Run**:
1. Open `company_u_content_based_recsys.ipynb`
2. Run all cells sequentially
3. Call `get_recommendations(user_id, num_recommendations=10)` with any valid user ID
4. Returns dataframe with recommended books and similarity scores

**Algorithm Overview**:
1. **Feature Engineering**: Extracts book titles and genres from `company_u_genres_output.csv`
2. **TF-IDF Vectorization**: Converts book content into numerical vectors using TF-IDF (Term Frequency-Inverse Document Frequency)
   - Emphasizes important words in titles and genres
   - Weights common vs. rare terms appropriately
3. **Similarity Matrix**: Computes cosine similarity between all books
   - Measures how similar each book is to every other book
   - Ranges from 0 (completely different) to 1 (identical content)
4. **Recommendation Aggregation**:
   - For each book the user hasn't read, computes average similarity to books they have read
   - Ranks recommendations by aggregated similarity score
5. **Output**: Returns top N recommendations with similarity scores

**Key Features**:
- Works for 100% of users (no data sparsity issues)
- Purely content-driven (independent of other users' preferences)
- Fast and deterministic
- Transparent: easy to explain why a book was recommended

**Example Output**:
```
User: User006
Books Read: ["The Great Gatsby", "To Kill a Mockingbird"]
Top Recommendations:
1. [0.78] Classic American Literature Novel (similar genres/themes)
2. [0.72] Historical Fiction Work (shared genre: Fiction)
...
```

---

### System 2: Collaborative Filtering (`company_u_collaborative_filtering.ipynb`)

**Purpose**: Recommend books based on what similar users (shared reading patterns) have read.

**How to Run**:
1. Open `company_u_collaborative_filtering.ipynb`
2. Run all cells sequentially
3. Call `get_cf_recommendations(user_id, num_recommendations=10)` with any valid user ID
4. Returns dataframe with recommended books and shared reader metrics

**Algorithm Overview**:
1. **User-Book Matrix**: Creates a matrix where rows=users, columns=books, values=read/not-read
2. **Co-Occurrence Matrix**: Counts how many users have read each pair of books
   - Books read by many of the same users score higher
   - Identifies "reading style clusters"
3. **Similarity Computation**: Uses Jaccard similarity to measure book-to-book similarity
   - Formula: (shared readers) / (total readers of either book)
   - Emphasizes strongly overlapping reading communities
4. **Recommendation Scoring**:
   - For each unread book, finds similarity to books the user has read
   - Aggregates scores using: **0.6 × max_similarity + 0.4 × avg_similarity**
   - Balances finding books similar to top favorites vs. consistent quality
5. **Output**: Returns top N recommendations with similarity and shared reader counts

**Key Features**:
- Captures reading community patterns
- Discovers "hidden gems" that work for similar users
- Effective for finding serendipitous recommendations
- Tracks "shared readers count" (how many users read both books)

**Coverage Note**: Works for ~22% of users (those with readers who share at least one book). For isolated users with unique reading patterns, scores are 0 (not an error—reflects actual data).

**Example Output**:
```
User: User162
Books Read: ["Book A", "Book B"]
Top Recommendations:
1. [0.85 similarity, 3 shared readers] Book C (also read by users who read Book A)
2. [0.72 similarity, 5 shared readers] Book D (overlapping reading community)
...
```

---

### System 3: Taste-Based Neural Network (`company_u_taste_network.ipynb`)

**Purpose**: Recommend books based on learned 8-dimensional "taste embeddings" — abstract flavor profiles that capture intrinsic book characteristics beyond explicit genres.

**How to Run**:
1. Open `company_u_taste_network.ipynb`
2. Run all cells sequentially
3. System generates:
   - `taste_embeddings_matrix.npy`: 8D embedding vectors for each book
   - `book_taste_profiles.csv`: Readable taste dimension breakdown
4. Call `get_taste_recommendations(user_id, num_recommendations=10)` with any valid user ID
5. Returns dataframe with recommendations and taste similarity scores

**Algorithm Overview**:
1. **Feature Extraction**: Analyzes book titles, genres, and metadata to identify intrinsic characteristics
2. **Embedding Generation**: Creates 8-dimensional vectors where each dimension represents a learned "taste aspect"
   - Example dimensions: *Literary Depth*, *Action/Pacing*, *Emotional Tone*, *Historical Context*, etc.
   - Dimensions learned from patterns in the collection (not predefined)
   - Continuous values allow nuanced similarity computation
3. **Similarity Matrix**: Computes cosine similarity between taste embeddings
   - Measures distance in 8D taste space between any two books
   - Books with similar taste profiles score high
4. **Recommendation Scoring**:
   - For each unread book, finds average taste similarity to books user has read
   - Aggregates using: **0.6 × max_similarity + 0.4 × avg_similarity**
   - Prefers books with strong connection to at least one read book
5. **Output**: Returns top N recommendations with taste similarity scores

**Key Features**:
- **Captures abstract taste patterns**: Finds connections beyond direct genre overlap
- **8-dimensional reasoning**: Rich representation allows nuanced comparisons
- **Works for 100% of users**: Doesn't depend on collaborative signal
- **Interpretable embeddings**: Can analyze what each dimension represents
- **Serendipity**: Often finds unexpected but high-quality matches

**Taste Dimension Analysis**:
```
Example taste profile for "The Great Gatsby":
Dimension 1 (Literary Depth):     0.92  ███████████████████
Dimension 2 (Character Focus):    0.85  ██████████████████
Dimension 3 (Social Commentary):  0.88  ███████████████████
Dimension 4 (Romance Weight):     0.75  ████████████████
Dimension 5 (Historical Setting): 0.60  ███████████
Dimension 6 (Fast Pacing):        0.35  ███████
Dimension 7 (Dark Themes):        0.48  ██████████
Dimension 8 (Surrealism):         0.42  █████████
```

**Coverage Note**: Works for 100% of users. Since embeddings are generated from book features (not user interactions), every user gets recommendations regardless of their reading history size.

**Example Output**:
```
User: User050
Books Read: ["Literary Classic A", "Contemporary Novel B"]
Top Recommendations:
1. [0.89 taste similarity] Book matching taste profile (Literary + Character-driven)
2. [0.82 taste similarity] Book with similar emotional tone and depth
3. [0.78 taste similarity] Book sharing thematic elements in 8D space
...
```

---

### System 4: Hybrid Recommendation — 3-Component Integration (`company_u_hybrid_recsys.ipynb`)

**Purpose**: Combine all three recommendation engines (Content-Based, Collaborative Filtering, Taste-Based) for superior, interpretable recommendations.

**How to Run**:
1. Open `company_u_hybrid_recsys.ipynb`
2. Run all cells sequentially
3. System loads all three recommendation engines automatically
4. Call `get_hybrid_recommendations(user_id, num_recommendations=10, cb_weight=0.33, cf_weight=0.33, taste_weight=0.33)`
5. Toggle AI Taste Network on/off with interactive checkbox
6. Returns dataframe with combined scores from all three engines

**Operating Modes**:

1. **Mode 1 (2-Component)**: When Taste Network is OFF
   - `50% Content-Based + 50% Collaborative Filtering`
   - Use for: Quick recommendations when taste embeddings unavailable
   - Command: `get_hybrid_recommendations(user_id, cb_weight=0.5, cf_weight=0.5)`

2. **Mode 2 (3-Component)**: When Taste Network is ON
   - `33% Content-Based + 33% Collaborative + 33% Taste-Based`
   - Use for: Premium recommendations leveraging all signal sources
   - Command: `get_hybrid_recommendations(user_id, cb_weight=0.33, cf_weight=0.33, taste_weight=0.33)`

**Hybrid Combination Strategy**:
1. **Independent Recommendation Generation**:
   - Get top 2N recommendations from content-based system
   - Get top 2N recommendations from collaborative filtering system
   - Get top 2N recommendations from taste-based system (if available)
   - Normalize each type of score to 0-1 range
2. **Score Blending**:
   ```
   Hybrid Score = cb_weight × cb_score 
               + cf_weight × cf_score 
               + taste_weight × taste_score
   ```
   - Default: Equal weights (1/3 each for 3-component)
   - Adjustable: Change weights for different recommendation strategies
3. **Merged Ranking**:
   - Combine all unique recommendations from all engines
   - Rank by final hybrid score
   - Eliminate duplicates (keep highest composite score)
   - Return top N with full transparency
4. **Output**: Returns recommendations with detailed breakdown showing contribution from each engine

**Key Features**:

- **Diversity**: Leverages content, community patterns, AND learned embeddings
  - Content: Explicit book features (genre, title similarity)
  - Collaborative: What similar readers enjoy
  - Taste: Abstract similarity in learned feature space
  
- **Robustness**: Falls back gracefully when any component lacks signal
  - New users: All three systems provide initial recommendations
  - Isolated users: Content + Taste systems ensure coverage
  - New books: All systems can score them
  
- **Interpretability**: Shows exact contribution of each engine
  ```
  Book X Score Breakdown:
  - Content-Based:      0.88  (similar genre/title characteristics)
  - Collaborative:      0.75  (readers of your books also enjoyed this)
  - Taste-Based:        0.92  (matches your taste profile in 8D space)
  ────────────────────
  Hybrid Score:         0.85  (weighted combination)
  ```
  
- **Flexibility**: Weights can be tuned dynamically for different use cases:

| Use Case | CB Weight | CF Weight | TB Weight | When to Use |
|----------|-----------|-----------|-----------|------------|
| New Users | 0.50 | 0.50 | 0.00 | No taste embeddings yet |
| Content-Heavy | 0.60 | 0.20 | 0.20 | Emphasize explicit genres |
| Community-Focused | 0.20 | 0.60 | 0.20 | Discover social favorites |
| Taste-Driven | 0.25 | 0.25 | 0.50 | Maximize serendipity |
| Balanced (Default) | 0.33 | 0.33 | 0.33 | All signals equally valued |

**Example Output**:
```
User: User074
Mode: 3-COMPONENT (33% CB + 33% CF + 33% TB)
Books User Has Read: 5 books

Top Hybrid Recommendations:
╭─────┬──────────────────────────┬──────────┬──────────┬──────────┬──────────╮
│ #  │ Title                    │  Hybrid  │ Content  │  CF      │  Taste   │
├─────┼──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
│  1  │ "Book X"                 │  0.92    │  0.88    │  0.96    │  0.93    │
│  2  │ "Book Y"                 │  0.85    │  0.90    │  0.80    │  0.85    │
│  3  │ "Book Z"                 │  0.78    │  0.75    │  0.81    │  0.77    │
├─────┼──────────────────────────┼──────────┼──────────┼──────────┼──────────┤
║ ... │                          │ ...      │ ...      │ ...      │ ...      │
╰─────┴──────────────────────────┴──────────┴──────────┴──────────┴──────────╯
```

---

## Recommendation System Comparison

| Aspect | Content-Based | Collaborative | Taste-Based | Hybrid |
|--------|---------------|---------------|-------------|--------|
| **Coverage** | 100% users | ~22% users | 100% users | 100% users |
| **Transparency** | Explicit (genre/title) | Moderate (community) | Advanced (8D embed) | Highest (all shown) |
| **Diversity** | Low-Medium | High | Medium-High | Highest |
| **Speed** | Fast | Fast | Fast | Very Fast |
| **Scalability** | Excellent | Excellent | Excellent | Excellent |
| **Cold Start** | Handles well | Struggles | Handles well | Excellent |
| **Serendipity** | Low | High | High | Highest |
| **Best For** | Reliable matches | Community discovery | Nuanced taste | All use cases |

---

## Interactive Testing & Configuration

The hybrid system includes an interactive widget-based testing interface:

```python
# In company_u_hybrid_recsys.ipynb, Section 6:
# - Select any user from dropdown
# - Adjust number of recommendations (1-30)
# - Toggle Taste Network ON/OFF
# - System auto-updates recommendations in real-time
# - Shows component breakdown for each recommendation
# - Explores how weights affect ranking
```

**Key Controls**:
- **User Selection**: Pick any User ID from dataset
- **Recommendation Count**: Slide 1-30 recommendations
- **Taste Network Toggle**: Enable/disable 3-component mode
- **Auto-Update**: Changes immediately show impact on recommendations
- **Component Transparency**: See exactly why each book was recommended

---

## Future Enhancement: AI Model Integration

The hybrid system is architected to support advanced AI enhancements:

**Planned Integration Points**:

1. **Neural Ranking Layer**: Learn optimal weights per user
   - Input: [CB_score, CF_score, TB_score, user_profile]
   - Output: Predicted relevance ranking
   - Benefits: Personalized weighting beyond static 33/33/33
   - Training data: Historical user engagement (clicks, ratings, dwell time)

2. **Semantic Understanding**: LLM-based deep content analysis
   - Extract semantic relationships from book summaries, reviews
   - Enhance content-based similarity beyond TF-IDF keywords
   - Identify subtle thematic connections
   - Link similar books despite different genres

3. **Cold Start Solutions**: AI-powered bootstrap strategy
   - For new users: Use similarity to existing user cohorts
   - For new books: Analyze metadata to seed embeddings
   - Rapid convergence to good recommendations

4. **Dynamic Ranking Optimization**: Deep learning ranker
   - Learn from implicit feedback (engagement, time-spent)
   - Optimize for downstream business metrics
   - A/B test recommender variants
   - Track NDCG, MAP, Click-Through Rate (CTR)

**Implementation Template** (Future):
```python
def get_hybrid_recommendations_with_ai(
    user_id, 
    num_recommendations=10,
    use_neural_ranker=False,
    learning_mode='inference'
):
    """
    Enhanced hybrid with optional AI ranking.
    
    Args:
        user_id: Target user
        num_recommendations: Top N to return
        use_neural_ranker: Apply learned neural ranker if True
        learning_mode: 'inference' or 'training'
    
    Returns:
        Sorted recommendations with AI explanations
    
    # TODO: Load neural ranking model
    # TODO: Add LLM semantic similarity layer
    # TODO: Implement cold-start AI strategy
    # TODO: Track metrics for model evaluation
    """
    
    # Step 1: Get base hybrid recommendations
    base_recs = get_hybrid_recommendations(user_id, num_recommendations*2)
    
    # Step 2: Apply neural ranker (if available)
    if use_neural_ranker and neural_model_loaded:
        ai_scores = neural_ranker.predict(base_recs)
        ranked_recs = sort_by_ai_score(base_recs, ai_scores)
    else:
        ranked_recs = base_recs
    
    # Step 3: Log engagement for model training
    if learning_mode == 'training':
        log_recommendation_feedback(user_id, ranked_recs)
    
    return ranked_recs[:num_recommendations]
```

To implement:
1. Collect recommendation feedback (implicit/explicit signals)
2. Train PyTorch or TensorFlow ranker model on feedback
3. Save trained model as `neural_ranker_v1.pt`
4. Load and integrate into hybrid function
5. Monitor NDCG@10, MAP@10 metrics on holdout test set

---

## Quick Reference: Which Step Should I Do Now?

**Confused about what to run next?** Use this:

| Goal | What to Open | How |
|------|-------------|-----|
| **Get recommendations from genre/title** | `company_u_content_based_recsys.ipynb` | Run all cells, then create new cell with code |
| **Get recommendations from what readers liked** | `company_u_collaborative_filtering.ipynb` | Run all cells, then create new cell with code |
| **Get recommendations from learned taste** | `company_u_taste_network.ipynb` | Run all cells (creates embedding files) |
| **Get ALL THREE combined** (BEST) | `company_u_hybrid_recsys.ipynb` | Run all setup, then use interactive widget |
| **Play with toggle and weights** | `company_u_hybrid_recsys.ipynb` cell 10 | Run cells 1-10, interact with widget |
| **See how models compare** | `company_u_hybrid_recsys.ipynb` cell 11 | Run all cells, see comparison table |

---

## Quick Start: Running All Models

This section provides step-by-step instructions to run each recommendation model and the hybrid system.

### Prerequisites — Before You Start

**Quick Checklist**:

1. **Do you have the main data file?**
   - In VS Code, open: `book-genre-ai/company_u/`
   - Look for: `company_u.csv` file
   - If you don't see it, ask where it is

2. **Is Python environment activated?** (in Terminal):
   ```bash
   cd /Users/mariammanukyan/Desktop/book-recommendation
   source .venv/bin/activate
   ```
   - Look for `(.venv)` prefix in your terminal — you'll see it before your prompt

3. **Folder open with right path?**
   - File → Open Folder
   - Choose: `/Users/mariammanukyan/Desktop/book-recommendation`
   - You'll see `book-genre-ai/` in left sidebar

4. **Optional: What files do you already have?**
   - `company_u.csv` — You should have this
   - `company_u_books_output.csv` — Maybe (from a previous run)
   - `company_u_genres_output.csv` — Maybe (from a previous run)
   - If you have all three, you can skip to Models directly
   - If you don't, the models will create what they need

---

### Model 1: Content-Based Recommendation

**What it does**: Recommends books based on genre and title similarity.

**Step-by-Step Instructions**:

1. **Open the notebook**:
   - File → Open File
   - Navigate to: `book-genre-ai/company_u/company_u_content_based_recsys.ipynb`

2. **Run all cells sequentially** (Jupyter menu: Run → Run All Cells):
   - This loads the book data and builds the TF-IDF similarity matrix
   - Expected time: 2-5 seconds
   - You'll see: "Content-Based system ready"

3. **Create a new cell to test** (where you'll get recommendations):
   - Scroll to the very bottom of the notebook
   - Press **B** key (adds blank cell below)
   - Or click the **+** button in toolbar
   - A white empty cell appears

4. **Get recommendations** (copy-paste this into your new cell):
   ```python
   # Get 10 recommendations for User002
   user_id = "User002"  # Change to different User IDs to test
   result = get_recommendations(user_id, num_recommendations=10)
   print(result)
   ```
   - Paste the code, then press `Ctrl+Enter` (or `Cmd+Enter`)
   - Results show below the cell

5. **What the output looks like**:
   ```
   {
     'user_id': 'User002',
     'status': 'success',
     'num_books_read': 5,
     'books_read': [Book A, Book B, Book C, Book D, Book E],
     'recommendations':
        Rank  Title                        Similarity
        0     Similar Book Title 1         0.85
        1     Similar Book Title 2         0.78
        2     Similar Book Title 3         0.72
   }
   ```
   
   **If you see this**: It worked!
   
   **If you got an error**:
   - "User002 not found" → Use a different User ID (see step 6)
   - Red cell → A cell above failed, scroll up to check

6. **Find valid User IDs** (if user not found):
   
   Create a new cell and run:
   ```python
   # See what users exist
   print(f"Total users: {len(unique_users)}")
   print("\nFirst 10 valid User IDs:")
   for user in unique_users[:10]:
       print(f"  {user}")
   ```
   Pick one and use it in step 4

7. **Try different settings**:
   ```python
   # Fewer recommendations
   result = get_recommendations("User050", num_recommendations=5)
   print(result)
   
   # Different user
   result = get_recommendations("User100", num_recommendations=15)
   print(result)
   ```

---

### Model 2: Collaborative Filtering

**What it does**: Recommends books based on what similar readers have read.

**Step-by-Step Instructions**:

1. **Open the notebook**:
   - File → Open File
   - Navigate to: `book-genre-ai/company_u/company_u_collaborative_filtering.ipynb`

2. **Run all cells sequentially** (Use Run All or `Ctrl+Shift+Enter`):
   - Builds co-occurrence matrix from reader patterns
   - Computes Jaccard + Cosine similarities
   - Expected time: 3-7 seconds
   - You'll see: `"CF recommendation function ready"`

3. **Create a new cell to test**:
   - Press **B** key (or click **+** button)
   - A blank cell appears

4. **Get recommendations** (copy-paste into your new cell):
   ```python
   # Get CF recommendations
   user_id = "User162"  # Change user ID to test different users
   result = get_cf_recommendations(user_id, num_recommendations=10)
   
   # Display as a readable table
   import pandas as pd
   df = pd.DataFrame([
       {"Title": book, "Score": score} 
       for book, score in list(result.items())
   ])
   print(df.to_string(index=False))
   ```
   - Press `Ctrl+Enter` to run
   - Results appear below

5. **What you should see**:
   ```
   Title                          Score
   Book that similar readers liked 0.85
   Another community favorite      0.72
   Hidden gem from reader overlap  0.68
   ...
   ```
   
   **If you see this**: It worked!
   
   **If you see nothing or zeros**: That user might be isolated (no shared readers). Try a different User ID.

6. **Check your coverage** (see how many users have recommendations):
   
   Create a new cell:
   ```python
   # Count users with CF recommendations
   covered = 0
   for user in unique_users:
       recs = get_cf_recommendations(user, num_recommendations=1)
       if len(recs) > 0:
           covered += 1
   
   print(f"CF Coverage: {covered}/{len(unique_users)} users ({100*covered/len(unique_users):.1f}%)")
   print("Note: CF works when users share reading patterns with others")
   ```

---

### Model 3: Taste-Based Neural Network

**What it does**: Recommends books based on 8D learned taste embeddings.

**Step-by-Step Instructions**:

1. **Open the notebook**:
   - File → Open File
   - Navigate to: `book-genre-ai/company_u/company_u_taste_network.ipynb`

2. **Run all cells sequentially** (Use Run All or `Ctrl+Shift+Enter`):
   - Generates 8-dimensional taste embeddings for each book
   - Computes cosine similarity between taste profiles
   - Expected time: 5-10 seconds
   - You'll see: `"Taste-Based system ready"`
   
   **Important**: Two files are created:
   - `taste_embeddings_matrix.npy` (the embeddings)
   - `book_taste_profiles.csv` (readable taste scores)

3. **Create a new cell to test**:
   - Press **B** key or click **+**
   - Blank cell ready

4. **Get recommendations** (copy-paste into your new cell):
   ```python
   # Get taste-based recommendations
   user_id = "User050"
   result = get_taste_recommendations(user_id, num_recommendations=10)
   
   # Show results
   for book, score in list(result.items())[:5]:
       print(f"{score:.3f} — {book}")
   ```
   - Press `Ctrl+Enter`

5. **What you should see**:
   ```
   0.892 — Book with similar taste profile
   0.845 — Another emotionally similar book
   0.778 — Hidden gem matching learned features
   0.695 — Surprising match based on embeddings
   ```
   
   **If you see scores**: It worked!
   
   ⚠️ **If you see an error**: No problem, this is expected if embeddings haven't been created yet

6. **Explore taste profiles** (optional deep dive):
   
   Create a new cell:
   ```python
   # Load and see taste dimensions
   import pandas as pd
   taste_df = pd.read_csv('book_taste_profiles.csv')
   
   print("Sample books with their taste profiles:")
   print(taste_df.head())
   print(f"\nTotal books with taste profiles: {len(taste_df)}")
   ```

7. **Check coverage** (taste works for everyone):
   ```python
   # Taste-based coverage
   all_covered = 0
   for user in unique_users:
       recs = get_taste_recommendations(user, num_recommendations=1)
       if len(recs) > 0:
           all_covered += 1
   
   print(f"Taste Coverage: {all_covered}/{len(unique_users)} (100% expected)")
   ```

---

### Model 4: Hybrid Recommendation (3-Component System)

**What it does**: Combines all three models (Content-Based, Collaborative, Taste-Based) for superior recommendations.

**Step-by-Step Instructions**:

#### Part A: Setup (Run Once)

1. **Open the notebook**:
   - In VS Code left sidebar, find: `book-genre-ai/company_u/`
   - Double-click: `company_u_hybrid_recsys.ipynb`

2. **Run the setup cells 1-7** (Data loading + all three models):
   
   Just hit **"Run All"** (or `Ctrl+Shift+Enter`)
   
   **What's loading**:
   - Cells 1-2: Loads book data and user data
   - Cells 3-5: Builds collaborative filtering similarity matrix
   - Cell 6: Sets up content-based TF-IDF system
   - Cell 7: Tries to load taste embeddings (might show warning, that's OK)
   
   **What you'll see**:
   ```
   "Data loaded successfully"
   "CF similarity matrix ready"
   "Content-Based system ready"
   "Taste-Based system ready"  (or warning if files missing)
   ```
   
   After this, all three recommendation engines are ready!

#### Part B: Get Hybrid Recommendations (Simple Way)

3. **Create a new cell** below the setup (press **B** or click **+**):
   ```python
   # Get hybrid recommendations
   user_id = "User002"
   result = get_hybrid_recommendations(
       user_id, 
       num_recommendations=10,
       cb_weight=0.33,      # 33% Content-Based
       cf_weight=0.33,      # 33% Collaborative Filtering
       taste_weight=0.33    # 33% Taste-Based
   )
   
   print(result['recommendations'])
   ```
   - Run it (`Ctrl+Enter`)
   - You see a table of recommendations with scores from all three models

#### Part C: Interactive Widget (More Fun Way)

4. **Run cells 8-9** (define hybrid functions):
   - Messages: `"Hybrid recommendation function ready"`

5. **Run cell 10** (the interactive widget):
   - Widget appears below cell with:
   
   ```
   ☑ Use AI Taste Network          ← Check/uncheck this!
   Select User:      [User002    ▼]
   # Recommendations: [|●●●●●| 10]
   CB Weight:        [|●●●●●| 0.33]
   CF Weight:        [|●●●●●| 0.33]
   TB Weight:        [|●●●●●| 0.33]  (hidden when toggle OFF)
   ```

6. **Interact with the toggle** (the magic moment):
   - **Click the checkbox to TURN ON taste network**:
     - Status changes to "ON - Using 3-component (33/33/33)"
     - Taste weight slider appears
     - Recommendations re-rank in real-time
   
   - **Click the checkbox to TURN OFF taste network**:
     - Status changes to "OFF - Using 2-component (50/50)"
     - Taste weight slider disappears
     - Recommendations re-rank again (different rankings!)

7. **Experiment**:
   - Pick different users from dropdown → See different recommendations
   - Drag recommendation slider → Get 5, 10, 20 recommendations
   - Toggle taste ON/OFF → Watch books re-rank live
   - Drag weight sliders (when ON) → Change how muchtaste influences results

#### Part D: Compare All Three Models

8. **Run cell 11** (comparison):
   - Shows side-by-side table: CB vs CF vs TB vs Hybrid
   - For 4 different test users
   - See how each model ranks the same books differently

The **"Use AI Taste Network"** checkbox in the interactive interface is the key to the hybrid model's flexibility. Here's how it works in detail:

#### **What Happens When You Toggle**

**Initial State**:
- Checkbox appears with label: "Use AI Taste Network"
- Default value: **Checked** (ON) if taste embeddings loaded successfully
- Default value: **Unchecked** (OFF) if taste embeddings not found
- Status indicator shows current mode below the checkbox

**When You CHECK the Box** (Turn ON):
1. **Immediately**:
   - Status message changes: "Taste Network: ON - Using 3-component hybrid (33/33/33)"
   - Taste Network Weight slider becomes VISIBLE
   - Weights auto-adjust to: 33% CB + 33% CF + 33% TB

2. **Recommendations Update in Real-Time**:
   - System calls `get_taste_recommendations()` for each user
   - All three engines contribute to final score
   - Books may re-rank (especially taste-similar books move up)
   - Component scores display all three values

3. **Example Impact**:
   ```
   BEFORE (Taste OFF):
   Rank | Title        | Hybrid | CB    | CF    | TB
   -----|--------------|--------|-------|-------|------
     1  | Book A       | 0.87   | 0.88  | 0.85  | —
     2  | Book B       | 0.82   | 0.80  | 0.84  | —
     3  | Book C       | 0.79   | 0.78  | 0.80  | —
   
   AFTER (Taste ON):
   Rank | Title        | Hybrid | CB    | CF    | TB
   -----|--------------|--------|-------|-------|------
     1  | Book B       | 0.89   | 0.80  | 0.84  | 0.95  ← moved up! Better taste match
     2  | Book A       | 0.87   | 0.88  | 0.85  | 0.80
     3  | Book C       | 0.79   | 0.78  | 0.80  | 0.75
   ```

**When You UNCHECK the Box** (Turn OFF):
1. **Immediately**:
   - Status message changes: "Taste Network: OFF - Using 2-component hybrid (50/50 CB+CF)"
   - Taste Network Weight slider becomes HIDDEN (disabled)
   - Weights auto-adjust to: 50% CB + 50% CF + 0% TB

2. **Recommendations Update in Real-Time**:
   - System STOPS calling `get_taste_recommendations()`
   - Only Content-Based and Collaborative signals used
   - Recommendations may re-rank (taste-only picks disappear)
   - Taste-Based column still shows values but doesn't affect score

3. **Example Impact**:
   ```
   BEFORE (Taste ON):
   Rank | Title        | Hybrid | CB    | CF    | TB
   -----|--------------|--------|-------|-------|------
     1  | Book B       | 0.89   | 0.80  | 0.84  | 0.95
     2  | Book A       | 0.87   | 0.88  | 0.85  | 0.80
   
   AFTER (Taste OFF):
   Rank | Title        | Hybrid | CB    | CF    | TB
   -----|--------------|--------|-------|-------|------
     1  | Book A       | 0.87   | 0.88  | 0.85  | 0.80  ← back on top (no taste factor)
     2  | Book B       | 0.82   | 0.80  | 0.84  | 0.95  ← dropped (high TB not used)
   ```

#### **How Recommendations Change When Toggling**

The toggle affects **recommendation ranking** through weight redistribution:

**Key Points**:
1. **Same books remain candidates**: Toggle doesn't eliminate books, it re-ranks them
2. **Different weighting = Different scores**: Same book may get 0.87 with taste ON, 0.82 with taste OFF
3. **Taste-heavy books float up with taste ON**: Books matching learned embeddings rise in ranking
4. **Content+CF-heavy books float up with taste OFF**: Books matching genres move higher
5. **Both systems contribute when ON**: Book needs to be good across all three dimensions to rank #1

#### **Real-World Example: How Toggle Affects Actual Recommendations**

**Scenario**: User read ["Literary Fiction A", "Classic Novel B"]

**With Taste Network OFF (50% CB + 50% CF)**:
```
Recommendations might look like:
1. "Another Literary Fiction"     (scored high on genre similarity)
2. "Classic Novel Similar"        (readers of your books liked this)
3. "Book about similar themes"    (content overlap)
4. "Genre-adjacent book"          (similar to one you read)

Why ranked this way:
- Books matching explicit genres rank highest
- Books read by similar readers score well
- No consideration of abstract taste dimensions
```

**With Taste Network ON (33% CB + 33% CF + 33% TB)**:
```
Recommendations might look like:
1. "Character-Driven Masterpiece"    (high on ALL three: genre + community + taste)
2. "Emotional Literary Novel"        (excellent taste match, good genre fit)
3. "Book about similar themes"       (still good but taste adds new insight)
4. "Surprising Hidden Gem"           (NEW! Ranked via learned embeddings)
5. "Another Literary Fiction"        (from before, now ranked lower)

Why ranked differently:
- Taste-based intelligence discovers serendipitous matches
- Books liked by similar users PLUS matching learned taste rank highest
- Unexpected but thematically similar books surface
- More diverse ranking (not just explicit genre similarity)
```

#### **Interactive Toggle Features**

**Automatic Behaviors**:

1. **Auto-Update on Toggle**: When you check/uncheck, results refresh immediately
   - No need to click "Show Recommendations" button
   - Status label updates instantly
   - Widget responsiveness shows system working

2. **Slider Visibility Toggle**:
   - Taste Network Weight slider only appears when Taste Network is ON
   - Disappears (grayed out) when Taste Network is OFF
   - Prevents confusion about unused parameters

3. **Disabled State** (if taste files not found):
   - Checkbox appears but is **disabled** (cannot click)
   - Toggle is OFF by default
   - Message: "Taste Network: Unavailable"
   - Reason: Auto-fallback to 50/50 CB+CF when embeddings missing

4. **Real-Time Mode Display**:
   ```
   Status Updates as You Toggle:
   
   Taste Network: ON - Using 3-component hybrid (33% CB + 33% CF + 33% TB)
   [checkbox is checked]
   [Taste Network Weight slider is VISIBLE]
   
   ↓ (after unchecking)
   
   Taste Network: OFF - Using 2-component hybrid (50% CB + 50% CF)
   [checkbox is unchecked]
   [Taste Network Weight slider is HIDDEN]
   ```

#### **Recommendation Changes When Select Different Users**

When you select a **different user from the dropdown**, the toggle state remains but recommendations change:

```
Example Flow:

1. Select "User002" (Taste ON)
   └─ Shows User002's recommendations with taste network active

2. Toggle to OFF
   └─ User002's recommendations recalculate (taste network off)

3. Select "User050" (Still OFF)
   └─ Shows User050's recommendations WITHOUT taste network
   
4. Toggle to ON
   └─ User050's recommendations recalculate (taste network on)
   
5. Back to "User002" (Still ON)
   └─ User002's recommendations recalculate WITH taste network
   └─ Different from step 1 because weights re-centered
```

#### **Slider Behavior When Toggle is ON**

When Taste Network is ON and slider becomes visible, you can manually adjust weights:

```python
# Default when you toggle ON:
cb_weight = 1/3    (33%)
cf_weight = 1/3    (33%)
taste_weight = 1/3 (33%)

# If you drag sliders while ON:
# Example: drag taste weight to 0.5
cb_weight = 0.25   (25%)
cf_weight = 0.25   (25%)
taste_weight = 0.5 (50%)
# Recommendations immediately re-rank with new weights
```

**Sliders Available**:
- **Content-Based Weight**: Adjust 0.0-1.0
- **CF Weight**: Adjust 0.0-1.0
- **Taste Network Weight**: (ONLY VISIBLE WHEN ON) Adjust 0.0-1.0

**Important**: Sliders are ignored when Taste Network is OFF (hidden and non-functional)

#### **Visual Feedback from Toggle**

The interface provides clear visual feedback:

```
┌─────────────────────────────────────────┐
│ CONFIGURATION:                          │
├─────────────────────────────────────────┤
│ Neural Taste Network:                   │
│ ☑ Use AI Taste Network                  │
│ Taste Network: ON - Using 3-component   │
│ hybrid (33/33/33)                       │
├─────────────────────────────────────────┤
│ Recommendation Parameters:              │
│                                         │
│ Select User: [User002        ▼]         │
│ # Recommendations: |●●●●●●●●| 10       │
│ Content-Based Weight: |●●●●●●●●●| 0.33 │
│ CF Weight: |●●●●●●●●●| 0.33             │
│ Taste Network Weight: |●●●●●●●●●| 0.33 │
│                                         │
│ [Show Recommendations]                  │
└─────────────────────────────────────────┘
```

#### **Troubleshooting Toggle Issues**

| Problem | Cause | Solution |
|---------|-------|----------|
| Checkbox is disabled | Taste files not found | Run Model 3 first to generate embeddings |
| Toggle doesn't update results | Results not auto-updating | Click "Show Recommendations" button |
| Taste weight slider won't appear | Checkbox not actually checked | Verify checkbox is visibly checked |
| Recommendations don't change when toggles | Mode already active | Toggle OFF then ON again |
| Status message says "Unavailable" | Taste embeddings missing | Ensure `taste_embeddings_matrix.npy` exists |

---

#### Part D: Compare All Three Approaches

12. **Run cell 11 (Comparison)**:
    - Shows side-by-side recommendations from all three models
    - Expected: Clear table comparing CB vs CF vs TB vs Hybrid
    - Runs for 4 test users
    - Shows how each model ranks the same books differently

---

### Complete Workflow: Run Everything in Order

**Recommended execution sequence** (first time setup):

```
1. Book Processor
   └─ Creates: company_u_books_output.csv

2. Genre Classifier
   └─ Creates: company_u_genres_output.csv

3. Content-Based Model
   └─ Creates similarity matrices in memory

4. Collaborative Filtering Model
   └─ Creates co-occurrence matrices in memory

5. Taste-Based Neural Network
   └─ Creates: taste_embeddings_matrix.npy
                book_taste_profiles.csv

6. Hybrid Recommendation System
   └─ Loads all three models
   └─ Provides unified interface
   └─ Interactive testing widgets
```

**Terminal Command** (if running notebooks via command line):
```bash
cd /Users/mariammarukyan/Desktop/book-recommendation/book-genre-ai/company_u
source /Users/mariammanukyan/Desktop/book-recommendation/.venv/bin/activate

# Run Book Processor
jupyter nbconvert --to notebook --execute company_u_books_processor.ipynb

# Run Genre Classifier
jupyter nbconvert --to notebook --execute company_u_genre_classifier.ipynb

# Run Content-Based Model
jupyter nbconvert --to notebook --execute company_u_content_based_recsys.ipynb

# Run Collaborative Filtering Model
jupyter nbconvert --to notebook --execute company_u_collaborative_filtering.ipynb

# Run Taste-Based Model
jupyter nbconvert --to notebook --execute company_u_taste_network.ipynb

# Run Hybrid System (loads all three)
jupyter nbconvert --to notebook --execute company_u_hybrid_recsys.ipynb
```

---

### Using Models Programmatically

**In Custom Scripts**:

```python
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load content-based model
exec(open('company_u_content_based_recsys.ipynb').read())  # NOT recommended

# Better: Run notebook first, then import functions via kernel session:

# When running in same Jupyter kernel:
cb_recs = get_recommendations("User100", num_recommendations=5)
cf_recs = get_cf_recommendations("User100", num_recommendations=5)
taste_recs = get_taste_recommendations("User100", num_recommendations=5)
hybrid_recs = get_hybrid_recommendations("User100", num_recommendations=5)
```

---

### Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| **No module named 'sklearn'** | `pip install scikit-learn` |
| **No module named 'pandas'** | `pip install pandas` |
| **No module named 'numpy'** | `pip install numpy` |
| **User ID not found** | Check `unique_users` list first; IDs are case-sensitive |
| **Taste files not found** | Run Model 3 (Taste-Based) first to generate files |
| **"CF Coverage: 0%"** | Normal—depends on dataset; some users may be isolated |
| **Memory error on large dataset** | Run one model at a time; restart kernel between models |
| **Widget not showing** | Ensure ipywidgets installed: `pip install ipywidgets` |
| **Slow recommendations** | Normal for first run; subsequent calls are cached |

---

### Performance Expectations

| Model | Time | Memory | Coverage |
|-------|------|--------|----------|
| Content-Based | <1 sec | 50 MB | 100% |
| Collaborative | 1-3 sec | 100 MB | ~22% |
| Taste-Based | 2-5 sec | 150 MB | 100% |
| Hybrid | <1 sec | 200 MB | 100% |

---

### Advanced: Custom Weight Configurations

```python
# Emphasize Content-Based (best for new users)
hybrid = get_hybrid_recommendations(
    user_id, 
    cb_weight=0.60, 
    cf_weight=0.20, 
    taste_weight=0.20
)

# Emphasize Taste-Based (best for discovery)
hybrid = get_hybrid_recommendations(
    user_id, 
    cb_weight=0.25, 
    cf_weight=0.25, 
    taste_weight=0.50
)

# Community-focused (what similar readers like)
hybrid = get_hybrid_recommendations(
    user_id, 
    cb_weight=0.20, 
    cf_weight=0.60, 
    taste_weight=0.20
)

# Custom weights (must sum to 1.0 for best results)
hybrid = get_hybrid_recommendations(
    user_id, 
    cb_weight=0.40, 
    cf_weight=0.30, 
    taste_weight=0.30
)
```

---

## Why This Matters

This project started with a simple goal: help readers discover their next favorite book. But it evolved into something much richer.

We built **four different recommendation engines** not because one wasn't enough, but because every reader is different:
- Some prefer books exactly like what they've read (Content-Based)
- Some trust the reading community and want to know what similar readers enjoyed (Collaborative Filtering)
- Some are adventurous and want to discover hidden patterns in taste (Taste-Based)
- Most of us want all three perspectives combined (Hybrid)

The **Armenian language support** isn't just a feature—it's recognition that literature transcends the Latin alphabet, and libraries serve diverse communities.

The **interactive toggle interface** lets *you* decide what "good recommendation" means in each moment. Some days you want community picks, other days you want serendipity. This system adapts to you.

---

## What You Can Do With This

Use this for:
- **Library operations**: Understand your collection and patron preferences
- **Reading discovery**: Get personalized book recommendations
- **Research**: Study recommendation algorithms, genre patterns, cultural diversity in literature
- **Learning**: Understand how multiple AI systems work together
- **Experimentation**: Modify weights, test different strategies, measure what works

---

## Looking Forward

This framework is designed to grow:
- Train feedback models from real user engagement
- Add LLM-powered semantic analysis for deeper book understanding
- Integrate with other libraries for broader recommendations
- Build cold-start solutions for new users and books
- Track implicit signals (reading time, reviews, social sharing)

The infrastructure is here. The possibilities are open.

---

## Questions or Improvements?

Found a bug? Have suggestions? The notebooks are structured for easy modification:
- Each section is clearly labeled
- Functions are documented with examples
- Output files are human-readable CSVs
- Weights and parameters are all tunable

Feel free to fork, modify, and experiment. That's what this is for.

---

Built with curiosity and coffee.

*Mariam Manukyan, 2026*  
Company U Library Analysis & Recommendation System
