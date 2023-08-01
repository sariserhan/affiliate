import streamlit as st

from streamlit_option_menu import option_menu

from backend.data.catalog import Catalog

def sidebar() -> str:
    with st.sidebar:
        catalog_list = get_catalog_list()
        
        sidebar = option_menu(
            menu_title=None,
            options=(catalog_list),
            icons=["list-stars", "question-square", "arrow-left-right", "star", "bookmark-star", "yin-yang"]
        )
    
    return sidebar

@st.cache_data
def get_catalog_list(catalogs=Catalog().fetch_records()) -> list:
    catalog_list = []
    for catalog in catalogs:
        if catalog['is_active']:
            catalog_list.append(catalog['name'])
    
    #Add All Items into Catalog and make it default
    catalog_list.insert(0, 'Pros & Cons')
    catalog_list.insert(0, 'Most Viewed')
    catalog_list.insert(0, 'Best Picks')
    catalog_list.insert(0, 'Compare Items with AI')
    catalog_list.insert(0, 'Ask AI')
    catalog_list.insert(0, 'All Items')
        
    return catalog_list
