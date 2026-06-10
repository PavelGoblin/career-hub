"""
Data Preparation Script
=======================
Downloads and generates datasets used across the tutorials.
Run: python scripts/prepare_datasets.py
"""

import os
import urllib.request
import zipfile
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "Data")
os.makedirs(DATA_DIR, exist_ok=True)


def download(url, filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, path)
        print(f"  -> saved to {path}")
    else:
        print(f"{filename} already exists, skipping.")
    return path


def generate_sales_data():
    """Generate synthetic sales dataset."""
    np.random.seed(42)
    n = 1000
    data = {
        "date": pd.date_range("2023-01-01", periods=n, freq="D"),
        "product": np.random.choice(["Widget", "Gadget", "Doohickey", "Thingamajig", "Whatsit"], n),
        "category": np.random.choice(["Electronics", "Clothing", "Food", "Books"], n),
        "region": np.random.choice(["North", "South", "East", "West"], n),
        "sales": np.random.gamma(shape=5, scale=100, size=n).astype(int),
        "quantity": np.random.randint(1, 50, n),
        "discount": np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
        "customer_rating": np.random.randint(1, 6, n),
    }
    df = pd.DataFrame(data)
    # Add some missing values
    df.loc[np.random.choice(n, 30), "sales"] = np.nan
    df.loc[np.random.choice(n, 20), "customer_rating"] = np.nan
    path = os.path.join(DATA_DIR, "sales_data.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


def generate_hr_data():
    """Generate synthetic HR / employee attrition dataset."""
    np.random.seed(123)
    n = 1500
    data = {
        "employee_id": range(1, n + 1),
        "age": np.random.randint(22, 65, n),
        "department": np.random.choice(["Sales", "R&D", "HR", "Marketing", "IT", "Finance"], n),
        "salary": np.random.randint(30000, 150000, n),
        "years_at_company": np.random.randint(0, 40, n),
        "promotion_last_2yr": np.random.choice([0, 1], n, p=[0.8, 0.2]),
        "satisfaction_score": np.random.uniform(1, 10, n).round(1),
        "avg_work_hours": np.random.randint(35, 60, n),
        "left": np.random.choice([0, 1], n, p=[0.85, 0.15]),
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "hr_data.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


def generate_customer_churn():
    """Generate synthetic customer churn dataset."""
    np.random.seed(456)
    n = 2000
    data = {
        "customer_id": [f"C{i:05d}" for i in range(1, n + 1)],
        "tenure_months": np.random.randint(1, 72, n),
        "monthly_charges": np.random.uniform(20, 120, n).round(2),
        "total_charges": np.random.uniform(100, 8000, n).round(2),
        "contract_type": np.random.choice(["Month-to-month", "One year", "Two year"], n, p=[0.5, 0.3, 0.2]),
        "internet_service": np.random.choice(["DSL", "Fiber optic", "No"], n, p=[0.3, 0.4, 0.3]),
        "payment_method": np.random.choice(["Credit card", "Bank transfer", "Electronic check", "Mailed check"], n),
        "churn": np.random.choice([0, 1], n, p=[0.75, 0.25]),
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "customer_churn.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


def generate_house_pricing():
    """Generate synthetic housing dataset."""
    np.random.seed(789)
    n = 1000
    size_sqft = np.random.normal(1800, 600, n).clip(500, 5000)
    bedrooms = np.random.randint(1, 6, n)
    bathrooms = np.random.randint(1, 4, n)
    age = np.random.randint(0, 80, n)
    location = np.random.choice(["Urban", "Suburban", "Rural"], n, p=[0.3, 0.5, 0.2])
    
    # Simulate price based on features
    base_price = 50000
    price = (base_price + size_sqft * 80 + bedrooms * 15000 + bathrooms * 10000 
             - age * 500 + np.where(location == "Urban", 30000, np.where(location == "Suburban", 10000, -20000))
             + np.random.normal(0, 25000, n))
    
    data = {
        "size_sqft": size_sqft.round(1),
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age,
        "location": location,
        "has_garage": np.random.choice([0, 1], n, p=[0.3, 0.7]),
        "has_garden": np.random.choice([0, 1], n, p=[0.5, 0.5]),
        "price": price.round(2),
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "house_pricing.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


def generate_fraud_data():
    """Generate synthetic credit card fraud dataset."""
    np.random.seed(111)
    n = 5000
    fraud_rate = 0.05
    is_fraud = np.random.choice([0, 1], n, p=[1 - fraud_rate, fraud_rate])
    
    # Normal transactions
    amount = np.where(is_fraud == 0,
                      np.random.gamma(2, 50, n),
                      np.random.gamma(5, 200, n))
    
    data = {
        "transaction_id": range(1, n + 1),
        "amount": amount.round(2),
        "transaction_hour": np.random.randint(0, 24, n),
        "day_of_week": np.random.randint(0, 7, n),
        "distance_from_home": np.random.exponential(50, n).round(1),
        "foreign_transaction": np.random.choice([0, 1], n, p=[0.8, 0.2]),
        "previous_attempts_24h": np.random.poisson(0.5, n),
        "is_fraud": is_fraud,
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "fraud_data.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows, fraud_rate={fraud_rate})")
    return path


def generate_store_data():
    """Generate synthetic store / retail dataset for feature selection case study."""
    np.random.seed(222)
    n = 500
    data = {
        "store_id": range(1, n + 1),
        "store_size_sqft": np.random.randint(500, 5000, n),
        "num_employees": np.random.randint(5, 100, n),
        "avg_transaction_value": np.random.uniform(10, 200, n).round(2),
        "daily_customers": np.random.randint(50, 2000, n),
        "years_operated": np.random.uniform(0, 30, n).round(1),
        "has_online_presence": np.random.choice([0, 1], n),
        "competitors_nearby": np.random.randint(0, 10, n),
        "parking_spots": np.random.randint(0, 100, n),
        "marketing_spend": np.random.uniform(1000, 50000, n).round(2),
        "revenue": np.random.uniform(50000, 2000000, n).round(2),
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "store_data.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


def generate_imdb_style_data():
    """Generate synthetic movie ratings data (IMDB-like)."""
    np.random.seed(333)
    n_movies = 200
    n_reviews = 5000
    
    movies = {
        "movie_id": range(1, n_movies + 1),
        "title": [f"Movie_{i}" for i in range(1, n_movies + 1)],
        "genre": np.random.choice(["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance"], n_movies),
        "year": np.random.randint(1990, 2025, n_movies),
        "budget_millions": np.random.uniform(1, 300, n_movies).round(1),
    }
    movies_df = pd.DataFrame(movies)
    path = os.path.join(DATA_DIR, "movies.csv")
    movies_df.to_csv(path, index=False)
    
    reviews = {
        "review_id": range(1, n_reviews + 1),
        "movie_id": np.random.randint(1, n_movies + 1, n_reviews),
        "rating": np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], n_reviews, 
                                    p=[0.02, 0.03, 0.05, 0.08, 0.12, 0.15, 0.20, 0.18, 0.12, 0.05]),
        "review_date": pd.date_range("2020-01-01", periods=n_reviews, freq="h").strftime("%Y-%m-%d"),
    }
    reviews_df = pd.DataFrame(reviews)
    path2 = os.path.join(DATA_DIR, "reviews.csv")
    reviews_df.to_csv(path2, index=False)
    print(f"Generated {path} & {path2} ({n_movies} movies, {n_reviews} reviews)")
    return movies_df, reviews_df


def generate_healthcare_data():
    """Generate synthetic healthcare dataset."""
    np.random.seed(444)
    n = 1000
    data = {
        "patient_id": range(1, n + 1),
        "age": np.random.randint(18, 90, n),
        "gender": np.random.choice(["M", "F"], n),
        "blood_pressure_systolic": np.random.normal(120, 15, n).round(1).clip(80, 200),
        "blood_pressure_diastolic": np.random.normal(80, 10, n).round(1).clip(50, 130),
        "cholesterol": np.random.normal(200, 40, n).round(1).clip(100, 350),
        "bmi": np.random.normal(26, 5, n).round(1).clip(15, 45),
        "heart_rate": np.random.normal(72, 12, n).round(0).clip(40, 120).astype(int),
        "smoker": np.random.choice([0, 1], n, p=[0.75, 0.25]),
        "diabetic": np.random.choice([0, 1], n, p=[0.85, 0.15]),
        "readmission_risk": np.random.choice(["Low", "Medium", "High"], n, p=[0.5, 0.3, 0.2]),
    }
    df = pd.DataFrame(data)
    path = os.path.join(DATA_DIR, "healthcare_data.csv")
    df.to_csv(path, index=False)
    print(f"Generated {path} ({n} rows)")
    return path


if __name__ == "__main__":
    print("=" * 60)
    print("Data Preparation Script")
    print("=" * 60)
    
    generate_sales_data()
    generate_hr_data()
    generate_customer_churn()
    generate_house_pricing()
    generate_fraud_data()
    generate_store_data()
    generate_imdb_style_data()
    generate_healthcare_data()
    
    print("\n" + "=" * 60)
    print("All datasets generated successfully in 'Data/' directory!")
    print("=" * 60)
