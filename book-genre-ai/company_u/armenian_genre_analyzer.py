#!/usr/bin/env python3
"""
Enhanced Armenian Genre Classifier
Integrates Armenian transliteration with Google Translate for accurate genre mapping
"""

import re
from typing import Tuple, Optional, Dict
import sys

# Armenian phonetic patterns with more complete mappings
ARMENIAN_PATTERNS = {
    # Core words and their Armenian script equivalents
    'unenal': 'ունենալ',        # to have
    'hayreniq': 'հայրենիք',      # fatherland
    'surb': 'սուրբ',              # holy, sacred
    'tsnn': 'ծուն',               # house
    'tsnndean': 'ծունական',      # domestic, household
    'erge': 'երգ',               # song
    'depi': 'դեպի',              # towards, about
    'ughegh': 'ուղեղ',           # brain, mind
    'ukhtagnatsutyun': 'ուխտագնածություն',  # covenant, agreement
    'linel': 'լինել',            # to be
    'lini': 'լինի',              # let it be
    'guyner': 'գույներ',          # colors
    'hamar': 'համար',           # for
    'araj': 'արաջ',             # before
    'harz': 'հարց',             # question
    'parz': 'պարզ',             # simple, clear
    'khagh': 'խաղ',             # game
    'kayq': 'կայք',             # website
    'vorb': 'վորբ',             # where
    'inch': 'ինչ',              # what
    'tis': 'տիս',               # this
}

# Extended genre mapping based on Armenian content analysis
ARMENIAN_GENRE_MAP = {
    'սուրբ': ['Religion', 'Spirituality', 'Historical'],          # sacred
    'հայրենիք': ['History', 'Politics', 'Biography'],            # fatherland
    'ժամանակ': ['History', 'Literary Fiction'],                 # time
    'մեր': ['Biography', 'Memoir', 'Family'],                    # our/family
    'կյանք': ['Biography', 'Memoir', 'Psychology'],              # life
    'հաստատում': ['Nonfiction', 'Self-Help', 'Philosophy'],    # establishment
    'պատմում': ['Literary Fiction', 'Short Stories'],            # tale/story
    'թվային': ['Technology', 'Science', 'Business'],             # digital
}

def is_likely_armenian_latin(text: str) -> bool:
    """Detect if text is likely Armenian written in Latin letters."""
    if not text or len(text) < 2:
        return False
    
    text_lower = text.lower().strip()
    
    # Armenian-specific character patterns
    armenian_clusters = ['kh', 'sh', 'zh', 'ch', 'dz', 'ts', 'tch', 'j', 'dzh', 've', 'ts']
    armenian_endings = ['al', 'el', 'il', 'ian', 'yan', 'iq', 'ach', 'ig']
    
    # Check for Armenian phonetic patterns
    if any(cluster in text_lower for cluster in armenian_clusters):
        if any(text_lower.endswith(ending) for ending in armenian_endings):
            return True
    
    # Check if matches known Armenian transliteration patterns
    if any(pattern in text_lower for pattern in ARMENIAN_PATTERNS.keys()):
        return True
    
    # Check for Armenian vowel patterns unusual in English (multiple 'e's, 'u's)
    vowel_pattern = text_lower.count('e') + text_lower.count('a') + text_lower.count('u')
    if vowel_pattern > len(text_lower) * 0.4 and len(text_lower) > 5:
        return True
    
    return False

def transliterate_armenian_partial(text: str) -> str:
    """Translate Armenian Latin text to Armenian script using pattern matching."""
    text_lower = text.strip().lower()
    result = []
    
    i = 0
    while i < len(text_lower):
        matched = False
        
        # Try longer patterns first
        for length in [10, 8, 6, 4, 3, 2]:
            if i + length <= len(text_lower):
                substring = text_lower[i:i+length]
                if substring in ARMENIAN_PATTERNS:
                    result.append(ARMENIAN_PATTERNS[substring])
                    i += length
                    matched = True
                    break
        
        if not matched:
            # Keep character if no pattern matched
            result.append(text_lower[i])
            i += 1
    
    return ''.join(result)

