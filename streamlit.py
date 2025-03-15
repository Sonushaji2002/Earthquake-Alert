import streamlit as st
import pickle

# Background Styling
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


# Function to handle safe float input
def safe_float_input(label, key):
    value = st.text_input(label, key=key)
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        st.error(f"Invalid input for {label}. Please enter a valid number.")
        return None


# Main app logic
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home()
    elif st.session_state.page == "prediction":
        prediction()


# Home Page
def home():
    st.title('Welcome to Earthquake Alert Prediction')
    st.write("This application helps predict the alert level of earthquakes based on input parameters.")

    if st.button("Go to Prediction Page"):
        reset_session_state()  # Reset values before moving to the prediction page
        st.session_state.page = "prediction"
        st.rerun()


# Reset session state to avoid autofill issues
def reset_session_state():
    st.session_state.magType = None
    st.session_state.type_event = None


# Prediction Page
def prediction():
    st.title('🌍 Earthquake Alert Prediction')
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

    features = [latitude, longitude, depth, mag, magType_map[magType], nst, gap, dmin, rms,
                type_map[type_event], horizontalError, depthError, magError, magNst]

    alert_levels = {0: "✅ Green", 1: "☢️ Orange", 2: "⛔ Red", 3: "⚠️ Yellow"}
    scaler = pickle.load(open('scalerRandomSearch.sav', 'rb'))
    model = pickle.load(open('XGRANDOMSEARCH_model.sav', 'rb'))

    if st.button('🔮 Predict Alert Level'):
        if None in features:
            st.error("Please fill in all required fields with valid numerical values.")
        else:
            scaled_features = scaler.transform([features])
            predicted_class = model.predict(scaled_features)
            st.success(f'🔔 **Predicted Alert Level:** {alert_levels[predicted_class[0]]}')

    if st.button("🔙 Go to Home Page"):
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    main()
