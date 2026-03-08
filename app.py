import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = "family.db"

# -----------------------------
# DATABASE FUNCTIONS
# -----------------------------
def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS family (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        phone TEXT,
        email TEXT,
        aadhaar_last4 TEXT
    )
    """)

    conn.commit()
    conn.close()

# ensure DB exists
init_db()

# -----------------------------
# SESSION STATE
# -----------------------------
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

# -----------------------------
# APP TITLE
# -----------------------------
st.title("Family DB Manager")

# -----------------------------
# STEP 1
# -----------------------------
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

# -----------------------------
# STEP 2
# -----------------------------
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

# -----------------------------
# STEP 3
# -----------------------------
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

# -----------------------------
# STEP 4
# -----------------------------
elif st.session_state.step == 4:

    st.header("Review & Submit")

    st.write("Please review your data")

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

            st.success("Record saved!")

            st.session_state.step = 1
            st.session_state.name = ""
            st.session_state.age = None
            st.session_state.phone = ""
            st.session_state.email = ""
            st.session_state.aadhaar_last4 = ""

            st.rerun()

# -----------------------------
# DISPLAY DATABASE RECORDS
# -----------------------------
st.divider()
st.subheader("Family Records")

conn = get_connection()

df = pd.read_sql_query(
    "SELECT id, name, age, phone, email, aadhaar_last4 FROM family",
    conn
)

for index, row in df.iterrows():

    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

    col1.write(row["id"])
    col2.write(row["name"])
    col3.write(row["age"])
    col4.write(row["phone"])
    col5.write(row["email"])
    col6.write(row["aadhaar_last4"])

    if col7.button("Delete", key=row["id"]):

        cursor = conn.cursor()
        cursor.execute("DELETE FROM family WHERE id=?", (row["id"],))
        conn.commit()

        st.warning("Record deleted")
        st.rerun()

conn.close()