import streamlit as st

st.set_page_config(page_title="📚 Bookmate AI", layout="wide")

st.markdown("<h1 style='text-align: center;'>📚 Welcome to Bookmate AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Your personalized multilingual book companion</p>", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"]:
    st.success(f"Logged in as {st.session_state['user']}")
else:
    st.info("👈 Please log in using the sidebar navigation")
