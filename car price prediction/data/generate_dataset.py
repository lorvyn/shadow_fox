import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate 5000 car records
n_samples = 5000

# Generate features
data = {
    'Car_Name': [f'Car_{i}' for i in range(n_samples)],
    'Year': np.random.randint(2005, 2024, n_samples),
    'Present_Price': np.random.uniform(2.5, 25.0, n_samples),
    'Kms_Driven': np.random.randint(5000, 150000, n_samples),
    'Fuel_Type': np.random.choice(['Petrol', 'Diesel', 'CNG'], n_samples, p=[0.5, 0.4, 0.1]),
    'Seller_Type': np.random.choice(['Dealer', 'Individual'], n_samples, p=[0.4, 0.6]),
    'Transmission': np.random.choice(['Manual', 'Automatic'], n_samples, p=[0.7, 0.3]),
    'Owner': np.random.choice([0, 1, 2, 3], n_samples, p=[0.5, 0.3, 0.15, 0.05])
}

df = pd.DataFrame(data)


current_year = 2024
df['car_age'] = current_year - df['Year']

# Generate realistic selling prices based on features
# Base price calculation with depreciation
depreciation_rate = 0.85  # 15% depreciation per year
df['Selling_Price'] = df['Present_Price'] * (depreciation_rate ** df['car_age'])

# Adjust for kilometers driven (higher km = lower price)
km_factor = 1 - (df['Kms_Driven'] / 200000) * 0.2
df['Selling_Price'] = df['Selling_Price'] * km_factor

# Adjust for fuel type (Diesel slightly higher, CNG lower)
fuel_adjustment = df['Fuel_Type'].map({'Petrol': 1.0, 'Diesel': 1.08, 'CNG': 0.92})
df['Selling_Price'] = df['Selling_Price'] * fuel_adjustment

# Adjust for seller type (Dealer slightly higher)
seller_adjustment = df['Seller_Type'].map({'Dealer': 1.05, 'Individual': 1.0})
df['Selling_Price'] = df['Selling_Price'] * seller_adjustment


trans_adjustment = df['Transmission'].map({'Manual': 1.0, 'Automatic': 1.15})
df['Selling_Price'] = df['Selling_Price'] * trans_adjustment

# Adjust for owners (more owners = lower price)
owner_adjustment = 1 - (df['Owner'] * 0.05)
df['Selling_Price'] = df['Selling_Price'] * owner_adjustment

# Add some random noise
noise = np.random.normal(0, 0.5, n_samples)
df['Selling_Price'] = df['Selling_Price'] * (1 + noise * 0.1)


df['Selling_Price'] = df['Selling_Price'].clip(0.5, df['Present_Price'] * 0.95)

# Round to 2 decimal places
df['Selling_Price'] = df['Selling_Price'].round(2)
df['Present_Price'] = df['Present_Price'].round(2)

# Reorder columns
df = df[['Car_Name', 'Year', 'Selling_Price', 'Present_Price', 'Kms_Driven', 
         'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']]

df.to_csv('car_data.csv', index=False)
print(f"Dataset created successfully with {len(df)} records!")
print(f"\nFirst few rows:")
print(df.head())
print(f"\nDataset statistics:")
print(df.describe())
