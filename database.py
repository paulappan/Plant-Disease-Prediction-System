import sqlite3

conn = sqlite3.connect("plant_disease.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(

plant_type INTEGER,

leaf_color INTEGER,

leaf_spot_size REAL,

humidity REAL,

temperature REAL,

rainfall REAL,

soil_ph REAL,

disease_present INTEGER,

prediction INTEGER

)
""")

conn.commit()
conn.close()