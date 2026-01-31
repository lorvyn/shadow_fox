"""
Unit Tests for Spell Checker Module
Tests core functionality of the autocorrect engine
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spell_checker import AutocorrectEngine


class TestAutocorrectEngine(unittest.TestCase):
    """Test cases for AutocorrectEngine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = AutocorrectEngine()
    
    def test_valid_word(self):
        """Test detection of correctly spelled words"""
        self.assertTrue(self.engine.is_valid_word("hello"))
        self.assertTrue(self.engine.is_valid_word("python"))
        self.assertTrue(self.engine.is_valid_word("computer"))
        self.assertTrue(self.engine.is_valid_word("world"))
    
    def test_invalid_word(self):
        """Test detection of misspelled words"""
        self.assertFalse(self.engine.is_valid_word("helo"))
        self.assertFalse(self.engine.is_valid_word("wrld"))
        self.assertFalse(self.engine.is_valid_word("speling"))
        self.assertFalse(self.engine.is_valid_word("computr"))
    
    def test_suggestions_generated(self):
        """Test that suggestions are generated for misspelled words"""
        suggestions = self.engine.get_suggestions("helo")
        self.assertGreater(len(suggestions), 0)
        self.assertIn("hello", suggestions)
        
        suggestions = self.engine.get_suggestions("wrld")
        self.assertGreater(len(suggestions), 0)
        self.assertIn("world", suggestions)
    
    def test_suggestions_limit(self):
        """Test that suggestions respect the max limit"""
        suggestions = self.engine.get_suggestions("test", max_suggestions=3)
        self.assertLessEqual(len(suggestions), 3)
    
    def test_common_typos(self):
        """Test auto-correction of common typos"""
        should_correct, correction = self.engine.should_auto_correct("teh")
        self.assertTrue(should_correct)
        self.assertEqual(correction, "the")
        
        should_correct, correction = self.engine.should_auto_correct("adn")
        self.assertTrue(should_correct)
        self.assertEqual(correction, "and")
    
    def test_custom_dictionary(self):
        """Test adding words to custom dictionary"""
        # Add a custom word
        custom_word = "testword123"
        self.engine.add_to_dictionary(custom_word)
        
        # Check if it's now valid
        self.assertTrue(self.engine.is_valid_word(custom_word))
    
    def test_tokenization(self):
        """Test text tokenization"""
        text = "Hello world, this is a test."
        words = self.engine._tokenize(text)
        
        self.assertEqual(len(words), 6)
        self.assertEqual(words[0][0], "Hello")
        self.assertEqual(words[1][0], "world")
        self.assertEqual(words[2][0], "this")
    
    def test_process_text(self):
        """Test processing entire text"""
        text = "Thsi is a smple test with som errors."
        errors = self.engine.process_text(text)
        
        # Should find at least 3 errors (Thsi, smple, som)
        self.assertGreaterEqual(len(errors), 3)
        
        # Check that errors have required fields
        for error in errors:
            self.assertIn('word', error)
            self.assertIn('suggestions', error)
            self.assertIn('start', error)
            self.assertIn('end', error)
    
    def test_correction_history(self):
        """Test recording and using correction history"""
        # Record a correction
        self.engine.record_correction("mistke", "mistake")
        
        # Check if it's in history
        self.assertIn("mistke", self.engine.correction_history)
        self.assertEqual(self.engine.correction_history["mistke"], "mistake")
    
    def test_edit_distance(self):
        """Test edit distance calculation"""
        # Identical strings
        self.assertEqual(self.engine._edit_distance("hello", "hello"), 0)
        
        # One character difference
        self.assertEqual(self.engine._edit_distance("hello", "helo"), 1)
        
        # Multiple differences
        self.assertGreater(self.engine._edit_distance("hello", "world"), 3)
    
    def test_empty_input(self):
        """Test handling of empty or invalid input"""
        self.assertTrue(self.engine.is_valid_word(""))
        self.assertEqual(len(self.engine.get_suggestions("")), 0)
    
    def test_non_alphabetic(self):
        """Test handling of non-alphabetic characters"""
        # Numbers should be considered valid (not checked)
        self.assertTrue(self.engine.is_valid_word("123"))
        
        # Special characters should be valid (not checked)
        self.assertTrue(self.engine.is_valid_word("!!!"))
    
    def test_suggestion_ranking(self):
        """Test that suggestions are properly ranked"""
        suggestions = self.engine.get_suggestions("programing")
        
        # "programming" should be high in the list
        self.assertIn("programming", suggestions[:3])
    
    def test_case_insensitive(self):
        """Test that checking is case-insensitive"""
        self.assertTrue(self.engine.is_valid_word("Hello"))
        self.assertTrue(self.engine.is_valid_word("HELLO"))
        self.assertTrue(self.engine.is_valid_word("hello"))


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = AutocorrectEngine()
    
    def test_complete_correction_workflow(self):
        """Test complete workflow from detection to correction"""
        # Input text with errors
        text = "This is a smple text with som mispelled wrods."
        
        # Process text
        errors = self.engine.process_text(text)
        
        # Should find errors
        self.assertGreater(len(errors), 0)
        
        # All errors should have suggestions
        for error in errors:
            self.assertGreater(len(error['suggestions']), 0)
    
    def test_learning_workflow(self):
        """Test that the engine learns from corrections"""
        # Make a correction
        self.engine.record_correction("tpyo", "typo")
        
        # Check if it affects future suggestions
        should_auto, correction = self.engine.should_auto_correct("tpyo")
        
        # After learning, it should be more confident
        self.assertEqual(correction, "typo")


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestAutocorrectEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == "__main__":
    print("="*60)
    print("Running Autocorrect Engine Tests")
    print("="*60)
    print()
    
    success = run_tests()
    
    print()
    print("="*60)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
    print("="*60)
    
    sys.exit(0 if success else 1)
