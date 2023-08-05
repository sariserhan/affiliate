import streamlit as st
from streamlit_option_menu import option_menu

from backend.data.catalog import Catalog
from backend.data.category import Category
 

def sidebar(catalogs: list = None) -> str:
    if catalogs:
        with st.sidebar:
            
            sidebar = option_menu(
                menu_title=None,
                options=catalogs,
                orientation='horizontal'
            )
            return sidebar
    else:
        with st.sidebar:
            categories = Category().fetch_records()
            category_list = [
                category['name'] for category in categories if category['is_active']
            ]
            main_sidebar = option_menu(
                menu_title=None,
                options=['All Items', 'Ask AI', 'Compare Items with AI', 'Best Picks', 'Most Viewed', 'Pros & Cons']+category_list,
                icons=["list-stars", "question-square", "arrow-left-right", "star", "bookmark-star", "yin-yang"]
            )
            return main_sidebar

# @st.cache_data
# def get_catalog_list(catalogs=Catalog().get_record_by_catalog()) -> list:
#     catalog_list = [
#         catalog['name'] for catalog in catalogs if catalog['is_active']
#     ]

#     return catalog_list
