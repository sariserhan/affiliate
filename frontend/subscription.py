import streamlit as st
import logging

from backend.data.subscribe import Subscription

logging.basicConfig(level=logging.DEBUG)

def subscription():
    with st.container():
        email = st.text_input(label='Email to subscribe', key='subscribe', placeholder='Email to subscribe/unsubscribe', label_visibility='collapsed')      
        subscribe_button = st.button(label='Subscribe')
        unsubscribe_button = st.button(label='Unsubscribe')
        
        try:
            subscription = Subscription(email=email)
        except ValueError as e:
            return st.error("Invalid email address")
    
        if subscribe_button:            
            try:
                subscription.subscribe()
                st.write(f'{email} Subscribed')
            except Exception as e:
                logging.error(f'Error trying to subscribe {e}')
                st.error(f'Error trying to subscribe {e}')
            
        if unsubscribe_button:
            try:
                subscription.unsubscribe()
                st.write(f'{email} Unsubscribed!')
            except Exception as e:
                logging.error(f'Error trying to unsubscribe {e}')
                st.error(f'Error trying to unsubscribe {e}')
    return