from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# --- THIS IS THE CRITICAL LINE ---
app = FastAPI() 
# ---------------------------------

# Load model and encoders
try:
    model = joblib.load('pricing_model.joblib')
    encoders = joblib.load('encoders.joblib')
    print("SUCCESS: Model and Encoders loaded.")
except Exception as e:
    print(f"ERROR: Could not load files. {e}")

class ProductInput(BaseModel):
    date: str
    category: str
    region: str
    weather_condition: str
    seasonality: str
    store_id: str
    product_id: str
    current_price: float
    competitor_price: float
    inventory_level: int
    holiday_promotion: int
    discount: float

@app.get("/")
def home():
    return {"message": "API is working!"}

@app.post("/recommend_price")
def recommend_price(item: ProductInput):
    # (Simplified logic to test connection first)
    return {"message": "Endpoint reached", "received_price": item.current_price}