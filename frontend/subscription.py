import streamlit as st
import logging

from backend.data.subscribe import Subscription

logging.basicConfig(level=logging.DEBUG)

def subscription():
    with st.form('subscription_form'):
        email = st.text_input(label='Email to subscribe', key='subscribe', placeholder='Email to subscribe/unsubscribe', label_visibility='collapsed')      
        subscribe_button = st.form_submit_button(label='Subscribe')
        unsubscribe_button = st.form_submit_button(label='Unsubscribe')
    
        if subscribe_button:            
            try:
                subscription = Subscription(email=email)
                subscription.subscribe()
                return st.success(f'{email} is subscribed')
            except ValueError as e:
                return st.error("Invalid email address!")
            except Exception as e:
                logging.error(f'Error trying to subscribe {e}')
                return st.error(f'Error trying to subscribe {e}')
            
        if unsubscribe_button:
            try:                
                subscription = Subscription(email=email)
                if subscription.get_record(key=email):
                    subscription.unsubscribe()
                    return st.success(f'{email} is unsubscribed!')
                else:
                    return st.warning(f'{email} not previously subscribed!')
            except ValueError as e:
                return st.error("Invalid email address!")
            except Exception as e:
                logging.error(f'Error trying to unsubscribe {e}')
                return st.error(f'Error trying to unsubscribe {e}')