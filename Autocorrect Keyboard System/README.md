# Autocorrect Keyboard System

A real-time spell checker and autocorrection tool built with Python. This application helps improve typing accuracy by automatically detecting and correcting misspelled words as you type.

## Author Information

**Name:** [R.VIGNESH]  
**Date:** January 2025

## Features

✅ **Real-time Spell Checking** - Checks words as you type with minimal delay  
✅ **Smart Autocorrection** - Automatically corrects common typos  
✅ **Suggestion System** - Right-click on misspelled words for correction suggestions  
✅ **Custom Dictionary** - Add your own words (names, technical terms, etc.)  
✅ **Learning Capability** - Learns from your correction choices  
✅ **Visual Feedback** - Red underlines for errors, green highlights for corrections  
✅ **Undo/Redo Support** - Full undo/redo functionality  
✅ **Word Count** - Real-time word counting  

## Screenshots

```
┌─────────────────────────────────────────────────────┐
│ File  Settings  Help                                │
├─────────────────────────────────────────────────────┤
│ ✓ Autocorrect: ON | Highlight: ON    [Add Word] [Clear] │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Type your text here...                             │
│                                                     │
│  Misspelled words will be underlined in red.       │
│  Right-click for suggestions!                       │
│                                                     │
├─────────────────────────────────────────────────────┤
│ Start typing... Errors will be highlighted    Words: 12 │
└─────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Python
Make sure Python is installed on your system:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install pyspellchecker
```

### Step 3: Run the Application
```bash
python main.py
```

## Usage Guide

### Basic Usage

1. **Start the Application**
   ```bash
   python main.py
   ```

2. **Begin Typing**
   - Type naturally in the text area
   - Misspelled words will be underlined in red after a brief pause
   - Common typos are auto-corrected automatically

3. **View Suggestions**
   - Right-click on any misspelled word
   - Select from the suggested corrections
   - The word will be replaced and highlighted briefly in green

### Features Explanation

#### Auto-Correction
- **How it works**: Common typos are automatically replaced
- **Examples**: 
  - "teh" → "the"
  - "recieve" → "receive"
  - "seperate" → "separate"
- **Control**: Toggle in Settings menu

#### Custom Dictionary
- **Add Words**: 
  1. Select the word you want to add
  2. Click "Add Word to Dictionary" button
  3. Or right-click and select "Add to dictionary"
- **Use Case**: Add names, technical terms, company-specific words

#### Learning System
- The system learns from your corrections
- If you repeatedly choose the same correction for a typo, it will auto-correct it in the future
- Makes the system more personalized over time

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Z` | Undo last change |
| `Ctrl+Y` | Redo change |
| `Right-click` | Show suggestions for word under cursor |

### Menu Options

#### File Menu
- **Clear Text**: Remove all text from the editor
- **Exit**: Close the application

#### Settings Menu
- **Enable Autocorrect**: Toggle automatic correction on/off
- **Highlight Errors**: Toggle red underlining of errors

#### Help Menu
- **About**: View application information

## Configuration

The application uses three main configuration files:

### 1. Custom Dictionary
**Location**: `dictionaries/custom_words.json`
- Stores words you've added
- Persists between sessions
- Format: JSON array of words

### 2. Configuration
**Location**: `config.py`
- Application settings
- Customizable parameters
- Typo patterns

### 3. Correction History
- Stored in memory during session
- Used for learning user preferences

## Project Structure

```
autocorrect-system/
├── main.py                      # Application entry point
├── spell_checker.py             # Core spell-checking engine
├── ui_interface.py              # GUI implementation
├── config.py                    # Configuration settings
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── dictionaries/
│   └── custom_words.json        # User's custom dictionary
└── tests/
    └── test_spell_checker.py    # Unit tests
```

## How It Works

### Architecture Overview

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Text Widget    │ ◄── Captures typing
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Debouncing     │ ◄── 300ms delay
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Spell Checker   │ ◄── Analyzes text
│    Engine       │
└────────┬────────┘
         │
         ├──► Valid words ──► No action
         │
         └──► Invalid words ──┐
                              │
                              ▼
                    ┌──────────────────┐
                    │   Auto-correct?  │
                    └─────────┬────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                YES │                   │ NO
                    │                   │
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │   Replace    │    │  Underline   │
            │ Automatically│    │  Show Red    │
            └──────────────┘    └──────────────┘
```

### Spell Checking Algorithm

1. **Tokenization**: Break text into individual words
2. **Validation**: Check each word against dictionary
3. **Suggestion Generation**: For invalid words, generate top 5 suggestions
4. **Ranking**: Score suggestions based on:
   - Edit distance (Levenshtein)
   - Word frequency
   - User history
   - Length similarity
5. **Auto-correct Decision**: 
   - Auto-correct if confidence > 90%
   - Otherwise, show suggestions

## Advanced Features

### Custom Typo Patterns

You can add your own common typo patterns in `config.py`:

```python
COMMON_TYPOS = {
    'youre': 'your',  # Add your patterns
    'their': 'there',
    # ... more patterns
}
```

### Performance Optimization

- **Debouncing**: 300ms delay before checking (configurable)
- **Threading**: Spell checking runs in background
- **Caching**: Frequently checked words are cached
- **Smart Updates**: Only checks modified sections

### Learning System

The system learns from your corrections:
1. User corrects "tpyo" to "typo"
2. System records: `tpyo → typo`
3. Next time "tpyo" appears, it's auto-corrected to "typo"

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Or test manually:
```bash
python spell_checker.py
```

## Troubleshooting

### Issue: Application won't start
**Solution**: 
```bash
pip install --upgrade pyspellchecker
```

### Issue: tkinter not found
**Solution** (Linux):
```bash
sudo apt-get install python3-tk
```

**Solution** (macOS):
```bash
brew install python-tk
```

### Issue: Slow performance
**Solution**: 
- Reduce text length (< 10,000 words works best)
- Increase debounce delay in `config.py`
- Disable auto-correct for large documents

### Issue: Wrong suggestions
**Solution**:
- Add correct words to custom dictionary
- The system will learn from your corrections over time

## Customization

### Change Colors
Edit `config.py`:
```python
ERROR_COLOR = "red"           # Change to "orange", "darkred", etc.
CORRECTION_COLOR = "lightgreen"  # Change highlight color
```

### Adjust Timing
Edit `config.py`:
```python
CHECK_DELAY_MS = 300  # Increase for less frequent checks
```

### Add Language Support
```python
from spellchecker import SpellChecker

# In spell_checker.py
spell = SpellChecker(language='es')  # Spanish
spell = SpellChecker(language='fr')  # French
```


## Credits

- **SpellChecker Library**: pyspellchecker
- **GUI Framework**: tkinter 

---
