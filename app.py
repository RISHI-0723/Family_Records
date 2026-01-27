from db import get_connection, init_db

# 🔑 Ensure DB + table exist at app startup
init_db()

import streamlit as st
if "step" not in st.session_state:
    st.session_state.step = 1

if "name" not in st.session_state:
    st.session_state.name = ""

if "age" not in st.session_state:
    st.session_state.age = None

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "aadhaar_last4" not in st.session_state:
    st.session_state.aadhaar_last4 = ""


st.title("Family Records – Multi-Form Wizard")

# ---------------------------
# STEP 1: Basic Details
# ---------------------------
if st.session_state.step == 1:
    st.header("Step 1: Basic Details")

    st.session_state.name = st.text_input(
        "Full Name",
        value=st.session_state.name
    )

    st.session_state.age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=st.session_state.age if st.session_state.age else 0
    )

    if st.button("Next"):
        st.session_state.step = 2
        st.rerun()

# ---------------------------
# STEP 2: Contact Details
# ---------------------------
elif st.session_state.step == 2:
    st.header("Step 2: Contact Details")

    st.session_state.phone = st.text_input(
        "Phone Number",
        value=st.session_state.phone
    )

    st.session_state.email = st.text_input(
        "Email Address",
        value=st.session_state.email
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.step = 3
            st.rerun()
# ---------------------------
# STEP 3: Aadhaar Details
# ---------------------------
elif st.session_state.step == 3:
    st.header("Step 3: Aadhaar Details")

    st.session_state.aadhaar_last4 = st.text_input(
        "Aadhaar Last 4 Digits",
        value=st.session_state.aadhaar_last4,
        max_chars=4
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Next"):
            st.session_state.step = 4
            st.rerun()
# ---------------------------
# STEP 4: Review & Submit
# ---------------------------
elif st.session_state.step == 4:
    st.header("Step 4: Review & Submit")

    st.write("Please review the details before submitting:")

    st.markdown(f"""
    **Name:** {st.session_state.name}  
    **Age:** {st.session_state.age}  
    **Phone:** {st.session_state.phone}  
    **Email:** {st.session_state.email}  
    **Aadhaar Last 4:** {st.session_state.aadhaar_last4}
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Submit"):
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO family (name, age, phone, email, aadhaar_last4)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    st.session_state.name,
                    st.session_state.age,
                    st.session_state.phone,
                    st.session_state.email,
                    st.session_state.aadhaar_last4
                )
            )

            conn.commit()
            conn.close()

            st.success("Family record added successfully!")

            # Reset wizard
            st.session_state.step = 1
            st.session_state.name = ""
            st.session_state.age = None
            st.session_state.phone = ""
            st.session_state.email = ""
            st.session_state.aadhaar_last4 = ""

            st.rerun()

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
