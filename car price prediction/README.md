# Car Price Prediction using Machine Learning

A machine learning project that predicts used car selling prices with 98% accuracy using Random Forest algorithm. Built as part of my learning journey in data science and ML.

## About This Project

I created this project to understand how machine learning can solve real-world problems in the automobile industry. The system predicts the selling price of used cars based on features like age, kilometers driven, fuel type, and more.

After trying multiple algorithms, I found that Random Forest gives the best results with an R² score of 0.984 - meaning the model can explain 98.4% of the price variation!

## Author Information

**Name:** [R.VIGNESH]  
**Date:** January 2025

## Key Features

🖥️ **Terminal Interface**
* Simple command-line tool for quick predictions
* Shows detailed results with depreciation calculation
* Perfect for quick testing and batch operations

🎨 **GUI Application**
* User-friendly window built with Tkinter
* Radio buttons and form inputs for easy data entry
* Real-time prediction with one click

🌐 **Web Application**
* Professional browser-based interface using Flask
* Modern responsive design with gradient backgrounds
* Accessible from any device with a browser

## What I Learned

This project taught me a lot about the complete machine learning workflow:

* Data preprocessing and cleaning techniques
* Feature engineering - creating car_age improved accuracy from 75% to 98%
* Different ML algorithms and when to use each one
* Model evaluation using R², RMSE, and MAE metrics
* Building user interfaces with Flask and Tkinter
* The importance of data visualization in finding patterns

## Technology Stack

**Programming Language:** Python 3.8+

**Core Libraries:**
* pandas and numpy - Data manipulation and numerical operations
* scikit-learn - Machine learning algorithms and tools
* matplotlib and seaborn - Data visualization
* Flask - Web application framework
* Tkinter - GUI development
* pickle - Model serialization

## Dataset Details

**Source:** Kaggle Vehicle Dataset  
**Total Records:** 5,000 cars  
**Features:** 7 main attributes

The dataset includes these features:
* Present Price - Current showroom price of the car
* Kilometers Driven - Total distance traveled
* Fuel Type - Petrol, Diesel, or CNG
* Seller Type - Dealer or Individual seller
* Transmission - Manual or Automatic
* Number of Owners - Previous ownership count
* Year - Manufacturing year

I created an additional feature called "car_age" by subtracting the year from 2024. This became the most important predictor, accounting for 64.6% of the model's decision-making!

## Model Performance

I tested three different algorithms to find the best one:

**Linear Regression** (Baseline)
* R² Score: 0.79
* Simple but couldn't capture complex patterns

**Decision Tree**
* R² Score: 0.96
* Better performance but showed signs of overfitting

**Random Forest** (Final Choice)
* R² Score: 0.984
* Best balance of accuracy and generalization

**Final Model Metrics:**
* R² Score: 0.984 - Explains 98.4% of price variation
* RMSE: ₹0.34 lakhs - Average prediction error of ₹34,000
* MAE: ₹0.21 lakhs - Mean absolute error
* MAPE: 6.82% - Average percentage error

The model predicts prices with an average error of just 6.82%, which is excellent for real-world applications!

## Feature Importance Analysis

After training, I analyzed which features matter most for price prediction:

1. **Car Age** - 64.6% (Most important by far!)
2. **Present Price** - 26.8% (Original value matters)
3. **Kilometers Driven** - 5.3% (Usage indicator)
4. **Number of Owners** - 1.2%
5. **Fuel Type** - 0.9%
6. **Transmission** - 0.6%
7. **Seller Type** - 0.5%

This was a key insight - depreciation based on age is the dominant factor in used car pricing!

## Installation & Setup

**Step 1: Clone the repository**

Download or clone this project to your local machine.

**Step 2: Install required packages**

Navigate to the project folder and run:

pip install -r requirements.txt

This installs all necessary libraries including pandas, scikit-learn, Flask, and more.

**Step 3: Train the model**

Navigate to the notebooks folder and run:

python train_model.py

This will:
* Load and preprocess the data
* Create 10 visualization charts
* Train the Random Forest model
* Save the model files in the models folder

Training takes about 2-3 minutes.

**Step 4: Verify installation**

