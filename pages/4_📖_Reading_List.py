import streamlit as st
import sqlite3

st.set_page_config(page_title="📖 Reading List", layout="wide")

if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("Please log in to use the reading list.")
    st.stop()

conn = sqlite3.connect("users.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS reading_list (
    username TEXT,
    book TEXT
)
""")
conn.commit()

st.title("📖 Your Reading List")

# Add new book
new_book = st.text_input("Add a book to your reading list")
if st.button("➕ Add"):
    conn.execute("INSERT INTO reading_list (username, book) VALUES (?, ?)", (st.session_state["user"], new_book))
    conn.commit()
    st.success("Book added.")

# Show reading list
cursor = conn.execute("SELECT book FROM reading_list WHERE username=?", (st.session_state["user"],))
books = cursor.fetchall()

st.subheader("📚 Books in Your List")
for b in books:
    st.write(f"📘 {b[0]}")
