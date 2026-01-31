"""
Car Price Prediction - Terminal Interface
Simple command-line interface for car price predictions
"""

import pickle
import numpy as np
import os

# Load model and encodings
MODEL_PATH = '../models/car_price_model.pkl'
ENCODING_PATH = '../models/encoding_info.pkl'

print("="*60)
print("        CAR PRICE PREDICTION - TERMINAL INTERFACE")
print("="*60)

try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    with open(ENCODING_PATH, 'rb') as file:
        encoding_info = pickle.load(file)
    print("\n✓ Model loaded successfully!")
except FileNotFoundError:
    print("\n❌ Error: Model files not found!")
    print("Please run train_model.py first to create the model.")
    exit(1)

def print_encoding_info():
    """Display encoding information for user reference"""
    print("\n" + "-"*60)
    print("ENCODING REFERENCE:")
    print("-"*60)
    for feature, mappings in encoding_info.items():
        print(f"\n{feature}:")
        for key, value in mappings.items():
            print(f"  {value} = {key}")
    print("-"*60)

def get_user_input():
    """Get car details from user"""
    print("\n📝 Please enter car details:\n")
    
    try:
        present_price = float(input("Present Price (in lakhs, e.g., 8.5): "))
        kms_driven = float(input("Kilometers Driven (e.g., 45000): "))
        
        print(f"\nFuel Type - {encoding_info['Fuel_Type']}")
        fuel_type = int(input("Enter Fuel Type code: "))
        
        print(f"\nSeller Type - {encoding_info['Seller_Type']}")
        seller_type = int(input("Enter Seller Type code: "))
        
        print(f"\nTransmission - {encoding_info['Transmission']}")
        transmission = int(input("Enter Transmission code: "))
        
        owner = int(input("\nNumber of Previous Owners (0-3): "))
        car_age = int(input("Age of Car (in years, e.g., 5): "))
        
        return present_price, kms_driven, fuel_type, seller_type, transmission, owner, car_age
    
    except ValueError:
        print("\n❌ Invalid input! Please enter valid numbers.")
        return None

def predict_price():
    """Main prediction function"""
    
    # Show encoding reference
    print_encoding_info()
    
    # Get inputs
    inputs = get_user_input()
    if inputs is None:
        return False
    
    present_price, kms_driven, fuel_type, seller_type, transmission, owner, car_age = inputs
    
    # Validate inputs
    if fuel_type not in encoding_info['Fuel_Type'].values():
        print(f"\n❌ Invalid Fuel Type code! Must be one of: {list(encoding_info['Fuel_Type'].values())}")
        return False
    
    if seller_type not in encoding_info['Seller_Type'].values():
        print(f"\n❌ Invalid Seller Type code! Must be one of: {list(encoding_info['Seller_Type'].values())}")
        return False
    
    if transmission not in encoding_info['Transmission'].values():
        print(f"\n❌ Invalid Transmission code! Must be one of: {list(encoding_info['Transmission'].values())}")
        return False
    
    # Create feature array (order: Present_Price, Kms_Driven, Owner, car_age, Fuel_Type, Seller_Type, Transmission)
    features = np.array([[present_price, kms_driven, owner, car_age, fuel_type, seller_type, transmission]])
    
    # Predict
    try:
        predicted_price = model.predict(features)[0]
        
        # Display result
        print("\n" + "="*60)
        print("                    PREDICTION RESULT")
        print("="*60)
        print(f"\n🚗 Car Details:")
        print(f"   Present Price: ₹{present_price:.2f} lakhs")
        print(f"   Kilometers Driven: {kms_driven:,.0f} km")
        print(f"   Age: {car_age} years")
        print(f"   Fuel Type: {[k for k, v in encoding_info['Fuel_Type'].items() if v == fuel_type][0]}")
        print(f"   Seller Type: {[k for k, v in encoding_info['Seller_Type'].items() if v == seller_type][0]}")
        print(f"   Transmission: {[k for k, v in encoding_info['Transmission'].items() if v == transmission][0]}")
        print(f"   Previous Owners: {owner}")
        
        print(f"\n💰 PREDICTED SELLING PRICE: ₹{predicted_price:.2f} lakhs")
        
        # Calculate depreciation
        depreciation = present_price - predicted_price
        depreciation_percent = (depreciation / present_price) * 100
        print(f"   Depreciation: ₹{depreciation:.2f} lakhs ({depreciation_percent:.1f}%)")
        
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during prediction: {str(e)}")
        return False

def main():
    """Main program loop"""
    while True:
        success = predict_price()
        
        print("\n" + "-"*60)
        continue_pred = input("\nPredict another car price? (yes/no): ").strip().lower()
        
        if continue_pred not in ['yes', 'y']:
            print("\n" + "="*60)
            print("        Thank you for using Car Price Predictor!")
            print("="*60)
            break
        
        print("\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("        Program interrupted. Goodbye!")
        print("="*60)
