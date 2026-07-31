import streamlit as st
import numpy as np
import sqlite3
import pandas as pd
import pickle

# Set page config (must be called first)
st.set_page_config(page_title="Plant Disease Prediction System", layout="centered", page_icon="🌿")

# Load model
with open("plant_disease_model (4).pkl", "rb") as f:
    model = pickle.load(f)

# Database connection
conn = sqlite3.connect(
    "plant_disease.db",
    check_same_thread=False
)

st.markdown("""
<style>

/* Background */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1500937386664-56d1dfef3854");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Main container */
.main .block-container {
    background: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 25px;
    margin-top: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

/* Title */
h1 {
    color: #1B5E20;
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    text-shadow: 2px 2px 5px rgba(0,0,0,0.15);
}

/* Labels */
label {
    font-weight: 600 !important;
    color: #1B5E20 !important;
}

/* Input boxes */
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
    border: 2px solid #81C784 !important;
    background-color: #f8fff8 !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2E7D32, #66BB6A);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
    width: 100%;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 5px 15px rgba(46,125,50,0.4);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(27,94,32,0.95);
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

def show_predict_page():

    st.markdown("""
    <style>

    .project-title {
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        color: #1B5E20;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 5px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.2);
    }

    .project-subtitle {
        text-align: center;
        font-size: 18px;
        color: #444444;
        font-style: italic;
        font-weight: 500;
        margin-bottom: 15px;
    }

    .project-divider {
        width: 220px;
        height: 4px;
        background: linear-gradient(90deg, #2E7D32, #66BB6A);
        margin: 15px auto 30px auto;
        border-radius: 20px;
    }

    </style>

    <div class="project-title">
        🌿 PLANT DISEASE PREDICTION SYSTEM
    </div>

    <div class="project-subtitle">
        An Intelligent Machine Learning Solution for Crop Health Monitoring
    </div>

   
    """, unsafe_allow_html=True)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        plant_type INTEGER,
        leaf_color INTEGER,
        leaf_spot_size REAL,
        humidity REAL,
        temperature REAL,
        rainfall REAL,
        soil_ph REAL,
        prediction TEXT
    )
    """)
    conn.commit()

    col1, col2 = st.columns(2)

    with col1:

        plant_options = {
            "Tomato": 0,
            "Potato": 1,
            "Rice": 2,
            "Corn": 3
        }

        selected_plant = st.selectbox(
            "Plant Type",
            list(plant_options.keys())
        )

        plant_type = plant_options[selected_plant]

        leaf_color = st.selectbox(
            "Leaf Color",
            [0, 1, 2]
        )

        leaf_spot_size = st.number_input(
            "Leaf Spot Size"
        )

        humidity = st.number_input(
            "Humidity"
        )

    with col2:

        temperature = st.number_input(
            "Temperature"
        )

        rainfall = st.number_input(
            "Rainfall"
        )

        soil_ph = st.number_input(
            "Soil pH"
        )

    result = None

    if st.button("Predict Disease"):

        columns = [
            "Plant_Type",
            "Leaf_Color",
            "Leaf_Spot_Size",
            "Humidity",
            "Temperature",
            "Rainfall",
            "Soil_pH"
        ]

        data = pd.DataFrame([[
            plant_type,
            leaf_color,
            leaf_spot_size,
            humidity,
            temperature,
            rainfall,
            soil_ph
        ]], columns=columns)

        prediction = model.predict(data)[0]

        labels = {
            0: "Healthy",
            1: "Mild Infection",
            2: "Severe Infection"
        }

        result = labels[prediction]

        # Save prediction to database
        cursor.execute(
            """
            INSERT INTO predictions(
                plant_type,
                leaf_color,
                leaf_spot_size,
                humidity,
                temperature,
                rainfall,
                soil_ph,
                prediction
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                plant_type,
                leaf_color,
                leaf_spot_size,
                humidity,
                temperature,
                rainfall,
                soil_ph,
                result
            )
        )

        conn.commit()

        if result == "Healthy":
            st.markdown(
                f"""
                <div style="
                    background-color:#d4edda;
                    color:#155724;
                    padding:15px;
                    border-radius:10px;
                    font-size:24px;
                    font-weight:bold;
                    text-align:center;">
                    🌿 Prediction: {result}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif result == "Mild Infection":
            st.markdown(
                f"""
                <div style="
                    background-color:#fff3cd;
                    color:#856404;
                    padding:15px;
                    border-radius:10px;
                    font-size:24px;
                    font-weight:bold;
                    text-align:center;">
                    ⚠️ Prediction: {result}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif result == "Severe Infection":
            st.markdown(
                f"""
                <div style="
                    background-color:#f8d7da;
                    color:#721c24;
                    padding:15px;
                    border-radius:10px;
                    font-size:24px;
                    font-weight:bold;
                    text-align:center;">
                    🚨 Prediction: {result}
                </div>
                """,
                unsafe_allow_html=True
            )

 

    # Show History Shortcut
    if st.button("📜 View Prediction History"):
        st.switch_page(history_page)

def show_history_page():
    st.title("📜 Prediction History")
    cursor = conn.cursor()
    
    # Ensure database table exists before querying
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        plant_type INTEGER,
        leaf_color INTEGER,
        leaf_spot_size REAL,
        humidity REAL,
        temperature REAL,
        rainfall REAL,
        soil_ph REAL,
        prediction TEXT
    )
    """)
    conn.commit()

    history = pd.read_sql_query(
        "SELECT * FROM predictions",
        conn
    )
    st.dataframe(history, use_container_width=True)

    if st.button("⬅️ Back to Prediction"):
        st.switch_page(predict_page)

# Define pages using modern st.Page API
predict_page = st.Page(show_predict_page, title="Predict Disease", icon="🌿", default=True)
history_page = st.Page(show_history_page, title="Prediction History", icon="📜")

# Render navigation
pg = st.navigation([predict_page, history_page])
pg.run()
