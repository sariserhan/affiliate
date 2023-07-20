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

    button = st.button(label='Send')

    if button:
        email_obj = EmailService()
        emails_to_send = email_obj.get_subscription_list()
        
        item_dict = email_obj.get_item(selected_item)
        for email in emails_to_send:
            if not item_dict['email_sent']:
                try:
                    email_obj.send_email(recipient_email=email, item_dict=item_dict)
                    st.success(f'Email sent to {email}')
                    try:
                        item_obj.update_record(key=item_dict['key'], updates={'email_sent': True})
                        logging.info(f"{item_dict['name']} updated in DB")
                    except Exception as e:
                        logging.error(f"Error in updating {item_dict['name']} in DB {e}")
                except Exception as e:
                    st.error(f'Error sending email --> {e}')   