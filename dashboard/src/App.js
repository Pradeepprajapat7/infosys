import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // 1. Setup the inputs to store your data
  const [formData, setFormData] = useState({
    product_id: 'PROD-101',
    store_id: 'STORE-001',
    category: 'Electronics',
    date: '2023-11-01',
    region: 'North',
    weather_condition: 'Sunny',
    seasonality: 'Winter',
    holiday_promotion: '0', 
    inventory_level: '',
    current_price: '',
    competitor_price: '',
    discount: '0.0'
  });

  const [result, setResult] = useState(null);

  // 2. This function tracks what you type
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  // 3. This function sends data to Python when you click the button
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Convert numbers (Strings to Integers/Floats)
      const payload = {
        ...formData,
        current_price: parseFloat(formData.current_price),
        competitor_price: parseFloat(formData.competitor_price),
        inventory_level: parseInt(formData.inventory_level),
        discount: parseFloat(formData.discount),
        holiday_promotion: parseInt(formData.holiday_promotion)
      };

      // Connect to your specific API address
      const response = await axios.post('http://127.0.0.1:8000/predict', payload);
      setResult(response.data); // Show the result
    } catch (err) {
      console.error(err);
      alert("Error: Is your Python backend running?");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1>Price Prediction Dashboard</h1>
        
        <form onSubmit={handleSubmit} className="form-grid">
          
          {/* --- Section 1: Product Info --- */}
          <h3>Product Info</h3>
          <div className="input-group">
             <label>Category</label>
             <select name="category" onChange={handleChange}><option>Electronics</option><option>Clothing</option></select>
          </div>

          {/* --- Section 2: Market Data --- */}
          <h3>Market Data</h3>
          <div className="input-group">
             <label>Region</label>
             <select name="region" onChange={handleChange}><option>North</option><option>South</option></select>
          </div>
          <div className="input-group">
             <label>Weather</label>
             <select name="weather_condition" onChange={handleChange}><option>Sunny</option><option>Rainy</option></select>
          </div>

          {/* --- Section 3: Pricing Numbers (The important ones) --- */}
          <h3>Price Variables</h3>
          <div className="input-group">
            <label>Current Price ($)</label>
            <input name="current_price" type="number" onChange={handleChange} required />
          </div>
          <div className="input-group">
            <label>Competitor Price ($)</label>
            <input name="competitor_price" type="number" onChange={handleChange} required />
          </div>
          <div className="input-group">
            <label>Inventory Level</label>
            <input name="inventory_level" type="number" onChange={handleChange} required />
          </div>
          <div className="input-group">
            <label>Discount (0.0 - 1.0)</label>
            <input name="discount" type="number" step="0.1" onChange={handleChange} />
          </div>

          <button type="submit" className="submit-btn">PREDICT PRICE</button>
        </form>

        {/* --- Section 4: Result Display --- */}
        {result && (
          <div className="result-box">
             <h2>Recommended Price: ${result.optimized_price}</h2>
             <p>Projected Uplift: ${result.uplift}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;