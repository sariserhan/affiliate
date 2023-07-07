import streamlit as st

def subscription():
    with st.container():
        email = st.text_input(label='Email to subscribe', key='subscribe', placeholder='Email to subscribe/unsubscribe', label_visibility='collapsed')        
        subscribe_button = st.button(label='Subscribe')
        unsubscribe_button = st.button(label='Unsubscribe')
    
        if subscribe_button:
            st.write(f'{email} Subscribed')
            
        if unsubscribe_button:
            st.write(f'{email} Unsubscribed!')