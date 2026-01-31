"""
Car Price Prediction - GUI Interface
Graphical user interface using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pickle
import numpy as np

# Load model and encodings
MODEL_PATH = '../models/car_price_model.pkl'
ENCODING_PATH = '../models/encoding_info.pkl'

try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    with open(ENCODING_PATH, 'rb') as file:
        encoding_info = pickle.load(file)
except FileNotFoundError:
    print("Error: Model files not found! Please run train_model.py first.")
    exit(1)

def predict():
    """Make prediction based on user inputs"""
    try:
        # Get values from entry fields
        present_price = float(present_price_entry.get())
        kms_driven = float(kms_entry.get())
        fuel_type = fuel_var.get()
        seller_type = seller_var.get()
        transmission = trans_var.get()
        owner = int(owner_entry.get())
        car_age = int(age_entry.get())
        
        # Validate inputs
        if present_price <= 0 or kms_driven <= 0 or car_age < 0 or owner < 0:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers!")
            return
        
        # Create feature array (order: Present_Price, Kms_Driven, Owner, car_age, Fuel_Type, Seller_Type, Transmission)
        features = np.array([[present_price, kms_driven, owner, car_age, 
                            fuel_type, seller_type, transmission]])
        
        prediction = model.predict(features)[0]
        
        # Calculate depreciation
        depreciation = present_price - prediction
        depreciation_percent = (depreciation / present_price) * 100
        
        # Display result
        result_text = f"Predicted Selling Price: ₹{prediction:.2f} lakhs\n"
        result_text += f"Depreciation: ₹{depreciation:.2f} lakhs ({depreciation_percent:.1f}%)"
        
        result_label.config(text=result_text, fg="#2ecc71", font=("Arial", 12, "bold"))
        
    except ValueError:
        messagebox.showerror("Invalid Input", 
                           "Please enter valid numbers in all fields!")
        result_label.config(text="", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        result_label.config(text="", fg="red")

def clear_fields():
    """Clear all input fields"""
    present_price_entry.delete(0, tk.END)
    kms_entry.delete(0, tk.END)
    owner_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    fuel_var.set(2)  # Default to Petrol
    seller_var.set(1)  # Default to Individual
    trans_var.set(1)  # Default to Manual
    result_label.config(text="")

# Create main window
root = tk.Tk()
root.title("Car Price Predictor")
root.geometry("550x700")
root.resizable(False, False)
root.configure(bg="#ecf0f1")

# Title Frame
title_frame = tk.Frame(root, bg="#3498db", height=80)
title_frame.pack(fill="x")
title_frame.pack_propagate(False)

title_label = tk.Label(title_frame, text="🚗 Car Price Predictor", 
                      font=("Arial", 24, "bold"), bg="#3498db", fg="white")
title_label.pack(pady=20)

# Main content frame
content_frame = tk.Frame(root, bg="#ecf0f1", padx=30, pady=20)
content_frame.pack(fill="both", expand=True)

# Style configuration
label_font = ("Arial", 10, "bold")
entry_font = ("Arial", 10)

# Present Price
tk.Label(content_frame, text="Present Price (lakhs):", font=label_font, 
         bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=8)
present_price_entry = tk.Entry(content_frame, font=entry_font, width=25)
present_price_entry.grid(row=0, column=1, pady=8, padx=10)
present_price_entry.insert(0, "8.5")

# Kilometers Driven
tk.Label(content_frame, text="Kilometers Driven:", font=label_font, 
         bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=8)
kms_entry = tk.Entry(content_frame, font=entry_font, width=25)
kms_entry.grid(row=1, column=1, pady=8, padx=10)
kms_entry.insert(0, "45000")

# Fuel Type
tk.Label(content_frame, text="Fuel Type:", font=label_font, 
         bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=8)
fuel_frame = tk.Frame(content_frame, bg="#ecf0f1")
fuel_frame.grid(row=2, column=1, sticky="w", pady=8, padx=10)
fuel_var = tk.IntVar(value=2)  # Default to Petrol

for text, value in [("CNG", 0), ("Diesel", 1), ("Petrol", 2)]:
    tk.Radiobutton(fuel_frame, text=text, variable=fuel_var, value=value,
                  font=("Arial", 9), bg="#ecf0f1").pack(side="left", padx=5)

# Seller Type
tk.Label(content_frame, text="Seller Type:", font=label_font, 
         bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=8)
seller_frame = tk.Frame(content_frame, bg="#ecf0f1")
seller_frame.grid(row=3, column=1, sticky="w", pady=8, padx=10)
seller_var = tk.IntVar(value=1)  # Default to Individual

for text, value in [("Dealer", 0), ("Individual", 1)]:
    tk.Radiobutton(seller_frame, text=text, variable=seller_var, value=value,
                  font=("Arial", 9), bg="#ecf0f1").pack(side="left", padx=5)

# Transmission
tk.Label(content_frame, text="Transmission:", font=label_font, 
         bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=8)
trans_frame = tk.Frame(content_frame, bg="#ecf0f1")
trans_frame.grid(row=4, column=1, sticky="w", pady=8, padx=10)
trans_var = tk.IntVar(value=1)  # Default to Manual

for text, value in [("Automatic", 0), ("Manual", 1)]:
    tk.Radiobutton(trans_frame, text=text, variable=trans_var, value=value,
                  font=("Arial", 9), bg="#ecf0f1").pack(side="left", padx=5)

# Number of Owners
tk.Label(content_frame, text="Number of Owners:", font=label_font, 
         bg="#ecf0f1").grid(row=5, column=0, sticky="w", pady=8)
owner_entry = tk.Entry(content_frame, font=entry_font, width=25)
owner_entry.grid(row=5, column=1, pady=8, padx=10)
owner_entry.insert(0, "1")

# Car Age
tk.Label(content_frame, text="Car Age (years):", font=label_font, 
         bg="#ecf0f1").grid(row=6, column=0, sticky="w", pady=8)
age_entry = tk.Entry(content_frame, font=entry_font, width=25)
age_entry.grid(row=6, column=1, pady=8, padx=10)
age_entry.insert(0, "5")

# Buttons frame
button_frame = tk.Frame(content_frame, bg="#ecf0f1")
button_frame.grid(row=7, column=0, columnspan=2, pady=20)

# Predict button
predict_btn = tk.Button(button_frame, text="Predict Price", command=predict,
                       bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                       width=15, height=2, cursor="hand2", relief="raised", bd=3)
predict_btn.pack(side="left", padx=10)

# Clear button
clear_btn = tk.Button(button_frame, text="Clear", command=clear_fields,
                     bg="#95a5a6", fg="white", font=("Arial", 12, "bold"),
                     width=10, height=2, cursor="hand2", relief="raised", bd=3)
clear_btn.pack(side="left", padx=10)

# Result frame
result_frame = tk.Frame(content_frame, bg="white", relief="solid", bd=2)
result_frame.grid(row=8, column=0, columnspan=2, pady=20, sticky="ew")

result_label = tk.Label(result_frame, text="", font=("Arial", 12, "bold"),
                       bg="white", fg="#2ecc71", wraplength=450, justify="center",
                       pady=20)
result_label.pack()

# Info label
info_label = tk.Label(content_frame, 
                     text="Enter car details and click 'Predict Price'",
                     font=("Arial", 9, "italic"), bg="#ecf0f1", fg="#7f8c8d")
info_label.grid(row=9, column=0, columnspan=2, pady=10)

# Run the application
root.mainloop()
