import streamlit as st

from st_pages import hide_pages

from frontend.subscription import unsubscribe

st.set_page_config(initial_sidebar_state="collapsed")

# --- CSS 
with open('./styles/main.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

hide_pages(["admin", "unsubscribe", "home"])

email = st.text_input(label='', placeholder="Email to unsubscribe!")
unsubscribe_button = st.button(label='Unsubscribe')

if unsubscribe_button:
    unsubscribe(email)
