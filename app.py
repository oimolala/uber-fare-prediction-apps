import streamlit as st
import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import os
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Page configuration
st.set_page_config(
    page_title="Uber Fare Prediction",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Grab/Gojek Aesthetic
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #f8f9fa;
    }

    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #00b14f 0%, #007d38 100%); /* Grab Green */
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }

    /* Card Styling */
    .st-emotion-cache-12w0qpk { /* Column/Card wrapper */
        background-color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Prediction Receipt Styling */
    .receipt-container {
        background-color: white;
        border: 1px dashed #ccc;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .fare-amount {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a1a;
        margin: 0.5rem 0;
    }
    .currency {
        font-size: 1.5rem;
        vertical-align: super;
    }

    /* Sidebar Tweaks - Fixed Visibility */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #eee;
    }
    
    /* Ensure sidebar text is visible */
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
    section[data-testid="stSidebar"] label {
        color: #1a1a1a !important;
    }
    
    /* Fix Metric visibility in sidebar */
    section[data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #00b14f !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: #666 !important;
    }

    .stButton>button {
        background-color: #00b14f !important;
        color: white !important;
        border: none !important;
        width: 100%;
        border-radius: 8px !important;
        font-weight: 700 !important;
        height: 3.5rem !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        background-color: #008f40 !important;
        box-shadow: 0 4px 12px rgba(0,177,79,0.3);
    }

    .car-size-info {
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 5px;
        margin-top: 0.5rem;
        text-align: center;
    }

    /* Search Result List Styling */
    .search-result {
        padding: 8px;
        border-bottom: 1px solid #eee;
        cursor: pointer;
    }
    .search-result:hover {
        background-color: #f0fdf4;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'p_lat' not in st.session_state:
    st.session_state.p_lat = 40.7614
if 'p_lon' not in st.session_state:
    st.session_state.p_lon = -73.9776
if 'd_lat' not in st.session_state:
    st.session_state.d_lat = 40.7489
if 'd_lon' not in st.session_state:
    st.session_state.d_lon = -73.9680
if 'p_search_query' not in st.session_state:
    st.session_state.p_search_query = ""
if 'd_search_query' not in st.session_state:
    st.session_state.d_search_query = ""
if 'p_selected_address' not in st.session_state:
    st.session_state.p_selected_address = ""
if 'd_selected_address' not in st.session_state:
    st.session_state.d_selected_address = ""

# Header
st.markdown("""
    <div class="header-container">
        <h1 style='margin:0;'>Uber Taxi App 🚕</h1>
        <p style='opacity:0.9; margin:0;'>Fast, reliable ride-hailing fare estimation</p>
    </div>
""", unsafe_allow_html=True)

# Geolocation Helper
@st.cache_data
def search_locations(query):
    """Fetch multiple location results from Nominatim for recommendations"""
    if not query or len(query) < 3:
        return []
    try:
        geolocator = Nominatim(user_agent="uber_fare_nawasena_app_v2")
        locations = geolocator.geocode(query, exactly_one=False, limit=5)
        if locations:
            return [{"address": loc.address, "lat": loc.latitude, "lon": loc.longitude} for loc in locations]
        return []
    except Exception:
        return []

# Routing Helper (OSRM API) - Improved for accuracy
@st.cache_data
def get_detailed_route(p_lat, p_lon, d_lat, d_lon):
    """Fetch real-road routing, distance, and duration from OSRM"""
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{p_lon},{p_lat};{d_lon},{d_lat}?overview=full&geometries=geojson"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['code'] == 'Ok':
            route_data = data['routes'][0]
            distance_km = route_data['distance'] / 1000
            duration_mins = route_data['duration'] / 60
            geometry = [[coord[1], coord[0]] for coord in route_data['geometry']['coordinates']]
            return geometry, distance_km, duration_mins
        return None, None, None
    except Exception:
        return None, None, None

# Math Helpers
def manhattan_distance_km(pick_lat, pick_lon, drop_lat, drop_lon):
    avg_lat = np.radians((pick_lat + drop_lat) / 2.0)
    lat_dist = 111.132
    lon_dist = 111.321 * np.cos(avg_lat)
    delta_lat = np.abs(drop_lat - pick_lat)
    delta_lon = np.abs(drop_lon - pick_lon)
    manhattan_km = (delta_lat * lat_dist) + (delta_lon * lon_dist)
    return round(manhattan_km * 1000, 2)

def preprocess_input(pickup_datetime, p_lat, p_lon, d_lat, d_lon, passenger_count, is_airport_trip):
    manhattan_dist = manhattan_distance_km(p_lat, p_lon, d_lat, d_lon)
    data = {
        'year': [pickup_datetime.year],
        'month': [pickup_datetime.month],
        'day': [pickup_datetime.day],
        'hour': [pickup_datetime.hour],
        'day_of_week': [pickup_datetime.weekday()],
        'passenger_count': [passenger_count],
        'is_airport_trip': [is_airport_trip],
        'manhattan_distance_m': [manhattan_dist]
    }
    df = pd.DataFrame(data)
    feature_order = ['year', 'month', 'day', 'hour', 'day_of_week', 'passenger_count', 'is_airport_trip', 'manhattan_distance_m']
    
    for col in ['year', 'month', 'day', 'hour', 'day_of_week']:
        df[col] = df[col].astype('int32')
    df['passenger_count'] = df['passenger_count'].astype('int64')
    df['is_airport_trip'] = df['is_airport_trip'].astype('int64')
    df['manhattan_distance_m'] = df['manhattan_distance_m'].astype('float64')
    
    return df[feature_order], manhattan_dist

# Sidebar
st.sidebar.markdown("### 🛠️ Developer Settings")
model_choice = st.sidebar.selectbox("Select Model Engine", ["XGBoost Regressor", "LightGBM Regressor"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Model Stats")
if model_choice == "XGBoost Regressor":
    st.sidebar.metric("R² Score", "0.854")
    st.sidebar.metric("RMSE", "$3.35")
else:
    st.sidebar.metric("R² Score", "0.871")
    st.sidebar.metric("RMSE", "$3.14")

# Main Interface Tabs
tab_book, tab_info = st.tabs(["📍 Book a Ride", "📖 How it Works"])

with tab_book:
    # Booking Layout
    col_input, col_map = st.columns([1, 1.2])

    with col_input:
        st.markdown("#### Where to?")
        
        # Pickup Search Logic
        p_query = st.text_input(
            "Pickup Point", 
            value=st.session_state.p_search_query, 
            placeholder="Your current location? (e.g. Manhattan Square)", 
            key="p_search_input", 
            label_visibility="collapsed"
        )
        
        # Logic to show suggestions only when user is typing something new
        if p_query and p_query != st.session_state.p_selected_address:
            results = search_locations(p_query)
            if results:
                st.markdown("**Suggestions:**")
                for i, res in enumerate(results):
                    if st.button(f"📍 {res['address'][:60]}...", key=f"p_res_{i}"):
                        st.session_state.p_lat, st.session_state.p_lon = res['lat'], res['lon']
                        st.session_state.p_selected_address = res['address']
                        st.session_state.p_search_query = res['address'] # Fill text input with selection
                        st.rerun()
            
        # Dropoff Search Logic
        d_query = st.text_input(
            "Destination", 
            value=st.session_state.d_search_query, 
            placeholder="Where are you going? (e.g. Times Square, New York)", 
            key="d_search_input", 
            label_visibility="collapsed"
        )
        
        if d_query and d_query != st.session_state.d_selected_address:
            results = search_locations(d_query)
            if results:
                st.markdown("**Suggestions:**")
                for i, res in enumerate(results):
                    if st.button(f"📍 {res['address'][:60]}...", key=f"d_res_{i}"):
                        st.session_state.d_lat, st.session_state.d_lon = res['lat'], res['lon']
                        st.session_state.d_selected_address = res['address']
                        st.session_state.d_search_query = res['address'] # Fill text input with selection
                        st.rerun()

        st.markdown("---")
        
        # Details Selection
        det_col1, det_col2 = st.columns(2)
        with det_col1:
            ny_time = datetime.utcnow() - timedelta(hours=5)
            p_date = st.date_input("Date", ny_time.date())
            p_time = st.time_input("Time", ny_time.time())
        
        with det_col2:
            passengers = st.slider("Passengers", 1, 6, 1)
            is_air = st.radio("Airport?", ["No", "Yes"], horizontal=True)
            is_airport_trip = 1 if is_air == "Yes" else 0

        # Car Size Visual Indicator
        if passengers <= 4:
            st.markdown('<div class="car-size-info" style="background-color: #e6f7ee; color: #333;">🚗 GrabCar (Standard)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="car-size-info" style="background-color: #fff4e6; color: #333;">🚙 GrabCar Plus (Large)</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        btn_predict = st.button("Calculate Fare")

    with col_map:
        st.markdown("#### Route Overview")
        # Center map
        m = folium.Map(location=[(st.session_state.p_lat + st.session_state.d_lat)/2, 
                                 (st.session_state.p_lon + st.session_state.d_lon)/2], 
                       zoom_start=13, tiles="cartodbpositron")
        
        folium.Marker([st.session_state.p_lat, st.session_state.p_lon], 
                      popup=st.session_state.p_selected_address if st.session_state.p_selected_address else "Pickup",
                      icon=folium.Icon(color='green', icon='circle', prefix='fa')).add_to(m)
        folium.Marker([st.session_state.d_lat, st.session_state.d_lon], 
                      popup=st.session_state.d_selected_address if st.session_state.d_selected_address else "Destination",
                      icon=folium.Icon(color='red', icon='map-marker', prefix='fa')).add_to(m)
        
        # Actual Path Routing
        route_geometry, road_dist, road_duration = get_detailed_route(
            st.session_state.p_lat, st.session_state.p_lon, 
            st.session_state.d_lat, st.session_state.d_lon
        )
        
        if route_geometry:
            folium.PolyLine(route_geometry, color='#00b14f', weight=6, opacity=0.85).add_to(m)
        else:
            folium.PolyLine([[st.session_state.p_lat, st.session_state.p_lon], 
                             [st.session_state.d_lat, st.session_state.d_lon]], 
                            color='#00b14f', weight=4, opacity=0.5, dash_array='10').add_to(m)

        map_data = st_folium(m, width=700, height=450, key="route_map")
        if map_data.get("last_clicked"):
            # Update destination on map click
            st.session_state.d_lat = map_data["last_clicked"]["lat"]
            st.session_state.d_lon = map_data["last_clicked"]["lng"]
            st.session_state.d_selected_address = f"Pinned: {st.session_state.d_lat:.4f}, {st.session_state.d_lon:.4f}"
            st.session_state.d_search_query = st.session_state.d_selected_address
            st.rerun()

    # Prediction Result Section
    if btn_predict:
        try:
            pickup_dt = datetime.combine(p_date, p_time)
            input_df, m_dist = preprocess_input(pickup_dt, st.session_state.p_lat, st.session_state.p_lon, 
                                              st.session_state.d_lat, st.session_state.d_lon, 
                                              passengers, is_airport_trip)
            
            fname = 'xgb_model.pkl' if "XGBoost" in model_choice else 'lgb_model.pkl'
            fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
            
            if os.path.exists(fpath):
                with open(fpath, 'rb') as f:
                    model = pickle.load(f)
                prediction = model.predict(input_df)[0]
                
                st.markdown("### 🧾 Ride Summary")
                res_col1, res_col2 = st.columns([1.5, 1])
                
                with res_col1:
                    st.markdown(f"""
                        <div class="receipt-container">
                            <p style='color:#666; margin:0;'>Estimated Fare</p>
                            <div class="fare-amount"><span class="currency">$</span>{max(0, prediction):.2f}</div>
                            <p style='color:#00b14f; font-weight:600;'>✓ Best price guaranteed</p>
                        </div>
                    """, unsafe_allow_html=True)
                
                with res_col2:
                    final_dist = road_dist if road_dist else m_dist/1000
                    eta = road_duration if road_duration else (final_dist * 2.5)
                    
                    st.info(f"📏 **Distance:** {final_dist:.2f} km")
                    st.info(f"⏱️ **Est. Time:** {int(eta)} - {int(eta+5)} mins")
                    st.info(f"👥 **Capacity:** {passengers} Pax")
                    
                    price_km = prediction / final_dist if final_dist > 0 else 0
                    st.success(f"💸 **Rate:** ${price_km:.2f}/km")
            else:
                st.error(f"Missing model: {fname}")
        except Exception as e:
            st.error(f"Calculation Error: {e}")

with tab_info:
    st.markdown("""
    ### About GrabPredict
    This application leverages advanced **Gradient Boosting** algorithms to estimate ride fares with high precision.
    
    - **Recommendations:** Search suggestions provided by Nominatim OpenStreetMap API.
    - **Geocoding:** Powered by OpenStreetMap Nominatim.
    - **Routing:** Real-road pathfinding via Open Source Routing Machine (OSRM).
    - **Distance:** Map calculates actual road distance, while the ML model uses Manhattan distance metrics for feature consistency.
    - **Machine Learning:** Models are trained on over 200,000 historical trips to account for time of day, passenger count, and airport surges.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>GrabPredict Prototype | Data Science Portfolio | © 2026 Nawasena</p>", unsafe_allow_html=True)

