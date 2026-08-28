"""
generate_data.py
Generates a realistic synthetic Amazon-style e-commerce sales dataset
(100,000+ records) used to power the Sales Analytics Dashboard.

Run:
    python scripts/generate_data.py
Output:
    data/amazon_sales_data.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

N_ROWS = 100_000

# ----------------------------------------------------------------------
# Reference / lookup data
# ----------------------------------------------------------------------
categories = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Smartwatch", "Bluetooth Speaker",
                    "Power Bank", "Tablet", "Camera", "Gaming Console", "Router"],
    "Fashion": ["Men's T-Shirt", "Women's Kurti", "Running Shoes", "Handbag", "Sunglasses",
                "Formal Shirt", "Jeans", "Wrist Watch", "Backpack", "Jacket"],
    "Home & Kitchen": ["Mixer Grinder", "Air Fryer", "Non-Stick Cookware", "Bedsheet Set",
                       "Water Bottle", "LED Bulb", "Vacuum Cleaner", "Pressure Cooker",
                       "Curtains", "Storage Boxes"],
    "Books": ["Fiction Novel", "Self-Help Book", "Children's Book", "Biography", "Cookbook"],
    "Beauty & Personal Care": ["Face Wash", "Shampoo", "Perfume", "Trimmer", "Skincare Kit",
                              "Hair Dryer", "Makeup Kit"],
    "Sports & Fitness": ["Yoga Mat", "Dumbbells", "Cricket Bat", "Football", "Resistance Bands",
                         "Cycling Helmet", "Treadmill"],
    "Toys & Baby Products": ["Building Blocks", "Remote Control Car", "Baby Stroller",
                             "Soft Toy", "Diaper Pack"],
    "Grocery": ["Basmati Rice", "Cooking Oil", "Green Tea", "Dry Fruits Pack", "Spices Combo"],
}

category_price_range = {
    "Electronics": (799, 65000),
    "Fashion": (299, 4500),
    "Home & Kitchen": (349, 12000),
    "Books": (149, 999),
    "Beauty & Personal Care": (99, 2500),
    "Sports & Fitness": (299, 15000),
    "Toys & Baby Products": (199, 5000),
    "Grocery": (99, 1500),
}

states_cities = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"],
    "Delhi": ["New Delhi"],
    "Karnataka": ["Bengaluru", "Mysuru"],
    "Tamil Nadu": ["Chennai", "Coimbatore"],
    "Telangana": ["Hyderabad"],
    "West Bengal": ["Kolkata", "Howrah"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
    "Gujarat": ["Ahmedabad", "Surat"],
    "Rajasthan": ["Jaipur", "Udaipur"],
    "Punjab": ["Ludhiana", "Amritsar"],
    "Kerala": ["Kochi", "Thiruvananthapuram"],
    "Haryana": ["Gurugram", "Faridabad"],
}

payment_modes = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Cash on Delivery", "Amazon Pay"]
payment_weights = [0.20, 0.15, 0.30, 0.10, 0.15, 0.10]

ship_modes = ["Standard", "Expedited", "Same-Day", "Prime One-Day"]
ship_weights = [0.45, 0.30, 0.15, 0.10]

sales_channels = ["Website", "Mobile App", "Amazon App - Prime"]
channel_weights = [0.35, 0.40, 0.25]

customer_segments = ["New", "Returning", "Prime Member"]
segment_weights = [0.30, 0.45, 0.25]

first_names = ["Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan",
               "Ananya", "Diya", "Saanvi", "Aadhya", "Kiara", "Myra", "Ishita", "Riya",
               "Rohan", "Kabir", "Advait", "Neha", "Priya", "Simran", "Karan", "Ritu"]
last_names = ["Sharma", "Verma", "Gupta", "Patel", "Reddy", "Iyer", "Nair", "Singh",
              "Kumar", "Mehta", "Joshi", "Das", "Chopra", "Malhotra", "Rao", "Bose"]

# ----------------------------------------------------------------------
# Build rows
# ----------------------------------------------------------------------
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
category_list = list(categories.keys())
category_weights = [0.22, 0.18, 0.15, 0.08, 0.12, 0.10, 0.08, 0.07]

for i in range(N_ROWS):
    category = np.random.choice(category_list, p=category_weights)
    product = random.choice(categories[category])
    low, high = category_price_range[category]
    unit_price = round(np.random.uniform(low, high), 2)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.35, 0.2, 0.1, 0.15, 0.08, 0.06, 0.04, 0.02])

    discount_pct = np.random.choice([0, 5, 10, 15, 20, 25, 30, 40], p=[0.25, 0.15, 0.15, 0.15, 0.12, 0.10, 0.05, 0.03])
    gross_sales = round(unit_price * quantity, 2)
    discount_amt = round(gross_sales * discount_pct / 100, 2)
    net_sales = round(gross_sales - discount_amt, 2)

    # cost ~ 55-75% of unit price -> profit margin varies by category
    cost_ratio = np.random.uniform(0.55, 0.78)
    cost = round(unit_price * quantity * cost_ratio, 2)
    profit = round(net_sales - cost, 2)

    order_date = start_date + timedelta(days=random.randint(0, date_range_days))
    state = random.choice(list(states_cities.keys()))
    city = random.choice(states_cities[state])

    is_returned = np.random.choice([0, 1], p=[0.94, 0.06])
    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.03, 0.05, 0.12, 0.35, 0.45]) if is_returned == 0 else np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])

    customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"

    rows.append({
        "Order_ID": f"AMZ-{100000 + i}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": f"CUST-{np.random.randint(10000, 45000)}",
        "Customer_Name": customer_name,
        "Customer_Segment": np.random.choice(customer_segments, p=segment_weights),
        "Category": category,
        "Product_Name": product,
        "Quantity": int(quantity),
        "Unit_Price": unit_price,
        "Gross_Sales": gross_sales,
        "Discount_Percent": discount_pct,
        "Discount_Amount": discount_amt,
        "Net_Sales": net_sales,
        "Cost": cost,
        "Profit": profit,
        "State": state,
        "City": city,
        "Payment_Mode": np.random.choice(payment_modes, p=payment_weights),
        "Ship_Mode": np.random.choice(ship_modes, p=ship_weights),
        "Sales_Channel": np.random.choice(sales_channels, p=channel_weights),
        "Is_Returned": int(is_returned),
        "Customer_Rating": int(rating),
    })

df = pd.DataFrame(rows)
df.sort_values("Order_Date", inplace=True)
df.reset_index(drop=True, inplace=True)

out_path = "data/amazon_sales_data.csv"
df.to_csv(out_path, index=False)
print(f"Generated {len(df):,} rows -> {out_path}")
print(df.head())
