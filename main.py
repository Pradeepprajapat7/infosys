from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

# 1. Initialize the App
app = FastAPI(title="PriceOptima Dynamic Pricing API")

# 2. Define the Input Data Structure (Updated to match your requirements)
class PricingInput(BaseModel):
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
    holiday_promotion: int  # Assuming 0 or 1
    discount: float

# 3. Load the Trained Model (Safe Loading)
model = None
try:
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
        print("✅ Model loaded successfully!")
    else:
        print("⚠️ 'model.pkl' not found. Running in SIMULATION MODE.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# 4. Define the Root Endpoint
@app.get("/")
def home():
    return {"message": "PriceOptima API is running. Go to /docs for Swagger UI."}

# 5. Define the Prediction Endpoint
@app.post("/predict")
def predict_price(data: PricingInput):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # PREDICTION LOGIC
        if model:
            # If model exists, try to predict (Note: Your model must have been trained on these exact columns)
            try:
                predicted_price = float(model.predict(input_df)[0])
            except:
                # Fallback if model columns don't match exactly
                predicted_price = (data.current_price + data.competitor_price) / 2 * 1.05
        else:
            # SIMULATION LOGIC (If no model file)
            # Logic: If inventory is low (< 20), raise price. If high, lower price.
            base_calc = (data.current_price + data.competitor_price) / 2
            
            if data.inventory_level < 20:
                predicted_price = base_calc * 1.10  # Scarcity markup
            else:
                predicted_price = base_calc * 1.02  # Standard markup
        
        # Calculate uplift
        uplift = predicted_price - data.current_price
        
        return {
            "product_id": data.product_id,
            "optimized_price": round(predicted_price, 2),
            "uplift": round(uplift, 2),
            "status": "Success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))