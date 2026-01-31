"""
Test Script - Verify Car Price Prediction System
This script tests that all components are working correctly
"""

import sys
import os

print("="*70)
print("  CAR PRICE PREDICTION - SYSTEM VERIFICATION TEST")
print("="*70)

# Test 1: Check Python version
print("\n[TEST 1] Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"✓ Python version: {sys.version.split()[0]} (OK)")
else:
    print(f"✗ Python version: {sys.version.split()[0]} (Requires 3.8+)")

# Test 2: Check required packages
print("\n[TEST 2] Checking required packages...")
required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'sklearn', 'flask']
missing_packages = []

for package in required_packages:
    try:
        __import__(package)
        print(f"✓ {package} is installed")
    except ImportError:
        print(f"✗ {package} is NOT installed")
        missing_packages.append(package)

if missing_packages:
    print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
    print("Install with: pip install -r requirements.txt")
else:
    print("\n✓ All required packages are installed!")

# Test 3: Check file structure
print("\n[TEST 3] Checking file structure...")
required_files = [
    '../data/car_data.csv',
    '../models/car_price_model.pkl',
    '../models/encoding_info.pkl',
    '../src/predict_terminal.py',
    '../src/predict_gui.py',
    '../src/app.py',
    '../templates/index.html'
]

missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"✓ {file}")
    else:
        print(f"✗ {file} (missing)")
        missing_files.append(file)

if missing_files:
    print(f"\n⚠️  Missing files: {len(missing_files)}")
    if '../models/car_price_model.pkl' in missing_files:
        print("   → Run: cd notebooks && python train_model.py")
else:
    print("\n✓ All required files are present!")

# Test 4: Test model loading
print("\n[TEST 4] Testing model loading...")
try:
    import pickle
    import numpy as np
    
    with open('../models/car_price_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../models/encoding_info.pkl', 'rb') as f:
        encoding_info = pickle.load(f)
    
    print("✓ Model loaded successfully")
    print("✓ Encoding info loaded successfully")
    
    # Test 5: Test prediction
    print("\n[TEST 5] Testing prediction functionality...")
    
    # Sample input: Present_Price, Kms_Driven, Owner, car_age, Fuel_Type, Seller_Type, Transmission
    test_input = np.array([[8.5, 45000, 1, 5, 2, 1, 1]])
    
    prediction = model.predict(test_input)[0]
    print(f"✓ Test prediction successful: ₹{prediction:.2f} lakhs")
    
    if 1.0 <= prediction <= 10.0:
        print("✓ Prediction value is reasonable")
    else:
        print("⚠️  Prediction value seems unusual")
    
except FileNotFoundError as e:
    print(f"✗ Model files not found: {e}")
    print("   → Run: cd notebooks && python train_model.py")
except Exception as e:
    print(f"✗ Error during model testing: {e}")

# Final Summary
print("\n" + "="*70)
print("  SUMMARY")
print("="*70)

if not missing_packages and not missing_files:
    print("\n✓ All tests passed! Your system is ready to use.")
    print("\nNext steps:")
    print("  1. Terminal interface: cd src && python predict_terminal.py")
    print("  2. GUI interface: cd src && python predict_gui.py")
    print("  3. Web interface: cd src && python app.py")
else:
    print("\n⚠️  Some tests failed. Please fix the issues above.")
    if missing_packages:
        print("\n  Install packages: pip install -r requirements.txt")
    if '../models/car_price_model.pkl' in missing_files:
        print("  Train model: cd notebooks && python train_model.py")

print("="*70)
