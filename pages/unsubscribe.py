import streamlit as st

from st_pages import hide_pages

from frontend.subscription import unsubscribe

# --- CSS 
with open('./styles/main.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

hide_pages(["admin"])

email = st.text_input(label='email', placeholder="Email to unsubscribe!", label_visibility='hidden')
unsubscribe_button = st.button(label='Unsubscribe')

if unsubscribe_button:
    unsubscribe(email)
