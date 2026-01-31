"""
Demo Script for Autocorrect System
Demonstrates the core functionality without GUI
"""

from spell_checker import AutocorrectEngine
import time


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*70 + "\n")


def demo_basic_spell_check():
    """Demonstrate basic spell checking"""
    print("DEMO 1: Basic Spell Checking")
    print_separator()
    
    engine = AutocorrectEngine()
    
    test_words = [
        ("hello", True),
        ("wrld", False),
        ("python", True),
        ("speling", False),
        ("computer", True),
        ("programing", False),
    ]
    
    print("Checking individual words:\n")
    for word, expected in test_words:
        is_valid = engine.is_valid_word(word)
        status = "✓ CORRECT" if is_valid else "✗ MISSPELLED"
        print(f"  '{word:15}' → {status}")
        
        if not is_valid:
            suggestions = engine.get_suggestions(word, max_suggestions=3)
            print(f"  {'':15}   Suggestions: {', '.join(suggestions)}")
    
    print_separator()


def demo_text_processing():
    """Demonstrate processing full text"""
    print("DEMO 2: Text Processing")
    print_separator()
    
    engine = AutocorrectEngine()
    
    # Sample text with intentional errors
    test_text = "Thsi is a smple exampel of text procesing with som mispelled wrods."
    
    print("Original text:")
    print(f"  '{test_text}'\n")
    
    print("Processing...\n")
    errors = engine.process_text(test_text)
    
    print(f"Found {len(errors)} errors:\n")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. Word: '{error['word']}'")
        print(f"     Position: {error['start']}-{error['end']}")
        print(f"     Top 3 suggestions: {', '.join(error['suggestions'][:3])}")
        
        if error['auto_correct']:
            print(f"     ⚡ Auto-correct: '{error['correction']}'")
        print()
    
    print_separator()


def demo_auto_correction():
    """Demonstrate auto-correction logic"""
    print("DEMO 3: Auto-Correction")
    print_separator()
    
    engine = AutocorrectEngine()
    
    common_typos = [
        "teh",      # the
        "adn",      # and
        "recieve",  # receive
        "occured",  # occurred
        "seperate", # separate
        "definately", # definitely
    ]
    
    print("Testing common typo patterns:\n")
    for typo in common_typos:
        should_correct, correction = engine.should_auto_correct(typo)
        
        if should_correct:
            print(f"  '{typo}' → '{correction}' ⚡ (auto-corrected)")
        else:
            suggestions = engine.get_suggestions(typo, max_suggestions=1)
            if suggestions:
                print(f"  '{typo}' → '{suggestions[0]}' (suggested)")
    
    print_separator()


def demo_custom_dictionary():
    """Demonstrate custom dictionary functionality"""
    print("DEMO 4: Custom Dictionary")
    print_separator()
    
    engine = AutocorrectEngine()
    
    # Technical terms and names
    custom_words = ["TensorFlow", "GitHub", "PostgreSQL", "Kubernetes"]
    
    print("Before adding to dictionary:\n")
    for word in custom_words:
        is_valid = engine.is_valid_word(word)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{word}'")
    
    print("\nAdding words to custom dictionary...\n")
    for word in custom_words:
        engine.add_to_dictionary(word)
        print(f"  + Added '{word}'")
    
    print("\nAfter adding to dictionary:\n")
    for word in custom_words:
        is_valid = engine.is_valid_word(word)
        status = "✓" if is_valid else "✗"
        print(f"  {status} '{word}'")
    
    print_separator()


def demo_learning():
    """Demonstrate learning from corrections"""
    print("DEMO 5: Learning System")
    print_separator()
    
    engine = AutocorrectEngine()
    
    print("Scenario: User repeatedly corrects 'tpyo' to 'typo'\n")
    
    # First time
    print("1st occurrence:")
    should_correct, correction = engine.should_auto_correct("tpyo")
    print(f"   Should auto-correct: {should_correct}")
    print(f"   Suggestion: {correction}")
    
    # Record the correction
    print("\n   User selects: 'typo'")
    engine.record_correction("tpyo", "typo")
    print("   ✓ Correction recorded\n")
    
    # Second time
    print("2nd occurrence:")
    should_correct, correction = engine.should_auto_correct("tpyo")
    print(f"   Should auto-correct: {should_correct}")
    print(f"   Suggestion: {correction}")
    print(f"\n   {'⚡ Now auto-corrects!' if should_correct else 'Still suggesting'}")
    
    print_separator()


