# 📈 PriceOptima: Dynamic Pricing Solution

## 📖 Project Objective
**PriceOptima** is a machine learning-based dynamic pricing solution designed to maximize revenue. By analyzing historical sales data, market demand, and competitor pricing, the model predicts the optimal selling price to maintain competitiveness while ensuring profitability.

## 📊 Dataset Details
The model was trained on a robust retail dataset containing the following attributes:
* **Total Data Points:** 20,280
* **Key Features:** Cost Price, Competitor Price, Demand Score, Inventory Level, Seasonality.
* **Target Variable:** Selling Price.

## 🛠️ Technologies Used

| Category | Technology |
| :--- | :--- |
| **Language** | Python 🐍 |
| **ML Libraries** | Scikit-learn (HistGradientBoosting), XGBoost, Pandas, NumPy |
| **Backend API** | FastAPI (Python) |
| **Frontend** | React.js |
| **Containerization** | Docker 🐳 |
| **Cloud Deployment** | Render |

## 🧠 Model Development & Results
We implemented and compared two advanced gradient boosting techniques to minimize error and maximize revenue.

### 1. Model Comparison
We compared **XGBoost Regression** against **Histogram Gradient Boosting** (LightGBM equivalent implementation in Scikit-learn).

| Model | RMSE (Root Mean Sq. Error) | MAE (Mean Absolute Error) |
| :--- | :--- | :--- |
| **XGBoost Regressor** | 89.25 | 69.48 |
| **HistGradientBoosting** | **87.83** 🏆 | **68.73** 🏆 |

### 2. Key Business Impact
* **Selected Model:** Histogram Gradient Boosting (LightGBM Equivalent) due to lower error rates.
* **Revenue Lift:** The optimized pricing strategy demonstrated a projected **11.08% Revenue Lift**.

### 2. Backend Setup (FastAPI)

# Navigate to the backend folder
cd backend

# (Optional) Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload

### 3. Frontend Setup (React Dashboard)

cd dashboard
npm install
npm start

### 💻 Dashboard Features
# The React interface provides a clean UI for business users:

    -> Input Form ----> Accepts Cost, Competitor Price, and Demand Score.

    -> Instant Prediction----> Sends JSON data to the /predict endpoint.

    -> Visualization----> Displays the Recommended Price and projected margin.



### 💻 Responce of backend
![Response](screenshot/backend.png)



### 💻 Dashboard Screenshot(Frontend)
![Dashboard Interface](screenshot/screenshot.png)


### 1. Clone the Repository
```bash
git clone [https://github.com/Pradeepprajapat7/infosys.git]





