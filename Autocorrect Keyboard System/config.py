"""
Configuration Module
Contains settings and constants for the autocorrect system
"""

# Application Settings
APP_NAME = "Autocorrect Keyboard System"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Your Name"

# Spell Checker Settings
DEFAULT_LANGUAGE = "en"
MAX_SUGGESTIONS = 5
AUTO_CORRECT_THRESHOLD = 0.9
CHECK_DELAY_MS = 300  # Milliseconds to wait before checking

# Dictionary Paths
CUSTOM_DICT_PATH = "dictionaries/custom_words.json"
USER_PREFS_PATH = "config/user_preferences.json"

# UI Settings
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
FONT_FAMILY = "Arial"
FONT_SIZE = 12
EDITOR_FONT_SIZE = 12

# Color Scheme
ERROR_COLOR = "red"
CORRECTION_COLOR = "lightgreen"
STATUS_ACTIVE_COLOR = "green"
STATUS_INACTIVE_COLOR = "orange"

# Highlighting Settings
UNDERLINE_ERRORS = True
HIGHLIGHT_CORRECTIONS = True
CORRECTION_HIGHLIGHT_DURATION = 2000  # Milliseconds

# Auto-Correction Settings
ENABLE_AUTO_CORRECT_DEFAULT = True
ENABLE_HIGHLIGHTING_DEFAULT = True

# Common Typo Patterns
# These will be auto-corrected with high confidence
COMMON_TYPOS = {
    'teh': 'the',
    'adn': 'and',
    'waht': 'what',
    'thsi': 'this',
    'taht': 'that',
    'recieve': 'receive',
    'occured': 'occurred',
    'seperate': 'separate',
    'definately': 'definitely',
    'wich': 'which',
    'wiht': 'with',
    'hte': 'the',
    'fro': 'for',
    'fo': 'of',
    'yuor': 'your',
    'tath': 'that',
    'freind': 'friend',
    'becuase': 'because',
    'woudl': 'would',
    'coudl': 'could',
    'shoudl': 'should',
}

# Keyboard Proximity Map (for better typo detection)
# Maps each key to its neighboring keys
KEYBOARD_PROXIMITY = {
    'q': ['w', 'a', 's'],
    'w': ['q', 'e', 'a', 's', 'd'],
    'e': ['w', 'r', 's', 'd', 'f'],
    'r': ['e', 't', 'd', 'f', 'g'],
    't': ['r', 'y', 'f', 'g', 'h'],
    'y': ['t', 'u', 'g', 'h', 'j'],
    'u': ['y', 'i', 'h', 'j', 'k'],
    'i': ['u', 'o', 'j', 'k', 'l'],
    'o': ['i', 'p', 'k', 'l'],
    'p': ['o', 'l'],
    'a': ['q', 'w', 's', 'z'],
    's': ['a', 'w', 'e', 'd', 'z', 'x'],
    'd': ['s', 'e', 'r', 'f', 'x', 'c'],
    'f': ['d', 'r', 't', 'g', 'c', 'v'],
    'g': ['f', 't', 'y', 'h', 'v', 'b'],
    'h': ['g', 'y', 'u', 'j', 'b', 'n'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'z': ['a', 's', 'x'],
    'x': ['z', 's', 'd', 'c'],
    'c': ['x', 'd', 'f', 'v'],
    'v': ['c', 'f', 'g', 'b'],
    'b': ['v', 'g', 'h', 'n'],
    'n': ['b', 'h', 'j', 'm'],
    'm': ['n', 'j', 'k'],
}

# Performance Settings
ENABLE_THREADING = True
MAX_TEXT_LENGTH = 100000  # Characters
CACHE_SIZE = 1000  # Number of words to cache

# Learning Settings
ENABLE_LEARNING = True
MIN_CORRECTIONS_TO_LEARN = 2  # How many times a correction must be made to learn

# Export Settings
EXPORT_FORMATS = ['txt', 'rtf', 'html']
DEFAULT_EXPORT_FORMAT = 'txt'

# Debug Settings
DEBUG_MODE = False
LOG_CORRECTIONS = True
LOG_FILE = "logs/autocorrect.log"
