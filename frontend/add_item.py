import re
import time
import random
import logging
import streamlit as st

from backend.data.affiliate_partner import Affiliate_Partner

# --- ADD ITEM
def add_item(item_obj, catalog_list):    
    f_clicked_toggle = None
    
    try:
        from streamlit_toggle import st_toggle_switch
        # TOGGLE SWITCH FOR f_clicked
        f_clicked_toggle = st_toggle_switch(
            label="Enable f-clicked?",
            key="switch_1",
            default_value=False,
            label_after=False,
            inactive_color="#D3D3D3",  # optional
            active_color="#11567f",  # optional
            track_color="#29B5E8",  # optional
        )
    except:
        logging.warning('Toggle Switch in not available')    
    
    catalog_list.append("Add New Catalog")
    
    # GET AFFILIATE PARTNER FROM DB
    affiliate_partner_list = []
    affiliate_partners = Affiliate_Partner().fetch_records()        
    for affiliate_partner in affiliate_partners:
        affiliate_partner_list.append(affiliate_partner['key'])
    
    affiliate_partner_list.append("Add New Partner")
    
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    
    name = st.text_input(label='Item Name', key='item_name', placeholder='Name', label_visibility='collapsed')
    if(regex.search(name) == None):
        pass
    else:
        st.warning(f"Special characters are not allowed in the name section: {name}")
        st.stop()
        
    description = st.text_area(label='Item Description', height=50, key='description', placeholder='Description',label_visibility='collapsed')    
    affiliate_link = st.text_input(label='Item Affiliate Link', key='affiliate_link', placeholder='Affiliate Link',label_visibility='collapsed')

    catalog_name = st.selectbox(label="Choose Category or Add New", options=catalog_list[:])
    if "Add New Catalog" == catalog_name:
        catalog_name = st.text_input(label='Add Catalog Name', key='catalog_name', placeholder='Catalog Name', label_visibility='collapsed')    
        
    affiliate_partner = st.selectbox(label="Choose Affiliate Partner or Add New", options=affiliate_partner_list)
    if "Add New Partner" == affiliate_partner:
        affiliate_partner = st.text_input(label='Add Partner Name', key='partner_name', placeholder='Partner Name', label_visibility='collapsed')
        
    if f_clicked_toggle:
        random_num = random.randint(1000, 5000)
        f_clicked_val = st.number_input(label='Num of f_clicked to start', value=random_num, key='f_clicked')
        
    uploaded_file = st.file_uploader("Choose a file")
    st.write('---')
    
    disable_button = True    
    
    if all([uploaded_file, name, description, affiliate_link, catalog_name, affiliate_partner]):
        image_val = uploaded_file.getvalue()
        image_name = uploaded_file.name
        disable_button = False            
    
    if st.button(label='Add a New Item', disabled=disable_button):
        progress_text = "Submitting... Please wait..."
        my_bar = st.progress(0, text=progress_text)
            
        try:
            item_obj.create_item(
                name=name, 
                description=description,
                image_path=image_val,
                image_name=image_name,
                affiliate_link=affiliate_link,
                affiliate_partner=affiliate_partner,
                catalog_names=[catalog_name],
                f_clicked=int(f_clicked_val) if f_clicked_toggle else 0
                )
            
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
                
            st.success(f'Item added into DB: {name}')
        except Exception as e:
            st.error("Something went wrong!")
            logging.error(e)