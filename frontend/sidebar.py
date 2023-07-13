import streamlit as st

from streamlit_option_menu import option_menu

from backend.data.catalog import Catalog

def sidebar() -> str:
    with st.sidebar:            
        catalog_list = get_catalog_list()
        
        sidebar = option_menu(
            menu_title="AI-Picks",
            # menu_title=None,
            options=(catalog_list[::-1])
        )
        
    return sidebar

def get_catalog_list() -> list:
    catalogs = Catalog().fetch_records()
    catalog_list = []
    for catalog in catalogs:
        catalog_list.append(catalog['name'])
        
    return catalog_list
