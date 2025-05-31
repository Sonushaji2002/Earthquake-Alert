import streamlit as st
import pickle

# Background
bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://wallpaperaccess.com/full/2910865.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(bg_img, unsafe_allow_html=True)

def safe_float_input(label, key):
    value = st.text_input(label, key=key)
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        st.error(f"Invalid input for {label}. Please enter a valid number.")
        return None

def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "prediction":
        prediction()
def home():
    st.title('EARTHQUAKE ALERT PREDICTION')
    st.write("This application helps predict the alert level of earthquakes based on input parameters.")

    if st.button("Go to Prediction Page"):
        reset_session_state()
        st.session_state.page = "prediction"
        st.rerun()
def reset_session_state():
    st.session_state.magType = None
    st.session_state.type_event = None
def prediction():
    st.title('EARTHQUAKE ALERT PREDICTI🌍N')

    st.write("Enter the required feature values to predict the earthquake alert level.")
    type_map = {'earthquake': 0, 'volcanic eruption': 2, 'nuclear explosion': 1}
    magType_map = {
        'Ml': 0, 'mb': 1, 'md': 2, 'mh': 3, 'ml': 4, 'ml(texnet)': 5, 'mlg': 6, 'mlr': 7,
        'ms': 8, 'mw': 9, 'mwb': 10, 'mwc': 11, 'mwp': 12, 'mwr': 13, 'mww': 14
    }

    magType = st.selectbox('Magnitude Type', magType_map.keys(), key="magType", index=0)
    type_event = st.selectbox('Event Type', type_map.keys(), key="type_event", index=0)

    latitude = safe_float_input('Latitude (°N/°S)', 'latitude')
    longitude = safe_float_input('Longitude (°E/°W)', 'longitude')
    depth = safe_float_input('Depth (km below surface)', 'depth')
    mag = safe_float_input('Earthquake Magnitude', 'mag')
    nst = safe_float_input('Number of Reporting Stations', 'nst')
    gap = safe_float_input('Azimuthal Gap (°)', 'gap')
    dmin = safe_float_input('Minimum Distance to Nearest Station (°)', 'dmin')
    rms = safe_float_input('Root Mean Square (RMS) Residual', 'rms')
    horizontalError = safe_float_input('Horizontal Location Uncertainty (km)', 'horizontalError')
    depthError = safe_float_input('Depth Measurement Uncertainty (km)', 'depthError')
    magError = safe_float_input('Magnitude Uncertainty (± value)', 'magError')
    magNst = safe_float_input('Stations Used for Magnitude Calculation', 'magNst')

    features = [
        latitude, longitude, depth, mag,
        magType_map.get(magType, None),
        nst, gap, dmin, rms,
        type_map.get(type_event, None),
        horizontalError, depthError, magError, magNst
    ]

    if None in features:
        st.error("⚠️ Please fill in all required fields with valid numerical values before predicting.")
        return

    try:
        scaler= pickle.load(open('scalerRandomSearch.sav', 'rb'))
        model=pickle.load(open('XGRANDOMSEARCH_model.sav', 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model or scaler file not found")
        return

    alert_levels={0: "✅ Green", 1: "☢️ Orange", 2: "⛔ Red", 3: "⚠️ Yellow"}

    if st.button('🔮 Predict Alert Level'):
        try:
            scaled_features = scaler.transform([features])
            predicted_class = model.predict(scaled_features)
            st.success(f'🔔 **Predicted Alert Level:** {alert_levels[predicted_class[0]]}')
        except Exception as e:
            st.error(f"⚠️ Error during prediction: {e}")
    if st.button("🔙 Go to Home Page"):
        st.session_state.page = "home"
        st.rerun()
if __name__ == "__main__":
    main()
