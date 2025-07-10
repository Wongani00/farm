# FARM System

**Forecasting Agricultural Revenue using Machine Learning**

FARM is a web app that predicts the prices of **maize**, **rice**, and **beans** in Malawi using machine learning. It helps farmers and businesses make informed decisions based on market trends Using **Dataset From:** https://data.humdata.org/dataset/wfp-food-prices-for-malawi?

---

## Features

- Price forecasting for beans, maize, and rice
- ML-powered predictions using Random Tree Regressor
- Data preprocessing, model selection, and evaluation pipeline

---

## Tech Stack

- **Backend**: Python + Flask  
- **Frontend**: HTML, CSS, JS, FontAwesome  
- **ML**: Scikit-learn (Random Tree Regressor)

---

Clone the repo and run the Flask app to access the forecasting dashboard.

```bash
git clone https://github.com/Wongani00/farm.git
cd farm
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
