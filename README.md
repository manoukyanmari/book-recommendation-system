# A Data-Driven System for Consumer Behavior Analysis and Personalized Book Recommendations

**Capstone Thesis** | American University of Armenia | Industrial Engineering and Systems Management

**Author:** Mariam Manukyan (mariam_manukyan@edu.aua.am)  
**Advisor:** Gurgen Hovakimyan, AUA College of Science and Engineering

---

## Abstract

This thesis presents a data-driven framework for analyzing consumer behavior and developing personalized book recommendation systems in environments with limited and imperfect data. The study analyzes three real-world datasets from different organizations (Company A, Company N, and Company U) and applies comprehensive analytical techniques including data preprocessing, language normalization, feature engineering, and topic modeling.

The research reveals data sparsity, imbalance, low variability in user engagement, and limitations in metadata quality across all organizations. Based on these insights, a **hybrid recommendation system** is developed, integrating:

1. **Content-Based Filtering** - leverages textual features and metadata
2. **Collaborative Filtering** - uses user interaction patterns and co-occurrence
3. **Taste-Based Neural Network** - learns latent book characteristics through 8-dimensional embeddings

The findings demonstrate that **content-based filtering provides the most stable recommendations** under sparse data conditions, while collaborative filtering is limited by insufficient user interaction overlap. The neural taste-based component captures latent similarities but has limited impact due to dataset homogeneity.

The study contributes a practical, adaptable framework for recommendation system design applicable to academic and low-resource library environments, supporting improved book discovery and data-driven decision-making.

