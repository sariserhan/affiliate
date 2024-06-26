import logging

import streamlit as st

from backend.data.catalog import Catalog
from backend.data.category import Category
from backend.data.item import Item
from frontend.utils.add_item import add_item
from frontend.utils.auth import auth
from frontend.utils.delete_item import delete_item
from frontend.utils.send_email import send_email
from frontend.utils.settings import (
    disable_theme_selection_for_user,
    get_db_backup,
    set_default_theme,
)

logging.basicConfig(level=logging.DEBUG)

st.set_page_config(layout='centered')

if "state_dict" not in st.session_state:
    st.session_state.state_dict = {}


# --- ADMIN AUTHENTICATION
if auth():
    with st.container():
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Add New Item", "Delete Item", "Send Email", "Settings"])

        catalogs = Catalog().fetch_records()
        catalog_list = [catalog['name'] for catalog in catalogs]

        categories = Category().fetch_records()
        category_list = [category['name'] for category in categories]

        item_obj = Item()

        # --- ADD ITEM
        with tab1:
            add_item(item_obj, catalog_list, category_list)

        # --- DELETE ITEM
        with tab2:
            delete_item(item_obj)

        # --- SEND EMAIL
        with tab3:
            send_email(item_obj, catalog_list)

        # --- WEBSITE-SETTINGS
        with tab4:
            disable_theme_selection_for_user()
            set_default_theme()
            get_db_backup()
