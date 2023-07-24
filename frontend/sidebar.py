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
    
    #Add All Items into Catalog and make it default
    catalog_list.insert(0, 'Best Picks')
    catalog_list.insert(0, 'All Items')
        
    return catalog_list
