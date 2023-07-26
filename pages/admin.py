import logging
import streamlit as st

from backend.data.item import Item
from backend.data.catalog import Catalog

from frontend.utils.auth import auth
from frontend.utils.add_item import add_item
from frontend.utils.delete_item import delete_item
from frontend.utils.send_email import send_email

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(layout='centered')

if "state_dict" not in st.session_state:
    st.session_state.state_dict = {}
    
# --- ADMIN AUTHENTICATION
if auth():
    with st.container():
        tab1, tab2, tab3 = st.tabs(["Add New Item", "Delete Item", "Send Email"])

        # --- SHARED AREA
        catalog_list = []
        catalogs = Catalog().fetch_records()
        for catalog in catalogs:
            catalog_list.append(catalog['name'])
            
        item_obj = Item()

        # --- ADD ITEM
        with tab1:
            add_item(item_obj, catalog_list)
                        
        # --- DELETE ITEM
        with tab2:
            delete_item(item_obj)
                        
        # --- SEND EMAIL
        with tab3:
            send_email(item_obj, catalog_list)                     
