import streamlit as st

from streamlit_option_menu import option_menu
from backend.data.catalog import Catalog


def sidebar():
    with st.sidebar:
        catalogs = Catalog().fetch_records()
        catalog_list = []
        for catalog in catalogs:
            catalog_list.append(catalog['name'])
        
        selected = option_menu(
            menu_title="Best Ones by AI",
            # menu_title=None,
            options=(catalog_list[::-1])
        )
        
    return selected