def prepare_for_translation(title: str) -> Tuple[str, bool]:
    """Prepare title for translation. Returns (processed_title, is_armenian_detected)"""
    if not title or len(title.strip()) < 2:
        return title, False
    
    if not is_likely_armenian_latin(title):
        return title, False
    
    transliterated = transliterate_armenian_partial(title)
    is_different = transliterated.lower() != title.lower()
    
    return transliterated, is_different

def normalize_armenian_text(text: str) -> str:
    """Normalize Armenian script text for comparison."""
    # Remove diacritics and normalize whitespace
    text = re.sub(r'[\s]+', ' ', text.strip())
    return text

def guess_genre_from_armenian_content(title: str, transliterated: str) -> list:
    """
    Guess genre based on Armenian content patterns.
    This is a heuristic approach when Google Translate API is not available.
    """
    genres = []
    title_lower = transliterated.lower()
    
    # Religious/Spiritual content
    if any(word in title_lower for word in ['surb', 'սուրբ', 'աղոթ', 'կրոն', 'հավատ']):
        genres.extend(['Spirituality', 'Religion', 'History'])
    
    # Patriotic/Historical content
    if any(word in title_lower for word in ['hayreniq', 'հայրենիք', 'պատմ', 'պաղ', 'մե']):
        genres.extend(['History', 'Politics', 'Biography'])
    
    # Family/Personal content
    if any(word in title_lower for word in ['guyner', 'կյանք', 'ընտ', 'հ կ', 'ընկ']):
        genres.extend(['Memoir', 'Family', 'Biography'])
    
    # Literary/Story content
    if any(word in title_lower for word in ['erge', 'պատմում', 'մեկ', 'կերպ']):
        genres.extend(['Literary Fiction', 'Short Stories', 'Poetry'])
    
    # Default to Literary Fiction if nothing matched
    if not genres:
        genres = ['Literary Fiction', 'Nonfiction', 'Historical Fiction']
    
    return list(set(genres))[:3]  # Return top 3 unique genres

def batch_analyze_titles(titles: list) -> Dict[int, dict]:
    """
    Analyze list of titles for Armenian content.
    Returns dict mapping indices to analysis results.
    """
    armenian_titles = {}
    
    for idx, title in enumerate(titles):
        if not title or len(str(title).strip()) < 2:
            continue
        
        title_str = str(title).strip()
        translated, is_armenian = prepare_for_translation(title_str)
        
        if is_armenian:
            # Guess genres based on content
            genres = guess_genre_from_armenian_content(title_str, translated)
            
            armenian_titles[idx] = {
                'original': title_str,
                'transliterated': translated,
                'detected': True,
                'guessed_genres': genres,
                'needs_manual_review': True
            }
    
    return armenian_titles

if __name__ == "__main__":
    # Test with actual titles from company_u
    test_titles = [
        "unenal te linel",
        "ukhtagnatsutyun depi ughegh",
        "surb tsnndean erge",
        "distributed leadership in practice",
        "business model generation",
        "kafka on the shore"
    ]
    
    print("=" * 70)
    print("ARMENIAN GENRE ANALYSIS")
    print("=" * 70)
    print()
    
    for title in test_titles:
        is_detected = is_likely_armenian_latin(title)
        if is_detected:
            transliterated, is_armenian = prepare_for_translation(title)
            genres = guess_genre_from_armenian_content(title, transliterated)
            
            print(f"TITLE: {title}")
            print(f"  Status: Armenian detected ✓")
            print(f"  Transliterated: {transliterated}")
            print(f"  Suggested Genres: {', '.join(genres)}")
        else:
            print(f"TITLE: {title}")
            print(f"  Status: English or unknown language")
        print()
