"""
Car Price Prediction - Model Training Script
This script handles data loading, preprocessing, EDA, model training, and evaluation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import pickle
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

print("="*60)
print("CAR PRICE PREDICTION - MODEL TRAINING")
print("="*60)

# ============================================================================
# STEP 1: LOAD DATA
# ============================================================================
print("\n[STEP 1] Loading Data...")
df = pd.read_csv('../data/car_data.csv')
print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset Info:")
print(df.info())

print("\nBasic Statistics:")
print(df.describe())

# ============================================================================
# STEP 2: DATA PREPROCESSING
# ============================================================================
print("\n[STEP 2] Data Preprocessing...")

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check for duplicates
print(f"\nDuplicate rows: {df.duplicated().sum()}")

# Feature Engineering: Create car_age
current_year = 2024
df['car_age'] = current_year - df['Year']
print(f"\nCreated 'car_age' feature")

# Drop unnecessary columns
df = df.drop(['Car_Name', 'Year'], axis=1)
print(f"Dropped 'Car_Name' and 'Year' columns")

print(f"\nFinal dataset shape: {df.shape}")
print("\nFinal columns:", df.columns.tolist())

# ============================================================================
# STEP 3: EXPLORATORY DATA ANALYSIS (EDA)
# ============================================================================
print("\n[STEP 3] Exploratory Data Analysis...")

# 1. Distribution of Selling Price
plt.figure(figsize=(10, 6))
plt.hist(df['Selling_Price'], bins=50, edgecolor='black', alpha=0.7)
plt.xlabel('Selling Price (lakhs)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Car Selling Prices', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)
plt.savefig('../notebooks/01_price_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_price_distribution.png")
plt.close()

# 2. Correlation Heatmap (before encoding)
plt.figure(figsize=(12, 8))
numeric_cols = df.select_dtypes(include=[np.number]).columns
correlation = df[numeric_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=1, fmt='.2f')
plt.title('Correlation Heatmap - Numerical Features', fontsize=14, fontweight='bold')
plt.savefig('../notebooks/02_correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_correlation_heatmap.png")
plt.close()

# 3. Price vs Car Age
plt.figure(figsize=(10, 6))
plt.scatter(df['car_age'], df['Selling_Price'], alpha=0.5, s=20)
plt.xlabel('Car Age (years)', fontsize=12)
plt.ylabel('Selling Price (lakhs)', fontsize=12)
plt.title('Selling Price vs Car Age', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)
plt.savefig('../notebooks/03_price_vs_age.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_price_vs_age.png")
plt.close()

# 4. Price by Fuel Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='Fuel_Type', y='Selling_Price', data=df, palette='Set2')
plt.xlabel('Fuel Type', fontsize=12)
plt.ylabel('Selling Price (lakhs)', fontsize=12)
plt.title('Selling Price by Fuel Type', fontsize=14, fontweight='bold')
plt.savefig('../notebooks/04_price_by_fuel.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_price_by_fuel.png")
plt.close()

# 5. Price by Transmission
plt.figure(figsize=(10, 6))
sns.boxplot(x='Transmission', y='Selling_Price', data=df, palette='Set3')
plt.xlabel('Transmission Type', fontsize=12)
plt.ylabel('Selling Price (lakhs)', fontsize=12)
plt.title('Selling Price by Transmission Type', fontsize=14, fontweight='bold')
plt.savefig('../notebooks/05_price_by_transmission.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 05_price_by_transmission.png")
plt.close()

# 6. Price by Seller Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='Seller_Type', y='Selling_Price', data=df, palette='pastel')
plt.xlabel('Seller Type', fontsize=12)
plt.ylabel('Selling Price (lakhs)', fontsize=12)
plt.title('Selling Price by Seller Type', fontsize=14, fontweight='bold')
plt.savefig('../notebooks/06_price_by_seller.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 06_price_by_seller.png")
plt.close()

print("\n✓ All EDA visualizations saved in 'notebooks' folder")

# ============================================================================
# STEP 4: ENCODE CATEGORICAL VARIABLES
# ============================================================================
print("\n[STEP 4] Encoding Categorical Variables...")

# Store original mappings
encoding_info = {
    'Fuel_Type': {},
    'Seller_Type': {},
    'Transmission': {}
}

# Encode Fuel_Type
le_fuel = LabelEncoder()
df['Fuel_Type_Encoded'] = le_fuel.fit_transform(df['Fuel_Type'])
encoding_info['Fuel_Type'] = dict(zip(le_fuel.classes_, le_fuel.transform(le_fuel.classes_)))
print(f"Fuel_Type encoding: {encoding_info['Fuel_Type']}")

# Encode Seller_Type
le_seller = LabelEncoder()
df['Seller_Type_Encoded'] = le_seller.fit_transform(df['Seller_Type'])
encoding_info['Seller_Type'] = dict(zip(le_seller.classes_, le_seller.transform(le_seller.classes_)))
print(f"Seller_Type encoding: {encoding_info['Seller_Type']}")

# Encode Transmission
le_trans = LabelEncoder()
df['Transmission_Encoded'] = le_trans.fit_transform(df['Transmission'])
encoding_info['Transmission'] = dict(zip(le_trans.classes_, le_trans.transform(le_trans.classes_)))
print(f"Transmission encoding: {encoding_info['Transmission']}")

# Drop original categorical columns
df = df.drop(['Fuel_Type', 'Seller_Type', 'Transmission'], axis=1)

# Rename encoded columns
df = df.rename(columns={
    'Fuel_Type_Encoded': 'Fuel_Type',
    'Seller_Type_Encoded': 'Seller_Type',
    'Transmission_Encoded': 'Transmission'
})

print("\n✓ Categorical variables encoded successfully")

# ============================================================================
# STEP 5: REMOVE OUTLIERS
# ============================================================================
print("\n[STEP 5] Removing Outliers...")

initial_rows = len(df)

# Remove outliers using IQR method for Selling_Price
Q1 = df['Selling_Price'].quantile(0.25)
Q3 = df['Selling_Price'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df = df[(df['Selling_Price'] >= lower_bound) & (df['Selling_Price'] <= upper_bound)]

removed_rows = initial_rows - len(df)
print(f"Removed {removed_rows} outlier rows ({removed_rows/initial_rows*100:.2f}%)")
print(f"Final dataset: {len(df)} rows")

# ============================================================================
# STEP 6: SPLIT DATA
# ============================================================================
print("\n[STEP 6] Splitting Data...")

# Separate features and target
X = df.drop(['Selling_Price'], axis=1)
y = df['Selling_Price']

print(f"\nFeatures (X): {X.shape}")
print(f"Target (y): {y.shape}")
print(f"\nFeature columns: {X.columns.tolist()}")

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

# ============================================================================
# STEP 7: MODEL TRAINING AND EVALUATION
# ============================================================================
print("\n[STEP 7] Training Multiple Models...")

def evaluate_model(y_true, y_pred, model_name):
    """Calculate and display model performance metrics"""
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    print(f"\n{model_name} Performance:")
    print(f"  R² Score: {r2:.4f}")
    print(f"  RMSE: ₹{rmse:.4f} lakhs")
    print(f"  MAE: ₹{mae:.4f} lakhs")
    print(f"  MAPE: {mape:.2f}%")
    
    return {'model': model_name, 'r2': r2, 'rmse': rmse, 'mae': mae, 'mape': mape}

results = []

# Model 1: Linear Regression
print("\n--- Training Linear Regression ---")
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)
results.append(evaluate_model(y_test, y_pred_lr, "Linear Regression"))

# Model 2: Decision Tree
print("\n--- Training Decision Tree ---")
dt = DecisionTreeRegressor(random_state=42, max_depth=10)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
results.append(evaluate_model(y_test, y_pred_dt, "Decision Tree"))

# Model 3: Random Forest (Base)
print("\n--- Training Random Forest (Base) ---")
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
results.append(evaluate_model(y_test, y_pred_rf, "Random Forest (Base)"))

# ============================================================================
# STEP 8: HYPERPARAMETER TUNING
# ============================================================================
print("\n[STEP 8] Hyperparameter Tuning for Random Forest...")

param_dist = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2']
}

print("Running RandomizedSearchCV (this may take a few minutes)...")
rf_random = RandomizedSearchCV(
    RandomForestRegressor(random_state=42),
    param_distributions=param_dist,
    n_iter=20,
    cv=3,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

rf_random.fit(X_train, y_train)

print(f"\n✓ Best parameters found: {rf_random.best_params_}")

# Use best model
best_rf = rf_random.best_estimator_
y_pred_best = best_rf.predict(X_test)
results.append(evaluate_model(y_test, y_pred_best, "Random Forest (Tuned)"))

# ============================================================================
# STEP 9: MODEL COMPARISON
# ============================================================================
print("\n[STEP 9] Model Comparison Summary...")

results_df = pd.DataFrame(results)
print("\n" + "="*70)
print(results_df.to_string(index=False))
print("="*70)

# Find best model
best_model_idx = results_df['r2'].idxmax()
best_model_name = results_df.loc[best_model_idx, 'model']
print(f"\n🏆 Best Model: {best_model_name}")
print(f"   R² Score: {results_df.loc[best_model_idx, 'r2']:.4f}")

# Visualize model comparison
plt.figure(figsize=(12, 6))
x_pos = np.arange(len(results_df))
plt.bar(x_pos, results_df['r2'], alpha=0.8, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
plt.xlabel('Model', fontsize=12)
plt.ylabel('R² Score', fontsize=12)
plt.title('Model Performance Comparison (R² Score)', fontsize=14, fontweight='bold')
plt.xticks(x_pos, results_df['model'], rotation=15, ha='right')
plt.ylim([0, 1])
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(results_df['r2']):
    plt.text(i, v + 0.02, f'{v:.4f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig('../notebooks/07_model_comparison.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: 07_model_comparison.png")
plt.close()

# ============================================================================
# STEP 10: FEATURE IMPORTANCE
# ============================================================================
print("\n[STEP 10] Analyzing Feature Importance...")

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': best_rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\nFeature Importance Ranking:")
print(feature_importance.to_string(index=False))

# Visualize feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_importance['feature'], feature_importance['importance'], color='#45B7D1')
plt.xlabel('Importance', fontsize=12)
plt.ylabel('Feature', fontsize=12)
plt.title('Feature Importance (Random Forest)', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('../notebooks/08_feature_importance.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: 08_feature_importance.png")
plt.close()

# ============================================================================
# STEP 11: PREDICTION VISUALIZATION
# ============================================================================
print("\n[STEP 11] Creating Prediction Visualizations...")

# Actual vs Predicted
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_best, alpha=0.5, s=30)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
         'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Price (lakhs)', fontsize=12)
plt.ylabel('Predicted Price (lakhs)', fontsize=12)
plt.title('Actual vs Predicted Prices (Best Model)', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../notebooks/09_actual_vs_predicted.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 09_actual_vs_predicted.png")
plt.close()

# Residual plot
residuals = y_test - y_pred_best
plt.figure(figsize=(10, 6))
plt.scatter(y_pred_best, residuals, alpha=0.5, s=30)
plt.axhline(y=0, color='r', linestyle='--', lw=2)
plt.xlabel('Predicted Price (lakhs)', fontsize=12)
plt.ylabel('Residuals', fontsize=12)
plt.title('Residual Plot', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('../notebooks/10_residuals.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 10_residuals.png")
plt.close()

# ============================================================================
# STEP 12: SAVE MODEL
# ============================================================================
print("\n[STEP 12] Saving Model and Encodings...")

# Save the best model
with open('../models/car_price_model.pkl', 'wb') as file:
    pickle.dump(best_rf, file)
print("✓ Model saved: models/car_price_model.pkl")

# Save encoding information
with open('../models/encoding_info.pkl', 'wb') as file:
    pickle.dump(encoding_info, file)
print("✓ Encoding info saved: models/encoding_info.pkl")

# Save feature names for reference
feature_names = X.columns.tolist()
with open('../models/feature_names.pkl', 'wb') as file:
    pickle.dump(feature_names, file)
print("✓ Feature names saved: models/feature_names.pkl")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*60)
print("TRAINING COMPLETE! 🎉")
print("="*60)
print(f"\n✓ Best Model: {best_model_name}")
print(f"✓ R² Score: {results_df.loc[best_model_idx, 'r2']:.4f}")
print(f"✓ RMSE: ₹{results_df.loc[best_model_idx, 'rmse']:.4f} lakhs")
print(f"✓ All visualizations saved in 'notebooks/' folder")
print(f"✓ Model files saved in 'models/' folder")
print("\nYou can now use the model for predictions!")
print("="*60)
