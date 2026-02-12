**Purpose**: Short guidance for AI coding assistants working in this repository. Focus on what to change, where, and how to run the main pipeline.

**Repo Overview**
- Small dataset-focused repo with two parallel pipelines in notebooks: [antares/antares_genre_classifier.ipynb](antares/antares_genre_classifier.ipynb) and [newmag/newmag_genre_classifier.ipynb](newmag/newmag_classifier.ipynb).
- Each notebook: reads a CSV input (e.g., [antares/antares.csv](antares/antares.csv)), detects language, fetches subjects from Open Library, maps subjects to a small genre set, and falls back to a Hugging Face zero-shot model when needed.

**Key Files**
- Notebook driver: [antares/antares_genre_classifier.ipynb](antares/antares_genre_classifier.ipynb) — canonical implementation to mirror when updating `newmag`.
- Inputs: `antares.csv`, `newmag.csv` in each folder.
- Outputs: `*_genres_output.csv` (e.g., [antares/antares_genres_output.csv](antares/antares_genres_output.csv)).
- Per-folder README.md notes dataset specifics: [antares/README.md](antares/README.md), [newmag/README.md](newmag/README.md).

**Big-picture architecture**
- Single-process, data-centric pipeline executed inside the notebook. Data flow is: CSV -> prepare_*(group & clean) -> for each title: language detection -> OpenLibrary subject lookup -> map and/or zero-shot classifier -> aggregate summary -> save CSV.
- Important constants are defined in the notebook: `TOP_K_GENRES`, `GENRE_KEYWORDS`, `LANGUAGE_NAMES`. Changes to mapping or behaviour should usually be made here.

**Project-specific conventions & patterns**
- Prefer the Open Library lookup first (`openlibrary_get_subjects`) and only call the HF zero-shot fallback (`valhalla/distilbart-mnli-12-1`) when no subjects map to known genres.
- Genre mapping is driven by `GENRE_KEYWORDS` (lowercased normalized checks). Add keywords here to extend mapping rather than changing mapping logic.
- Language detection uses a lightweight heuristic + `langid.classify`. Add language names to `LANGUAGE_NAMES` if adding support for new 2-letter codes.
- Outputs append an empty row and a single SUMMARY row with two metrics: top genres by title count and by weighted `Number` sum.

**Integration points & external dependencies**
- Open Library API (`requests.get("https://openlibrary.org/search.json")`) — expect network timeouts; code uses `timeout=20`.
- Hugging Face `transformers` pipeline zero-shot model — requires `transformers` and a PyTorch backend (`torch`). Running offline or without GPUs will be slower.
- `langid` for language classification.

**How to run / developer workflow**
- Preferred: open the notebook in VS Code or Jupyter and run the cells interactively. The notebook already runs end-to-end when executed cell-by-cell.
- To run headless (convert to script):
  - Export a script: `jupyter nbconvert --to script antares/antares_genre_classifier.ipynb`
  - Edit the generated `.py` to ensure paths and env are correct, then run `python antares/antares_genre_classifier.py`.
- Quick install (examples): `python -m pip install pandas requests langid transformers torch`.

**Editing guidance for AI agents**
- Minimal, focused edits only. When adding features prefer changing constants and mappings (`GENRE_KEYWORDS`, `TOP_K_GENRES`) rather than core control flow.
- If adding new external calls, mirror existing error handling: wrap network calls with try/except and fall back quietly to zero-shot classifier or empty subjects.
- Keep the two notebooks consistent: if you change the `antares` notebook behaviour, replicate the same pattern in `newmag`.

**Examples (what to change and where)**
- Add a new keyword for `Science Fiction`: edit the `GENRE_KEYWORDS` block in [antares/antares_genre_classifier.ipynb](antares/antares_genre_classifier.ipynb) and run the pipeline.
- Increase candidate genres per title: change `TOP_K_GENRES = 3` at the top of the notebook.

**Notes / gotchas**
- No top-level `requirements.txt` or CI detected: ensure runtime env has `pandas`, `requests`, `langid`, `transformers`, and `torch` before running notebooks.
- The zero-shot pipeline may download model weights on first run; consider pre-caching in environments that run at scale.

If any part of this guidance is unclear or you want more examples (unit-test patterns, CI steps, or a `requirements.txt`), tell me which section to expand.
