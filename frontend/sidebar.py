import streamlit as st

from streamlit_option_menu import option_menu

from backend.data.catalog import Catalog

def sidebar() -> str:
    with st.sidebar:
        catalog_list = get_catalog_list()
        
        sidebar = option_menu(
            menu_title=None,
            options=(catalog_list)
        )
    
    return sidebar

@st.cache_data
def get_catalog_list(catalogs=Catalog().fetch_records()) -> list:
    catalog_list = []
    for catalog in catalogs:
        if catalog['is_active']:
            catalog_list.append(catalog['name'])
    
    # Make default Catalog
    default_catalog = 'Camera'
    for index, catalog in enumerate(catalog_list):
        if catalog == default_catalog:
            catalog_list[0], catalog_list[index] = catalog_list[index], catalog_list[0]
            break
        
    return catalog_list
