"""
Car Price Prediction - Flask Web Application
Backend server for the web interface
"""

from flask import Flask, render_template, request
import pickle
import numpy as np
import os

app = Flask(__name__, template_folder='../templates')

# Get the correct paths relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'car_price_model.pkl')
ENCODING_PATH = os.path.join(BASE_DIR, 'models', 'encoding_info.pkl')

try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    with open(ENCODING_PATH, 'rb') as file:
        encoding_info = pickle.load(file)
    print("✓ Model loaded successfully!")
except FileNotFoundError as e:
    print(f"Error: Model files not found at {MODEL_PATH}")
    print("Please ensure the models folder exists in the project root.")
    exit(1)

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html', encoding_info=encoding_info)

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get data from form
        present_price = float(request.form['present_price'])
        kms_driven = float(request.form['kms_driven'])
        fuel_type = int(request.form['fuel_type'])
        seller_type = int(request.form['seller_type'])
        transmission = int(request.form['transmission'])
        owner = int(request.form['owner'])
        car_age = int(request.form['car_age'])
        
        # Validate inputs
        if present_price <= 0 or kms_driven <= 0 or car_age < 0 or owner < 0:
            return render_template('index.html', 
                                 prediction_text='Error: Please enter valid positive numbers!',
                                 error=True,
                                 encoding_info=encoding_info)
        
        # Create feature array (order: Present_Price, Kms_Driven, Owner, car_age, Fuel_Type, Seller_Type, Transmission)
        features = np.array([[present_price, kms_driven, owner, car_age, 
                            fuel_type, seller_type, transmission]])
        
        # Predict
        prediction = model.predict(features)[0]
        
        # Calculate depreciation
        depreciation = present_price - prediction
        depreciation_percent = (depreciation / present_price) * 100
        
        # Create result message
        prediction_text = f'💰 Predicted Selling Price: ₹{prediction:.2f} lakhs'
        depreciation_text = f'📉 Depreciation: ₹{depreciation:.2f} lakhs ({depreciation_percent:.1f}%)'
        
        # Get original names for display
        fuel_name = [k for k, v in encoding_info['Fuel_Type'].items() if v == fuel_type][0]
        seller_name = [k for k, v in encoding_info['Seller_Type'].items() if v == seller_type][0]
        trans_name = [k for k, v in encoding_info['Transmission'].items() if v == transmission][0]
        
        return render_template('index.html', 
                             prediction_text=prediction_text,
                             depreciation_text=depreciation_text,
                             input_summary={
                                 'present_price': present_price,
                                 'kms_driven': kms_driven,
                                 'fuel_type': fuel_name,
                                 'seller_type': seller_name,
                                 'transmission': trans_name,
                                 'owner': owner,
                                 'car_age': car_age
                             },
                             encoding_info=encoding_info)
    
    except ValueError:
        return render_template('index.html', 
                             prediction_text='Error: Please enter valid numbers in all fields!',
                             error=True,
                             encoding_info=encoding_info)
    except Exception as e:
        return render_template('index.html', 
                             prediction_text=f'Error: {str(e)}',
                             error=True,
                             encoding_info=encoding_info)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("  CAR PRICE PREDICTION - WEB APPLICATION")
    print("="*60)
    print("\n🌐 Starting Flask server...")
    print("📍 Open your browser and go to: http://127.0.0.1:5000")
    print("⚠️  Press CTRL+C to stop the server\n")
    app.run(debug=True, port=5000)