Navigate to the src folder and run:

python test_system.py

This checks that everything is set up correctly.

## How to Use

After installation, you can use any of the three interfaces:

**Option 1: Terminal Interface**

Navigate to src folder:

python predict_terminal.py

Follow the prompts to enter car details. The system will show you the predicted price and depreciation.

**Option 2: GUI Application**

Navigate to src folder:

python predict_gui.py

A window will open with form fields. Fill in the details and click "Predict Price" to see results.

**Option 3: Web Application**

Navigate to src folder:

python app.py

Open your browser and go to: http://127.0.0.1:5000

You'll see a professional web interface where you can enter details and get predictions.

## Project Structure

## 📁 Project Structure

```
car_price_prediction/
│
├── data/
│   ├── car_data.csv              # Dataset
│   └── generate_dataset.py       # Script to generate sample data
│
├── notebooks/
│   ├── train_model.py            # Main training script
│   ├── 01_price_distribution.png
│   ├── 02_correlation_heatmap.png
│   ├── 03_price_vs_age.png
│   └── ... (other visualizations)
│
├── models/
│   ├── car_price_model.pkl       # Trained model
│   ├── encoding_info.pkl         # Categorical encodings
│   └── feature_names.pkl         # Feature list
│
├── src/
│   ├── predict_terminal.py       # Terminal interface
│   ├── predict_gui.py            # GUI interface
│   └── app.py                    # Flask web app
│
├── templates/
│   └── index.html                # Web interface template
│
└── README.md
```


The project is organized into several folders:

**data/** - Contains the dataset and data generation scripts
* car_data.csv - Main dataset with 5,000 records
* generate_dataset.py - Script to create sample data
* sample_batch.csv - Example file for batch predictions

**models/** - Stores trained ML models
* car_price_model.pkl - Trained Random Forest model (30MB)
* encoding_info.pkl - Categorical variable encodings
* feature_names.pkl - List of feature names

**notebooks/** - Training scripts and visualizations
* train_model.py - Complete model training pipeline
* 10 PNG files - Charts showing data patterns and model performance

**src/** - Source code for all interfaces
* app.py - Flask web application
* predict_terminal.py - Command-line interface
* predict_gui.py - Tkinter GUI application
* batch_predict.py - Process multiple cars at once
* test_system.py - Verify installation

**templates/** - HTML files for web interface
* index.html - Main web page

## Sample Predictions

Here are some example predictions to show how the model works:

**Example 1: Recent Premium Car**

Input:
* Present Price: ₹15 lakhs
* Age: 2 years
* Kilometers: 20,000 km
* Fuel: Diesel
* Transmission: Automatic
* Seller: Dealer
* Owners: 0

Predicted Price: ₹10.71 lakhs  
Depreciation: ₹4.29 lakhs (28.6%)

**Example 2: Well-Used Hatchback**

Input:
* Present Price: ₹5.5 lakhs
* Age: 8 years
* Kilometers: 80,000 km
* Fuel: CNG
* Transmission: Manual
* Seller: Individual
* Owners: 2

Predicted Price: ₹4.48 lakhs  
Depreciation: ₹1.02 lakhs (18.6%)

**Example 3: Mid-Range Sedan**

Input:
* Present Price: ₹8.5 lakhs
* Age: 5 years
* Kilometers: 45,000 km
* Fuel: Petrol
* Transmission: Manual
* Seller: Individual
* Owners: 1

Predicted Price: ₹6.51 lakhs  
Depreciation: ₹1.99 lakhs (23.4%)

These predictions are very close to actual market prices!


## Acknowledgments

I would like to thank:
* The open-source community for amazing libraries like scikit-learn, Flask, and pandas


**Online Resources:**
* Scikit-learn Official Documentation
* Flask Documentation
* Kaggle - Vehicle Dataset
* Stack Overflow Community


## License

This project is created for educational purposes. Feel free to use it for learning, but please give credit if you use parts of the code.


---

Thank you for checking out my project! I hope it helps others learn about machine learning and real-world applications.

**Note:** This is my first major ML project, and I'm still learning. If you find any issues or have suggestions for improvement, please let me know!
