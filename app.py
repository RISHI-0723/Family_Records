import streamlit as st
import pandas as pd
from db import init_db, get_connection

st.title("Family DB Manager (Dummy Data)")

if st.button("Initialize Database"):
    init_db()
    st.success("Database created with dummy data")
    st.rerun()

conn = get_connection()

query = """
SELECT 
    name AS Name,
    age AS Age,
    phone AS Phone,
    email AS Email,
    aadhaar_last4 AS Aadhaar_Last_4
FROM family
"""

df = pd.read_sql_query(query, conn)
conn.close()

st.subheader("Family Records")
st.table(df)
