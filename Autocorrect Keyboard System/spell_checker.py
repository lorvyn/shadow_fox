"""
Spell Checker Module
Handles spell checking, suggestions, and auto-correction logic
"""

from spellchecker import SpellChecker
import json
import os
from typing import List, Tuple, Dict

class AutocorrectEngine:
    """Main spell checking and autocorrection engine"""
    
    def __init__(self, custom_dict_path='dictionaries/custom_words.json'):
        """Initialize the spell checker with default and custom dictionaries"""
        self.spell = SpellChecker()
        self.custom_dict_path = custom_dict_path
        self.custom_words = set()
        self.correction_history = {}  # Track user's correction choices
        self.auto_correct_threshold = 0.9  # Confidence threshold for auto-correction
        
        # Load custom dictionary if exists
        self.load_custom_dictionary()
    
    def load_custom_dictionary(self):
        """Load custom words from JSON file"""
        if os.path.exists(self.custom_dict_path):
            try:
                with open(self.custom_dict_path, 'r') as f:
                    data = json.load(f)
                    self.custom_words = set(data.get('words', []))
                    self.spell.word_frequency.load_words(self.custom_words)
            except Exception as e:
                print(f"Error loading custom dictionary: {e}")
    
    def save_custom_dictionary(self):
        """Save custom words to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.custom_dict_path), exist_ok=True)
            with open(self.custom_dict_path, 'w') as f:
                json.dump({'words': list(self.custom_words)}, f, indent=2)
        except Exception as e:
            print(f"Error saving custom dictionary: {e}")
    
    def add_to_dictionary(self, word: str):
        """Add a word to custom dictionary"""
        word_lower = word.lower()
        self.custom_words.add(word_lower)
        self.spell.word_frequency.load_words([word_lower])
        self.save_custom_dictionary()
    
    def is_valid_word(self, word: str) -> bool:
        """Check if a word is spelled correctly"""
        if not word or not word.isalpha():
            return True  # Skip non-alphabetic strings
        
        word_lower = word.lower()
        
        # Check in custom dictionary first
        if word_lower in self.custom_words:
            return True
        
        # Check in main dictionary
        misspelled = self.spell.unknown([word_lower])
        return len(misspelled) == 0
    
    def get_suggestions(self, word: str, max_suggestions: int = 5) -> List[str]:
        """Get correction suggestions for a misspelled word"""
        if not word or not word.isalpha():
            return []
        
        word_lower = word.lower()
        
        # Get candidates from spell checker
        candidates = self.spell.candidates(word_lower)
        
        if not candidates:
            return []
        
        # Rank suggestions
        ranked_suggestions = self._rank_suggestions(word_lower, candidates)
        
        # Return top N suggestions
        return ranked_suggestions[:max_suggestions]
    
    def _rank_suggestions(self, original: str, candidates: set) -> List[str]:
        """Rank suggestions based on multiple factors"""
        scored_suggestions = []
        
        for candidate in candidates:
            score = 0
            
            # Factor 1: Word frequency (higher frequency = higher score)
            try:
                frequency = self.spell.word_frequency[candidate]
            except KeyError:
                frequency = 0
            score += frequency * 100
            
            # Factor 2: Edit distance (fewer edits = higher score)
            edit_dist = self._edit_distance(original, candidate)
            score += (10 - edit_dist) * 50  # Inverse scoring
            
            # Factor 3: User history (if user has chosen this before)
            if original in self.correction_history:
                if candidate == self.correction_history[original]:
                    score += 200  # Boost previously chosen corrections
            
            # Factor 4: Length similarity
            len_diff = abs(len(original) - len(candidate))
            score += (10 - len_diff) * 10
            
            scored_suggestions.append((candidate, score))
        
        # Sort by score (descending)
        scored_suggestions.sort(key=lambda x: x[1], reverse=True)
        
        return [word for word, score in scored_suggestions]
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings"""
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                # Cost of insertions, deletions, or substitutions
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def should_auto_correct(self, word: str) -> Tuple[bool, str]:
        """
        Determine if word should be auto-corrected
        Returns: (should_correct, correction)
        """
        suggestions = self.get_suggestions(word, max_suggestions=3)
        
        if not suggestions:
            return False, ""
        
        top_suggestion = suggestions[0]
        
        # Auto-correct if:
        # 1. There's only one suggestion OR
        # 2. The top suggestion has been used before for this typo OR
        # 3. It's a very common typo pattern
        
        if len(suggestions) == 1:
            return True, top_suggestion
        
        if word.lower() in self.correction_history:
            if self.correction_history[word.lower()] == top_suggestion:
                return True, top_suggestion
        
        # Common typo patterns (keyboard proximity)
        common_typos = {
            'teh': 'the',
            'adn': 'and',
            'waht': 'what',
            'thsi': 'this',
            'taht': 'that',
            'recieve': 'receive',
            'occured': 'occurred',
            'seperate': 'separate',
        }
        
        if word.lower() in common_typos:
            return True, common_typos[word.lower()]
        
        return False, top_suggestion
    
    def record_correction(self, original: str, correction: str):
        """Record user's correction choice for learning"""
        self.correction_history[original.lower()] = correction.lower()
    
    def process_text(self, text: str) -> List[Dict]:
        """
        Process entire text and return list of errors with suggestions
        Returns: List of dicts with {word, position, suggestions}
        """
        words = self._tokenize(text)
        errors = []
        
        for word, start_pos, end_pos in words:
            if not self.is_valid_word(word):
                suggestions = self.get_suggestions(word)
                auto_correct, correction = self.should_auto_correct(word)
                
                errors.append({
                    'word': word,
                    'start': start_pos,
                    'end': end_pos,
                    'suggestions': suggestions,
                    'auto_correct': auto_correct,
                    'correction': correction
                })
        
        return errors
    
    def _tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Tokenize text into words with their positions
        Returns: List of (word, start_position, end_position)
        """
        words = []
        current_word = ""
        start_pos = 0
        
        for i, char in enumerate(text):
            if char.isalpha() or char == "'":  # Include apostrophes
                if not current_word:
                    start_pos = i
                current_word += char
            else:
                if current_word:
                    words.append((current_word, start_pos, i))
                    current_word = ""
        
        # Don't forget the last word
        if current_word:
            words.append((current_word, start_pos, len(text)))
        
        return words


# Example usage
if __name__ == "__main__":
    # Initialize engine
    engine = AutocorrectEngine()
    
    # Test spell checking
    test_words = ["hello", "wrld", "python", "speling", "correct"]
    
    print("Testing spell checker:")
    for word in test_words:
        is_correct = engine.is_valid_word(word)
        if not is_correct:
            suggestions = engine.get_suggestions(word)
            print(f"'{word}' is misspelled. Suggestions: {suggestions}")
        else:
            print(f"'{word}' is correct")
    
    print("\n" + "="*50 + "\n")
    
    # Test text processing
    test_text = "Thsi is a smple text with som mispelled wrods."
    print(f"Processing text: '{test_text}'")
    errors = engine.process_text(test_text)
    
    print(f"\nFound {len(errors)} errors:")
    for error in errors:
        print(f"  - '{error['word']}' at position {error['start']}")
        print(f"    Suggestions: {error['suggestions'][:3]}")
        if error['auto_correct']:
            print(f"    Auto-correct to: '{error['correction']}'")
