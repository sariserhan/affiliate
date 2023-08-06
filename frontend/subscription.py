import logging

import streamlit as st

from backend.data.subscribe import Subscription
from backend.email.send_email import EmailService

logging.basicConfig(level=logging.DEBUG)


def subscription():
    result = None
    with st.form('subscription_form', clear_on_submit=True):
        col1, col2, col3, col4 = st.columns([1.6, 2.5, 0.6, 0.7])
        with col1:
            st.write('Subscribe to receive weekly email newsletter')
        with col2:
            email = st.text_input(label='Email to subscribe', key='subscribe',
                                  placeholder='Email to subscribe/unsubscribe', label_visibility='collapsed')
        with col3:
            if st.form_submit_button(label='Subscribe'):
                result, message = subscribe(email)
        with col4:
            if st.form_submit_button(label='Unsubscribe'):
                result, message = unsubscribe(email)

    if result == 'error':
        st.error(message)
    if result == 'warning':
        st.warning(message)
    if result == 'success':
        st.success(message)


def subscribe(email: str):
    try:
        email_service = EmailService()
        subscription = Subscription(email=email)
        subscription.subscribe()
        email_service.send_email(recipient_email='serhan.sari@yahoo.com',
                                 subscription_event=f"New subscription --> {email}")
        return 'success', f'{email} is subscribed'
    except ValueError as e:
        return 'error', "Invalid email address!"
    except Exception as e:
        logging.error(f'Error trying to subscribe {e}')
        return 'error', f'Error trying to subscribe {e}'


def unsubscribe(email: str):
    try:
        email_service = EmailService()
        subscription = Subscription(email=email)
        if email_obj := subscription.get_record(key=email):
            if email_obj['is_subscribed']:
                subscription.unsubscribe()
                email_service.send_email(
                    recipient_email='serhan.sari@yahoo.com', subscription_event=f"User Unsubscribed --> {email}")
                return 'success', f'{email} is unsubscribed'
            else:
                return 'warning', f'{email} is not subscribed!'
        else:
            return 'warning', f'{email} not previously subscribed!'
    except ValueError as e:
        return 'error', "Invalid email address!"
    except Exception as e:
        logging.error(f'Error trying to unsubscribe {e}')
        return 'error', f'Error trying to unsubscribe {e}'
