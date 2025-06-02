#Earthquake Alert Prediction Web App

This is a web application built with **Streamlit** that predicts the alert level of an earthquake (**Green, Orange, Red, or Yellow**) based on user-provided seismic data.

---

##Features

- Easy-to-use web interface
- Earthquake-themed background
- Input validation for all fields
- Predicts alert level using a trained **XGBoost** model
- Uses a saved **scaler** and **model** (`scalerRandomSearch.sav`, `XGRANDOMSEARCH_model.sav`)

---

##Technologies Used

- Python
- Streamlit
- XGBoost
- Scikit-learn
- Pickle

---

##How to Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/earthquake-alert-prediction.git
   cd earthquake-alert-prediction
Install the dependencies:

bash
Copy
Edit
pip install -r requirements.txt
requirements.txt should contain:

nginx
Copy
Edit
streamlit
xgboost
scikit-learn
Start the app:

bash
Copy
Edit
streamlit run streamlit.py
Inputs Required
Magnitude

Depth

Latitude & Longitude

Event Type (earthquake, volcanic eruption, etc.)

Magnitude Type (Mw, Ml, etc.)

Other seismic features (gap, RMS, etc.)

Output
One of the four alert levels:

✅ Green

☢️ Orange

⛔ Red

⚠️ Yellow

📄 License
This project is open-source and free to use.

