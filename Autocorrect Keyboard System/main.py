"""
Main Application Entry Point
Autocorrect Keyboard System
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui_interface import main

if __name__ == "__main__":
    print("="*60)
    print("Starting Autocorrect Keyboard System...")
    print("="*60)
    print("\nFeatures:")
    print("  ✓ Real-time spell checking")
    print("  ✓ Smart autocorrection")
    print("  ✓ Custom dictionary support")
    print("  ✓ Right-click for suggestions")
    print("  ✓ Learning from corrections")
    print("\nKeyboard Shortcuts:")
    print("  • Ctrl+Z : Undo")
    print("  • Ctrl+Y : Redo")
    print("  • Right-click on misspelled word for suggestions")
    print("\n" + "="*60 + "\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication closed by user.")
    except Exception as e:
        print(f"\nError starting application: {e}")
        print("Please ensure all dependencies are installed:")
        print("  pip install pyspellchecker")
        sys.exit(1)
