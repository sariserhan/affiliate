import logging
import streamlit as st

logging.basicConfig(level=logging.DEBUG)

def delete_item(item_obj):
    with st.form(key="delete-form", clear_on_submit=True):
        item_dict = {}

        for item in item_obj.fetch_records():
            if item['key'] not in item_dict:
                item_dict[item['name']] = item['key']
        
        selected_item = st.selectbox(label="Choose Item", options=[name for name in item_dict.keys()])
        key = item_dict[selected_item]
        st.write('---')
        
        button = st.form_submit_button(label='Delete')
        if button:
            item_key = item_obj.get_record(key)['key']            
            if key == item_key:
                if item_obj.delete_item(key=key):
                    st.success(f'Item is deleted {selected_item}')
                    logging.info(f'Item is deleted {selected_item}')
                else:
                    st.error(f'Error in deleting item {selected_item}')
                    logging.error(f'Error in deleting item {selected_item}')
                    