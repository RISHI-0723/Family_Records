# Family Records – Streamlit + SQLite

A simple **Streamlit-based family database manager** built using **SQLite**.
This project demonstrates clean database design, safe handling of sensitive-like
data (dummy only), and separation of UI and database logic.

## Tech Stack
- Python
- Streamlit
- SQLite

## Features
- Initialize database with dummy family data
- Display records in a clean tabular UI
- Proper schema design with primary keys
- No real personal data stored

## Project Structure
- `app.py` – Streamlit UI
- `db.py` – Database connection and initialization logic
- `schema.sql` – Table structure
- `sample_data.sql` – Dummy data
- `requirements.txt` – Dependencies

## How to Run Locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
