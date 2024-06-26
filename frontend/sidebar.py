import streamlit as st
from streamlit_option_menu import option_menu

from backend.data.category import Category


def get_sidebar() -> str:
    with st.sidebar:
        categories = Category().fetch_records()
        category_list = [
            category['name'] for category in categories if category['is_active']
        ]

        options_list = [
            'All Items',
            'Ask AI',
            'Compare Items with AI',
            'Best Picks',
            'Most Viewed',
            'Pros & Cons',
        ]

        options_list.extend(category_list)

        return option_menu(
            menu_title=None,
            options=options_list,
            icons=[
                "list-stars",
                "question-square",
                "arrow-left-right",
                "star",
                "bookmark-star",
                "yin-yang",
            ],
        )


@st.cache_data(show_spinner='Loading...')
def get_catalog_sidebar(category: str):
    category_key = category.replace(' ', '_')
    return Category().get_record(category_key)['catalog_list']