def demo_performance():
    """Demonstrate performance with large text"""
    print("DEMO 6: Performance Test")
    print_separator()
    
    engine = AutocorrectEngine()
    
    # Generate large text
    sentence = "This is a simple sentence with some words in it. "
    large_text = sentence * 100  # 100 sentences
    
    word_count = len(large_text.split())
    
    print(f"Processing text with {word_count} words...\n")
    
    start_time = time.time()
    errors = engine.process_text(large_text)
    end_time = time.time()
    
    elapsed = end_time - start_time
    words_per_second = word_count / elapsed if elapsed > 0 else 0
    
    print(f"  ✓ Processed in {elapsed:.3f} seconds")
    print(f"  ✓ Speed: {words_per_second:.0f} words/second")
    print(f"  ✓ Found {len(errors)} errors")
    
    print_separator()


def demo_suggestion_ranking():
    """Demonstrate how suggestions are ranked"""
    print("DEMO 7: Suggestion Ranking")
    print_separator()
    
    engine = AutocorrectEngine()
    
    test_words = ["programing", "recieve", "occured", "seperate"]
    
    print("Showing top 5 ranked suggestions:\n")
    for word in test_words:
        suggestions = engine.get_suggestions(word, max_suggestions=5)
        print(f"  '{word}':")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"    {i}. {suggestion}")
        print()
    
    print_separator()


def demo_real_world_example():
    """Demonstrate real-world usage scenario"""
    print("DEMO 8: Real-World Example")
    print_separator()
    
    engine = AutocorrectEngine()
    
    # Simulate writing an email
    email_text = """
    Dear Team,
    
    I wanted to breif you on the progres we've made with the new porject.
    We have sucessfully completed teh initial phase and are now movign to
    the next stge. Please let me know if you have any questons or concernss.
    
    Best regards
    """
    
    print("Original email draft:")
    print(email_text)
    
    print("\nProcessing for errors...\n")
    errors = engine.process_text(email_text)
    
    print(f"Found {len(errors)} spelling errors:\n")
    
    corrections = []
    for error in errors:
        original = error['word']
        suggestion = error['suggestions'][0] if error['suggestions'] else "?"
        corrections.append((original, suggestion))
        
        if error['auto_correct']:
            print(f"  • '{original}' → '{suggestion}' (auto-corrected)")
        else:
            print(f"  • '{original}' → '{suggestion}' (suggested)")
    
    print("\nApplying corrections...")
    
    corrected_text = email_text
    for original, suggestion in corrections:
        corrected_text = corrected_text.replace(original, suggestion)
    
    print("\nCorrected email:")
    print(corrected_text)
    
    print_separator()


def main():
    """Run all demonstrations"""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          Autocorrect Keyboard System - Demo Script              ║
    ║                    Feature Demonstrations                        ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    demos = [
        ("Basic Spell Checking", demo_basic_spell_check),
        ("Text Processing", demo_text_processing),
        ("Auto-Correction", demo_auto_correction),
        ("Custom Dictionary", demo_custom_dictionary),
        ("Learning System", demo_learning),
        ("Performance Test", demo_performance),
        ("Suggestion Ranking", demo_suggestion_ranking),
        ("Real-World Example", demo_real_world_example),
    ]
    
    print("\nThis demo will showcase all features of the autocorrect system.")
    print("Press Enter to continue between demos, or Ctrl+C to exit.\n")
    
    try:
        for name, demo_func in demos:
            input(f"Press Enter to run: {name}...")
            demo_func()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        return
    
    print("\n" + "="*70)
    print("\n✓ All demonstrations completed!")
    print("\nTo use the full GUI application, run: python main.py")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
