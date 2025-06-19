import streamlit as st
import sqlite3
import hashlib

def create_user_table():
    conn = sqlite3.connect("users.db")
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

st.set_page_config(page_title="🔐 Login / Sign Up", layout="wide")

create_user_table()
st.title("🔐 Login / Sign Up")

choice = st.radio("Choose", ["Login", "Sign Up"])

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if choice == "Sign Up":
    if st.button("Create Account"):
        if username and password:
            add_user(username, hash_pw(password))
            st.success("Account created. Please log in.")
        else:
            st.warning("Fill in both fields.")
else:
    if st.button("Log In"):
        user = login_user(username, hash_pw(password))
        if user:
            st.session_state["user"] = username
            st.success("Logged in successfully")
            st.rerun()

        else:
            st.error("Invalid credentials.")