**Index Terms:** recommender systems, hybrid recommendation model, implicit feedback, sparse data, content-based filtering, collaborative filtering, neural networks, NLP, topic modeling

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Methodology](#methodology)
3. [Datasets](#datasets)
4. [Project Structure](#project-structure)
5. [Key Findings](#key-findings)
6. [System Architecture](#system-architecture)
7. [How to Use](#how-to-use)
8. [Technologies](#technologies)
9. [Results Summary](#results-summary)
10. [Recommendations](#recommendations)

---

## Problem Statement

### Challenges in Library Environments

Libraries and bookstores in low-resource contexts face critical limitations when implementing recommendation systems:

- **No Explicit Feedback:** Systems must rely entirely on implicit feedback (borrowing history), with no ratings or reviews
- **Limited Metadata:** Genre information is incomplete, inconsistent, or entirely missing
- **Multilingual Complexity:** Armenian and English data requires translation and normalization
- **Data Sparsity:** Most books receive only 1-3 checkouts, restricting pattern detection
- **Low Variability:** Minimal difference in user engagement signals

Traditional recommendation techniques struggle to produce accurate, diverse, and personalized recommendations under these conditions. This research develops a framework specifically designed for sparse, low-information environments.

---

## Methodology

### Research Design

This study adopts an **empirical and comparative design**, analyzing three real-world datasets using a unified preprocessing and modeling pipeline. Each dataset is processed independently, enabling cross-dataset comparison of patterns, feature importance, and model performance.

### Data Processing Pipeline

```
Raw Data
    ↓
[Preprocessing & Normalization]
    ├─ Language translation (Armenian → English)
    ├─ Stop word removal
    └─ Data cleaning and standardization
    ↓
[Feature Engineering]
    ├─ Structural features (title length, punctuation, digits)
    ├─ Lexical features (N-grams, keywords)
    ├─ Semantic features (sentiment, emotion)
    └─ Topic modeling (TF-IDF clustering)
    ↓
[Distribution Analysis]
    ├─ Sparsity quantification
    ├─ Variability assessment
    └─ Engagement concentration
    ↓
[Recommendation System Development]
    ├─ Content-Based Model
    ├─ Collaborative Filtering Model
    ├─ Taste-Based Neural Model
    └─ Hybrid Integration
```

### Key Analytical Techniques

**Structural Analysis:** Title length, punctuation patterns, digit usage

**Lexical Analysis:** Tokenization, N-gram extraction, keyword frequency

**Semantic Analysis:** Sentiment polarity, emotion classification using NLP

**Topic Modeling:** TF-IDF vectorization, clustering, latent theme extraction

**Distribution Analysis:** Sparsity metrics, Lorenz curves, power-law characteristics

---

## Datasets

### Company A
- **Size:** 1,091 titles (predominantly Armenian)
- **Characteristics:** High transaction volume, strong genre imbalance
- **Key Finding:** Nonfiction dominance with limited lexical variation
- **Status:** ✓ Analyzed

### Company N
- **Size:** 287 titles (Armenian)
- **Characteristics:** Uniform transaction values, no variability
- **Key Finding:** Identical engagement across all titles prevents differentiation
- **Status:** ✓ Analyzed

### Company U
- **Size:** 667 titles (612 English, 55 Armenian)
- **Structured Metadata:** Genre information available
- **Characteristics:** Sparse interactions (718 total checkouts, avg. 1.08 per title)
- **Key Finding:** 78.3% of activity concentrated in 20% of titles
- **Status:** ✓ Fully analyzed with hybrid system implementation

---

## Project Structure

```
book-recommendation/
├── README.md                                  # This file
├── Data/
│   ├── 1. Raw given/
│   │   ├── antares.csv                       # Company A data
│   │   ├── newmag.csv                        # Company N data
│   │   └── patron_checkouts_fall2025.csv     # Company U data
│   ├── 2. Cleaned to start/
│   │   ├── company_a.csv
│   │   ├── company_n.csv
│   │   └── company_u.csv
│   ├── 3. AUA - structurize before verification/
│   │   └── company_u_books_output.csv
│   ├── 4. Output Files/
│   │   ├── company_a_genres_output.csv
│   │   ├── company_n_genres_output.csv
│   │   └── company_u_genres_output.csv
│   └── DATA_SEMANTICS.md
│
├── book-genre-ai/
│   ├── company_a/
│   │   ├── README.md                         # Company A analysis documentation
│   │   ├── company_a_genre_classifier.ipynb  # Genre classification analysis
│   │   ├── company_a_visualization.ipynb     # Visualizations
│   │   ├── company_a.csv                     # Processed data
│   │   ├── company_a_genres_output.csv       # Classification results
│   │   ├── graphs/                           # Visualizations
│   │   ├── armenian_stopwords.csv
│   │   ├── translation_cache.json
│   │   └── openlibrary_cache.json
│   │
│   ├── company_n/
│   │   ├── README.md                         # Company N analysis documentation
│   │   ├── company_n_genre_classifier.ipynb  # Genre classification
│   │   ├── company_n_visualization.ipynb     # Analysis visualization
│   │   ├── company_n.csv
│   │   ├── company_n_genres_output.csv
│   │   ├── graphs/
│   │   ├── armenian_stopwords.csv
│   │   ├── translation_cache.json
│   │   └── openlibrary_company_n_cache.json
│   │
│   ├── company_u/
│   │   ├── README.md                         # Company U analysis documentation
│   │   ├── company_u_genre_classifier.ipynb  # Genre classification
│   │   ├── company_u_visualization.ipynb     # Visualizations
│   │   ├── company_u_content_based_recsys.ipynb    # Content-based model
│   │   ├── company_u_collaborative_filtering.ipynb # CF model
│   │   ├── company_u_taste_network.ipynb           # Neural taste model
│   │   ├── company_u_hybrid_recsys.ipynb          # Integrated hybrid system
│   │   ├── company_u.csv
│   │   ├── company_u_genres_output.csv
│   │   ├── company_u_books_output.csv
│   │   ├── graphs/
│   │   ├── armenian_stopwords.csv
│   │   ├── translation_cache.json
│   │   ├── openlibrary_company_u_cache.json
│   │   ├── taste_embeddings_matrix.npy       # Neural embeddings
│   │   ├── book_taste_profiles.csv           # Taste dimensions
│   │   ├── ARMENIAN_CLASSIFICATION_SUMMARY.md
│   │   ├── armenian_genre_analyzer.py
│   │   ├── armenian_transliterator.py
│   │   └── company_u_books_processor.ipynb
│   │
│   └── pdf_exports/
│       └── no_code/                          # Clean PDF versions
│
└── remove_emoji.py                           # Utility script
```

---

## Key Findings

### Across All Datasets

| Finding | Impact |
|---------|--------|
| Structural features (title length, punctuation) show near-zero correlation with engagement | Content features alone cannot explain borrowing patterns |
| Sentiment analysis shows majority of titles in neutral range | Emotional tone does not differentiate user behavior |
| Topic clusters have low separation and similar engagement levels | Latent thematic structure doesn't reveal user preferences |
| 78.3% of activity concentrated in 20% of titles | Extreme sparsity and concentration limit pattern detection |

### Recommendation Model Performance

**Content-Based Filtering:**
- Most differentiated similarity scores
- Stable performance across sparse data
- Requires minimal user interaction data
- Limitation: Depends on metadata quality

**Collaborative Filtering:**
- Co-occurrence matrix: 99.55% sparse (Company U)
- Mean similarity: 0.026996
- Convergence issue: Most unread books get identical scores
- Solution implemented: Popularity-based boosting breaks ties
- After improvement: Differentiated scores (0.600 to 0.027 range)

**Taste-Based Neural Network:**
- 8-dimensional learned embeddings
- Captures latent book characteristics
- Provides complementary signals to CB and CF
- Impact limited by dataset homogeneity

**Hybrid Model (Integrated):**
- Combines all three approaches with weighted scoring
- Primary driver: Content-based signals (most reliable)
- Secondary: Popularity-boosted collaborative filtering
- Tertiary: Taste embeddings (latent patterns)
- Result: Balanced recommendations adapting to data availability

---

## System Architecture

### Hybrid Recommendation Framework

```
┌─────────────────────────────────────────────────────┐
│         USER REQUEST (User ID, K recommendations)   │
└──────┬──────────────────────────────────────────────┘
       │
       ├─→ ┌─────────────────────────────────────┐
       │   │ CONTENT-BASED FILTERING             │
       │   │ - Title/metadata similarity (TF-IDF)│
       │   │ - Returns top-K suggestions         │
       │   └─────────────────────────────────────┘
       │
       ├─→ ┌─────────────────────────────────────┐
       │   │ COLLABORATIVE FILTERING             │
       │   │ - Co-occurrence analysis            │
       │   │ - Jaccard + Cosine blend (50/50)    │
       │   │ - Popularity boost (60% weight)     │
       │   │ - Returns differentiated scores     │
       │   └─────────────────────────────────────┘
       │
       ├─→ ┌─────────────────────────────────────┐
       │   │ TASTE-BASED NEURAL NETWORK          │
       │   │ - 8-dim learned embeddings          │
       │   │ - Cosine similarity in embedding    │
       │   │ - Returns latent pattern scores     │
       │   └─────────────────────────────────────┘
       │
       └─→ ┌─────────────────────────────────────┐
           │ HYBRID SCORE INTEGRATION            │
           │ Score = α·CB + β·CF + γ·Taste       │
           │ Default: 33/33/33 weighting         │
           │ Adaptive: 50/50 without taste net.  │
           └─────────────────────────────────────┘
                       │
                       ↓
           ┌─────────────────────────────────────┐
           │ RANKED RECOMMENDATIONS              │
           │ - Top-K results with scores         │
           │ - Component breakdown shown         │
           │ - Interpretability provided         │
           └─────────────────────────────────────┘
```

### Operating Modes

**Mode 1: 2-Component Hybrid** (Taste Network Unavailable)
- 50% Content-Based Filtering
- 50% Collaborative Filtering (with popularity boost)
- Default fallback when taste embeddings missing

**Mode 2: 3-Component Hybrid** (Taste Network Available)
- 33% Content-Based Filtering
- 33% Collaborative Filtering (with popularity boost)
- 33% Taste-Based Neural Network

---

## How to Use

### Quick Start

#### 1. Navigate to Company U (Most Complete Implementation)

```bash
cd book-recommendation/book-genre-ai/company_u/
```

#### 2. Run the Hybrid Recommendation System

Open and execute the main notebook:
```
company_u_hybrid_recsys.ipynb
```

#### 3. Get Recommendations

```python
# Direct function call
result = get_hybrid_recommendations(
    user_id='User002', 
    num_recommendations=10,
    cb_weight=0.33,
    cf_weight=0.33,
    taste_weight=0.33
)

# Interactive interface (runs automatically in notebook)
# Use widgets to:
# - Select user
# - Choose number of recommendations
# - Toggle taste network ON/OFF
# - Adjust component weights
```

#### 4. View Results

Results display:
- Hybrid score (combined ranking)
- Content-Based score
- Collaborative Filtering score
- Taste-Based score

Example output:
```
COLLABORATIVE FILTERING (Score: Reader Overlap)
 1. edited                              | Score: 0.600458
 2. by Harry Collis ; illustrated       | Score: 0.049810
 3. written                             | Score: 0.030627
 4. Erikh Fromm                         | Score: 0.026626
 5. Marc Nichanian ; translated         | Score: 0.026626
```

### Individual Component Testing

**Test Content-Based Only:**
```python
cb_recs = get_cb_recommendations_internal(
    'User002', 
    num_recommendations=10
)
```

**Test Collaborative Filtering:**
```python
cf_recs = get_cf_recommendations_internal(
    'User002', 
    num_recommendations=10
)
```

**Test Taste-Based Neural:**
```python
taste_recs = get_taste_recommendations_internal(
    'User002', 
    num_recommendations=10
)
```

---

## Technologies

### Core Libraries

| Technology | Purpose |
|-----------|---------|
| **Python 3.8+** | Programming language |
| **Pandas & NumPy** | Data processing and numerical computing |
| **Scikit-learn** | Machine learning and similarity computation |
| **TensorFlow/Keras** | Neural network for taste embeddings |
| **TextBlob & NRCLex** | NLP and sentiment analysis |
| **Scipy** | Sparse matrix operations |

### External APIs

| Service | Usage |
|---------|-------|
| **Google Books API** | Metadata enrichment (genres, descriptions) |
| **Open Library API** | Genre classification and book information |
| **Translation APIs** | Armenian to English conversion |

### Infrastructure

- **Caching:** JSON-based translation caching for efficiency
- **Jupyter Notebooks:** Interactive analysis and experimentation
- **File Format:** NPY (NumPy) for embeddings, CSV for data, JSON for caching

---

## Results Summary

### Company A Results
- High transaction volume enables differentiation
- Content-based model produces well-separated similarity scores
- Collaborative filtering generates measurable but less consistent signals
- Hybrid model provides balanced recommendations

### Company N Results
- Uniform transaction values prevent differentiation
- No observable variation in user engagement
- Recommendation models unable to generate meaningful ranked outputs
- System functions as designed but lacks informative signals

### Company U Results (Primary Study)
- **Data Sparsity:** 99.55% sparse co-occurrence matrix
- **Average Checkouts:** 1.08 per title
- **Distribution:** 78.3% of activity in 20% of titles
- **Content-Based:** Most reliable (0.4217 mean similarity)
- **Collaborative Filtering:** Initially all-identical scores → **Fixed with popularity boost**
- **Taste Network:** Stable 8-dimensional embeddings
- **Hybrid Output:** Ranked recommendations combining all signals

### Key Improvement: CF Popularity Boosting

**Before Fix:**
```
All scores identical: 0.0238
Problem: 99.55% sparsity converged all recommendations
```

**After Fix:**
```
Scores now varied: 0.600, 0.050, 0.031, 0.027...
Solution: Popularity boost (60% weight) breaks mathematical convergence
Result: Meaningful ranking differentiation
```

This improvement transforms CF from non-functional to valuable component in hybrid system.

---

## Recommendations

### For Implementation

1. **Prioritize Content-Based Filtering:** Most stable in sparse environments
2. **Improve Metadata Quality:** Invest in verified genre classifications
3. **Expand Interaction Data:** Collect more detailed user feedback
4. **Deploy Gradually:** Start with 2-component system, add taste network when data permits
5. **Monitor Performance:** Track which recommendations lead to actual checkouts

### For Future Work

1. **Richer Metadata:** Incorporate author, series, subject classification
2. **User Segmentation:** Anonymized user attributes for personalization
3. **Feedback Loop:** Collect binary feedback ("helpful?" / "not helpful?")
4. **Cross-Organization Analysis:** Combine datasets for pattern learning
5. **Advanced Embeddings:** Use modern pretrained language models (BERT, etc.)

### For Libraries & Bookstores

- **Deploy the hybrid system** to support book discovery
- **Use interactive interface** to explain recommendations to patrons
- **Track engagement metrics** to continuously improve weights
- **Collect user feedback** to refine future models
- **A/B test** different recommendation components

---

## Technical Details

### Collaborative Filtering with Popularity Boost

**Problem:** In sparse data, traditional CF similarity converges to identical values for most books.

**Solution:** Combine multiple signals:
- Jaccard similarity (co-occurrence based): 50%
- Cosine similarity (vector based): 50%
- **Popularity boost:** 60% of final score
  - Based on how many total users checked out the book
  - Breaks ties when similarity is equal

**Formula:**
```
weighted_sim = 0.5 * jaccard_sim + 0.5 * cosine_sim
popularity_boost = normalized_book_frequency * 0.6
final_score = weighted_sim + popularity_boost
```

**Result:** Recommendations now properly ranked by combination of co-occurrence overlap AND global popularity.

### Taste Network Architecture

- **Input:** Book title (text)
- **Embedding Layer:** Learned representations
- **Output:** 8-dimensional taste profile
- **Training:** MLP classifier on available category data
- **Output:** Latent taste dimensions capturing abstract book characteristics

### Hybrid Score Computation

```python
hybrid_score = (
    cb_weight * content_score +
    cf_weight * collaborative_score +
    taste_weight * taste_score
)
```

Default: Equal weights (0.33 each)  
Adaptive: 0.5/0.5 when taste network unavailable

---

## Data Characteristics

### Sparsity Analysis (Company U)

```
Total Checkouts: 718
Total Possible: 909 books × 100+ users ≈ 90,000+

User-Book Matrix Sparsity:
- 99.55% empty cells
- Only 4,655 non-zero co-occurrences out of 826,281
- Average co-occurrence: 0.0062

Book Frequency Distribution:
- Max: 3 checkouts
- Mean: 1.08 checkouts
- Median: 1.00 checkout
- 78.3% of activity in 20% of titles
```

### Dataset Characteristics

| Metric | Company A | Company N | Company U |
|--------|-----------|-----------|-----------|
| Titles | 1,091 | 287 | 667 |
| Language | Armenian | Armenian | English/Armenian |
| Avg Checkouts | Higher | Uniform | 1.08 |
| Variability | Yes | No | Low |
| Recommendation Viability | High | None | Moderate |

---

## Key References

[1] Chen, Y., Wang, R., Wu, L., & Li, Z. (2023). Deep reinforcement learning in recommender systems: A survey and new perspectives. *Knowledge-Based Systems*, 261, 110236.

[2] Kiran, R., Kumar, P., & Bhasker, B. (2020). DNNRec: A novel deep learning-based hybrid recommender system. *Expert Systems with Applications*, 144, 113054.

[3] Liu, H., Wang, Y., Zhang, Z., & Deng, J. (2024). Matrix factorization recommender based on adaptive Gaussian differential privacy for implicit feedback. *Information Processing & Management*, 61(1), 103720.

[4] Shimizu, R., Matsutani, M., & Goto, M. (2022). An explainable recommendation framework based on an improved knowledge graph attention network. *Knowledge-Based Systems*, 239, 107970.

[5] Wayesa, F., Leranso, M., Asefa, G., & Kedir, A. (2023). Pattern-based hybrid book recommendation system using semantic relationships. *Scientific Reports*, 13, 3693.

---

## Project Status

**Completed:**
- Data preprocessing and normalization across three datasets
- Comprehensive feature engineering and analysis
- Content-based filtering implementation
- Collaborative filtering with popularity boosting
- Taste-based neural network training
- Hybrid recommendation system integration
- Interactive testing interface
- Documentation and READMEs

**Datasets Analyzed:**
- Company A (1,091 titles)
- Company N (287 titles)
- Company U (667 titles) - Primary system deployment

**Deployment Ready:**
- Hybrid system fully functional
- Interactive widgets for testing
- All components integrated
- Performance optimized for sparse data

---

## Contact & Support

**Original Author:** Mariam Manukyan  
**Email:** mariam_manukyan@edu.aua.am

**Advisor:** Gurgen Hovakimyan  
**Institution:** American University of Armenia, College of Science and Engineering

For detailed analysis results, extended findings, and company-specific reports, please refer to individual company READMEs and comprehensive analysis documents within each company folder.

---

## Acknowledgments

We extend our sincere gratitude to the participating companies for providing the data and supporting this research. Their collaboration made it possible to conduct real-world analysis and develop practical, data-driven solutions for book recommendation and consumer behavior analysis.

A detailed comprehensive report (approximately 60 pages) containing extended analysis, visualizations, and domain-specific insights will be delivered separately to each participating organization.

---

**Last Updated:** April 27, 2026  
**Project Version:** 1.0 - Capstone Thesis Submission
