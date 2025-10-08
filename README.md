# 🛍️ Sales Prediction

A **machine learning-powered web app** that predicts outlet sales using Random Forest regression, featuring a clean web interface for real-time sales forecasting.

---

## 🌐 Live Demo

🔗 [**View Live App**](https://salesprediction-5wt5.onrender.com)

---

## 🎯 Features

- ✅ Random Forest regression model for sales prediction  
- ✅ Automated data preprocessing & feature engineering  
- ✅ Interactive Flask web interface with AJAX  
- ✅ REST API for programmatic predictions  
- ✅ Health check endpoint  
- ✅ Cloud deployment on Render  

---

## 🚀 Tech Stack

- **Backend**: Python, Flask  
- **ML**: scikit-learn, pandas, numpy  
- **Frontend**: HTML, CSS, JavaScript (AJAX)  
- **Deployment**: Render, Gunicorn  

---

## 📚 Usage

### 💻 Web Interface  
1. Open in browser:  
   `http://127.0.0.1:5000`  
2. Input outlet details  
3. Click **"Predict Sales"** → View result  

### ⚡ API Example  

python
import requests

response = requests.post('https://salesprediction-5wt5.onrender.com/predict', json={
    "Item_Weight": 12.5,
    "Item_Visibility": 0.05,
    "Item_Type": "Dairy",
    "Outlet_Size": "Medium",
    "Outlet_Location_Type": "Tier 2",
    "Outlet_Type": "Supermarket Type1"
})
print(response.json())
## ⚙️ Setup Instructions
git clone <repo-url>
cd SALES_DATA_FORECASTING
python -m venv .venv
source .venv/bin/activate  # Or .\.venv\Scripts\Activate.ps1 on Windows

pip install -r requirements.txt

python train_model.py

python app.py


