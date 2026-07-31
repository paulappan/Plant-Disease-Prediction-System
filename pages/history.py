import streamlit as st
import sqlite3
import pandas as pd

st.title("📜 Prediction History")

# Connect to database
conn = sqlite3.connect("plant_disease.db")

# Read data from predictions table
history = pd.read_sql_query(
    """
    SELECT
        plant_type,
        leaf_color,
        leaf_spot_size,
        humidity,
        temperature,
        rainfall,
        soil_ph,
        prediction
    FROM predictions
    """,
    conn
)

# Reset index
history = history.reset_index(drop=True)

# Display dataframe without index
st.dataframe(
    history.style.hide(axis="index"),
    use_container_width=True
)

conn.close()