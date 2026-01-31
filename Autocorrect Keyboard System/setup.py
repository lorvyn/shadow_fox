#!/usr/bin/env python3
"""
Setup and Installation Script
Autocorrect Keyboard System
"""

import subprocess
import sys
import os


def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print("   Please upgrade Python and try again.")
        return False
    
    print("✓ Python version is compatible")
    return True


def install_dependencies():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    try:
        print("Installing pyspellchecker...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "pyspellchecker==0.7.2", "--quiet"
        ])
        print("✓ pyspellchecker installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error: Failed to install dependencies")
        print("   Try running: pip install pyspellchecker")
        return False


def check_tkinter():
    """Check if tkinter is available"""
    print_header("Checking GUI Framework")
    
    try:
        import tkinter
        print("✓ tkinter is available")
        return True
    except ImportError:
        print("❌ Error: tkinter is not available")
        print("\n   Installation instructions:")
        print("   - Ubuntu/Debian: sudo apt-get install python3-tk")
        print("   - Fedora: sudo dnf install python3-tkinter")
        print("   - macOS: brew install python-tk")
        print("   - Windows: tkinter should be included with Python")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        "dictionaries",
        "config",
        "logs",
        "tests"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created: {directory}/")
        else:
            print(f"  Already exists: {directory}/")
    
    return True


def test_installation():
    """Test if the installation works"""
    print_header("Testing Installation")
    
    try:
        # Try importing the main modules
        from spell_checker import AutocorrectEngine
        print("✓ Spell checker module loaded")
        
        # Try creating an engine instance
        engine = AutocorrectEngine()
        print("✓ Autocorrect engine initialized")
        
        # Test basic functionality
        result = engine.is_valid_word("test")
        print("✓ Basic spell checking works")
        
        return True
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False


def print_success_message():
    """Print success message and usage instructions"""
    print_header("Installation Complete!")
    
    print("🎉 Autocorrect Keyboard System is ready to use!\n")
    print("To start the application, run:")
    print("  python main.py\n")
    print("Features:")
    print("  ✓ Real-time spell checking")
    print("  ✓ Smart autocorrection")
    print("  ✓ Custom dictionary support")
    print("  ✓ Learning from corrections")
    print("  ✓ Right-click suggestions\n")
    print("For help and documentation, see README.md")
    print("\n" + "="*60 + "\n")


def main():
    """Main setup function"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║       Autocorrect Keyboard System - Setup Script        ║
    ║                      Version 1.0.0                       ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Checking GUI framework", check_tkinter),
        ("Creating directories", create_directories),
        ("Testing installation", test_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please fix the errors and run setup.py again.")
            sys.exit(1)
    
    print_success_message()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
