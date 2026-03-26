#!/usr/bin/env python3
"""
Armenian Transliteration Module
Converts Armenian words written in Latin letters to Armenian script
and prepares for Google Translate API lookups
"""

import re
from typing import Tuple, Optional

# Phonetic Armenian → Armenian script mapping (ISO 9985 / BGVN romanization)
ARMENIAN_MAP = {
    # Single characters
    'a': 'ա',    'b': 'բ',    'g': 'գ',    'd': 'դ',    'e': 'ե',
    'z': 'զ',    'e': 'ե',    't': 'թ',    'j': 'ժ',    'i': 'ի',
    'l': 'լ',    'x': 'խ',    'c': 'ծ',    'k': 'կ',    'h': 'հ',
    'j': 'ճ',    'm': 'մ',    'y': 'յ',    'n': 'ն',    'sh': 'շ',
    'o': 'ո',    'ch': 'չ',    'p': 'պ',    'j': 'ջ',    'r': 'ր',
    's': 'ս',    'v': 'վ',    't': 'տ',    'r': 'ռ',    'c': 'ց',
    'w': 'ւ',    'p': 'փ',    'u': 'ւ',
}

# Common Armenian phonetic patterns (for transliteration reverse-engineering)
ARMENIAN_PATTERNS = {
    # Common Armenian prefixes/suffixes
    'tsnnd': 'ծուն',        # house
    'surb': 'սուրբ',        # holy
    'unenal': 'ունենալ',    # to have
    'erge': 'երգե',         # song
    'ukhtagnatsutyun': 'ուխտագնածություն',  # covenant
    'depi': 'դեպի',         # towards
    'ughegh': 'ուղեղ',      # brain
    'hayreniq': 'Հայրենիք',  # Fatherland
    'haghardzag': 'հաղարձակ', # abundant
}

def is_likely_armenian_latin(text: str) -> bool:
    """Detect if text is likely Armenian written in Latin letters."""
    if not text or len(text) < 3:
        return False
    
    # Check for Armenian phonetic patterns
    text_lower = text.lower()
    
    # Common Armenian consonant clusters that rarely appear in English
    armenian_clusters = ['tch', 'dzh', 'ts', 'kh', 'sh', 'zh', 'ch', 'dz']
    
    # Check for non-English vowel patterns
    if any(text_lower.startswith(cluster) for cluster in armenian_clusters):
        return True
    
    # Check if matches known Armenian transliteration patterns
    if any(pattern in text_lower for pattern in ARMENIAN_PATTERNS.keys()):
        return True
    
    return False

def transliterate_armenian(text: str) -> Optional[str]:
    """
    Attempt to transliterate Armenian text from Latin letters to Armenian script.
    Uses pattern matching and phonetic rules.
    """
    text_lower = text.strip().lower()
    
    # Try pattern matching first (most reliable)
    for pattern, armenian in ARMENIAN_PATTERNS.items():
        if pattern in text_lower:
            # Replace pattern with Armenian equivalent
            result = text_lower.replace(pattern, armenian)
            return result
    
    # Character-by-character transliteration (less reliable)
    result = []
    i = 0
    while i < len(text_lower):
        # Try two-character patterns first
        if i + 1 < len(text_lower):
            two_char = text_lower[i:i+2]
            if two_char in ARMENIAN_MAP:
                result.append(ARMENIAN_MAP[two_char])
                i += 2
                continue
        
        # Single character
        char = text_lower[i]
        if char in ARMENIAN_MAP:
            result.append(ARMENIAN_MAP[char])
        else:
            result.append(char)  # Keep unrecognized characters
        i += 1
    
    return ''.join(result)

def prepare_for_translation(title: str) -> Tuple[str, bool]:
    """
    Prepare book title for Google Translate API lookup.
    Returns (processed_title, is_armenian_detected)
    """
    if not title or len(title.strip()) < 2:
        return title, False
    
    # Check if Armenian pattern detected
    if not is_likely_armenian_latin(title):
        return title, False
    
    # Attempt transliteration
    try:
        transliterated = transliterate_armenian(title)
        if transliterated and transliterated != title.lower():
            return transliterated, True
    except Exception:
        pass
    
    return title, False

def batch_process_titles(titles: list) -> dict:
    """
    Process list of titles and return mapping of Armenian-detected titles.
    Returns dict with indices and transliterated forms.
    """
    armenian_titles = {}
    
    for idx, title in enumerate(titles):
        processed, is_armenian = prepare_for_translation(title)
        if is_armenian:
            armenian_titles[idx] = {
                'original': title,
                'processed': processed,
                'detected': True
            }
    
    return armenian_titles

if __name__ == "__main__":
    # Test examples
    test_titles = [
        "unenal te linel",
        "ukhtagnatsutyun depi ughegh",
        "surb tsnndean erge",
        "business model generation",
        "kafka on the shore"
    ]
    
    print("Armenian Transliteration Tests")
    print("=" * 60)
    
    for title in test_titles:
        is_armenian = is_likely_armenian_latin(title)
        transliterated = transliterate_armenian(title) if is_armenian else None
        print(f"Title: {title}")
        print(f"  → Armenian detected: {is_armenian}")
        if transliterated:
            print(f"  → Transliterated: {transliterated}")
        print()
