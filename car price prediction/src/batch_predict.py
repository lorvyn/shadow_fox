"""
Batch Prediction Script
Predict prices for multiple cars from a CSV file
"""

import pickle
import pandas as pd
import numpy as np

# Load model and encodings
MODEL_PATH = '../models/car_price_model.pkl'
ENCODING_PATH = '../models/encoding_info.pkl'

print("="*70)
print("  CAR PRICE PREDICTION - BATCH PROCESSING")
print("="*70)

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

def create_sample_batch():
    """Create a sample batch file for demonstration"""
    sample_data = {
        'Present_Price': [8.5, 12.0, 5.5, 15.0, 6.8],
        'Kms_Driven': [45000, 30000, 80000, 20000, 55000],
        'Fuel_Type': ['Petrol', 'Diesel', 'CNG', 'Diesel', 'Petrol'],
        'Seller_Type': ['Individual', 'Dealer', 'Individual', 'Dealer', 'Individual'],
        'Transmission': ['Manual', 'Automatic', 'Manual', 'Automatic', 'Manual'],
        'Owner': [1, 0, 2, 0, 1],
        'car_age': [5, 3, 8, 2, 6]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_csv('../data/sample_batch.csv', index=False)
    print("✓ Sample batch file created: data/sample_batch.csv")
    return df

def encode_data(df, encoding_info):
    """Encode categorical variables"""
    df_encoded = df.copy()
    
    # Encode Fuel_Type,Transmission, Seller_Type
    fuel_map = encoding_info['Fuel_Type']
    df_encoded['Fuel_Type'] = df_encoded['Fuel_Type'].map(fuel_map)
    
    seller_map = encoding_info['Seller_Type']
    df_encoded['Seller_Type'] = df_encoded['Seller_Type'].map(seller_map)
    
    trans_map = encoding_info['Transmission']
    df_encoded['Transmission'] = df_encoded['Transmission'].map(trans_map)
    
    return df_encoded

def batch_predict(input_file):
    """Process batch predictions from CSV file"""
    
    print(f"\n📂 Loading file: {input_file}")
    
    try:
        df = pd.read_csv(input_file)
        print(f"✓ Loaded {len(df)} cars for prediction")
        
        print("\n📋 Input data preview:")
        print(df.head())
        
        # Encode categorical variables
        df_encoded = encode_data(df, encoding_info)
        
        # Ensure correct column order to match training
        # Training order: Present_Price, Kms_Driven, Fuel_Type, Seller_Type, Transmission, Owner, car_age
        # But model expects: Present_Price, Kms_Driven, Owner, car_age, Fuel_Type, Seller_Type, Transmission (after reordering)
        
        # Create feature array in the correct order
        X = df_encoded[['Present_Price', 'Kms_Driven', 'Owner', 'car_age', 'Fuel_Type', 'Seller_Type', 'Transmission']].values
        
        # Make predictions
        print("\n🔮 Making predictions...")
        predictions = model.predict(X)
        
        # Add predictions to dataframe
        df['Predicted_Price'] = predictions
        df['Depreciation'] = df['Present_Price'] - df['Predicted_Price']
        df['Depreciation_Percent'] = (df['Depreciation'] / df['Present_Price']) * 100
        
        
        print("\n" + "="*70)
        print("  PREDICTION RESULTS")
        print("="*70)
        
        for idx, row in df.iterrows():
            print(f"\nCar {idx + 1}:")
            print(f"  Present Price: ₹{row['Present_Price']:.2f} lakhs")
            print(f"  Kilometers: {row['Kms_Driven']:,.0f} km")
            print(f"  Age: {row['car_age']} years")
            print(f"  Fuel: {row['Fuel_Type']}, Seller: {row['Seller_Type']}, Trans: {row['Transmission']}")
            print(f"  Owners: {row['Owner']}")
            print(f"  → PREDICTED PRICE: ₹{row['Predicted_Price']:.2f} lakhs")
            print(f"  → Depreciation: ₹{row['Depreciation']:.2f} lakhs ({row['Depreciation_Percent']:.1f}%)")
        
        # Save results
        output_file = input_file.replace('.csv', '_predictions.csv')
        df.to_csv(output_file, index=False)
        print("\n" + "="*70)
        print(f"✓ Results saved to: {output_file}")
        print("="*70)
        
        
        print("\n📊 Summary Statistics:")
        print(f"  Total Cars: {len(df)}")
        print(f"  Average Present Price: ₹{df['Present_Price'].mean():.2f} lakhs")
        print(f"  Average Predicted Price: ₹{df['Predicted_Price'].mean():.2f} lakhs")
        print(f"  Average Depreciation: {df['Depreciation_Percent'].mean():.1f}%")
        print(f"  Price Range: ₹{df['Predicted_Price'].min():.2f} - ₹{df['Predicted_Price'].max():.2f} lakhs")
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found!")
        print("\nCreating a sample batch file for you...")
        df = create_sample_batch()
        print("\n💡 Try running: python batch_predict.py")
        print("   It will now use the sample batch file.")
        return
    except KeyError as e:
        print(f"❌ Error: Missing required column: {e}")
        print("\nRequired columns:")
        print("  - Present_Price")
        print("  - Kms_Driven")
        print("  - Fuel_Type (Petrol/Diesel/CNG)")
        print("  - Seller_Type (Dealer/Individual)")
        print("  - Transmission (Manual/Automatic)")
        print("  - Owner (0-3)")
        print("  - car_age (years)")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    import sys
    
    # Check if file is provided
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        # Try sample file first
        input_file = '../data/sample_batch.csv'
        
        if not pd.io.common.file_exists(input_file):
            print("ℹ️  No input file specified. Creating sample batch file...")
            create_sample_batch()
            print("\n💡 Usage: python batch_predict.py [input_file.csv]")
            print("   Example: python batch_predict.py ../data/sample_batch.csv")
            print("\n   Or just run without arguments to use the sample file.")
    
    batch_predict(input_file)

if __name__ == "__main__":
    main()
