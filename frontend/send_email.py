import logging
import streamlit as st

from frontend.column_setup import get_image
from backend.email.send_email import EmailService

def send_email(item_obj, catalog_list):
    item_list = []
    image_list= []
    image_name = None

    def on_selectbox_change(selected_catalog):
        pass

    catalog_list.remove('Add New Catalog')
    selected_catalog = st.selectbox(label="Choose Category", options=catalog_list)
    if selected_catalog:
        for item in item_obj.fetch_records():
            if item['catalog'] == selected_catalog and not item['email_sent']:
                item_list.append(item['name'])
                image_list.append(item['image_name'])
                
    selected_item = st.selectbox(label="Choose Item to Send", 
                                    options=item_list, 
                                    on_change=on_selectbox_change, args=(selected_catalog, )
                                    )
    for image_name_in_list in image_list:
        if selected_item in image_name_in_list:
            image_name = image_name_in_list
            break
    if image_name:
        image = get_image(image_name=image_name, selected_catalog=selected_catalog)
        st.image(image=image, caption=image_name, use_column_width=True)
    else:
        st.warning("No Product to send in this category")
    st.write('---')

    col1, col2, col3, _ = st.columns([1.2,1,1.5,1.1])
    email_obj = EmailService()
    item_dict = email_obj.get_item(selected_item)
    
    success = False
    warning = False
    error, error_e = False, ''
    email_sending_to = ''
    
    with col1:
        button = st.button(label='Send to Subscribers')

        if button:            
            emails_to_send = email_obj.get_subscription_list()
                        
            for email in emails_to_send:
                if not item_dict['email_sent']:
                    try:
                        email_obj.send_email(recipient_email=email, item_dict=item_dict)
                        email_sending_to = email
                        success = True                        
                        try:
                            item_obj.update_record(key=item_dict['key'], updates={'email_sent': True})
                            logging.info(f"{item_dict['name']} updated in DB")
                        except Exception as e:
                            logging.error(f"Error in updating {item_dict['name']} in DB {e}")
                    except Exception as e:
                        logging.error(f'Error sending email --> {e}')                           
                        error, error_e = True, e

    with col3:
        test_email_to_send = st.text_input(label='Email', key='email', placeholder='Email', label_visibility='collapsed')
                        
    with col2:
        button = st.button(label='Send Test Email')

        if button:
            if test_email_to_send:
                try:
                    email_obj.send_email(recipient_email=test_email_to_send, item_dict=item_dict)
                    success = True
                    email_sending_to = test_email_to_send
                except Exception as e:
                    logging.error(f"Error in updating {item_dict['name']} in DB {e}")
            else:                
                warning = True
                
                
    if success:
        st.success(f'Email sent to {email_sending_to}')
    if warning:
        st.warning('Please enter email to send!')
    if error:
        st.error(f'Error sending email --> {error_e}')