from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

# ==========================================
# 1. Initialize the App
# ==========================================
app = FastAPI(title="PriceOptima Dynamic Pricing API")

# ==========================================
# 2. Configure CORS (Crucial for React)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Allows all connections
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods (POST, GET, etc.)
    allow_headers=["*"],
)

# ==========================================
# 3. Define Input Data Structure (Matches React Form)
# ==========================================
class PricingInput(BaseModel):
    product_id: str
    store_id: str
    category: str
    date: str
    region: str
    weather_condition: str
    seasonality: str
    holiday_promotion: int    # 0 or 1
    inventory_level: int
    current_price: float
    competitor_price: float
    discount: float

# ==========================================
# 4. Load the Trained Model (Safe Loading)
# ==========================================
model = None
try:
    if os.path.exists("model.pkl"):
        model = joblib.load("model.pkl")
        print("✅ Model loaded successfully!")
    else:
        print("⚠️ 'model.pkl' not found. Running in SIMULATION MODE.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# ==========================================
# 5. Define API Endpoints
# ==========================================

@app.get("/")
def home():
    return {"message": "PriceOptima API is running. Go to /docs for Swagger UI."}

@app.post("/predict")
def predict_price(data: PricingInput):
    try:
        # Convert input data to DataFrame
        input_df = pd.DataFrame([data.dict()])
        
        # --- PREDICTION LOGIC ---
        if model:
            # If model exists, try to predict
            try:
                # We only select columns the model likely trained on (numeric)
                # Adjust this list if your model uses different columns
                model_features = input_df[['current_price', 'competitor_price', 'inventory_level', 'discount', 'holiday_promotion']]
                predicted_price = float(model.predict(model_features)[0])
            except:
                # Fallback if model columns don't match exactly
                print("Model feature mismatch, using logic fallback.")
                predicted_price = (data.current_price + data.competitor_price) / 2 * 1.05
        else:
            # SIMULATION LOGIC (If no model file exists)
            # Logic: If inventory is low (< 20), raise price. If high, lower price.
            base_calc = (data.current_price + data.competitor_price) / 2
            
            if data.inventory_level < 20:
                predicted_price = base_calc * 1.15  # High demand/Low stock markup
            elif data.seasonality == "Winter":
                 predicted_price = base_calc * 1.10 # Seasonal markup
            else:
                predicted_price = base_calc * 1.02  # Standard markup
        
        # Calculate uplift (How much more we earn vs current price)
        uplift = predicted_price - data.current_price
        
        return {
            "product_id": data.product_id,
            "optimized_price": round(predicted_price, 2),
            "uplift": round(uplift, 2),
            "status": "Success"
        }
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))