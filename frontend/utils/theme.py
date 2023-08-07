import logging

import streamlit as st

logging.basicConfig(level=logging.DEBUG)

theme = {
    "light": {'backgroundColor': "#FFFFFF", 'secondaryBackgroundColor': "#F0F2F6", 'primaryColor': "#FF4B4B", 'textColor': "#31333F"},
    "dark": {'backgroundColor': "#0E1117", 'secondaryBackgroundColor': "#262730", 'primaryColor': "#FF4B4B", 'textColor': "#FAFAFA"}
}


def reconcile_theme_config():
    keys = ['primaryColor', 'backgroundColor',
            'secondaryBackgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        if st.get_option(f'theme.{key}') != st.session_state[key]:
            st._config.set_option(f'theme.{key}', st.session_state[key])
            has_changed = True
    if has_changed:
        st.experimental_rerun()


def set_color(key: str, color: str):
    st.session_state[key] = color


def set_theme(dark_mode: bool):
    if 'primaryColor' not in st.session_state or 'backgroundColor' not in st.session_state or 'secondaryBackgroundColor' not in st.session_state or 'textColor' not in st.session_state:
        set_color('backgroundColor', theme['light']['backgroundColor'])
        set_color('primaryColor', theme['light']['primaryColor'])
        set_color('secondaryBackgroundColor',
                  theme['light']['secondaryBackgroundColor'])
        set_color('textColor', theme['light']['textColor'])

    if dark_mode:
        logging.info(
            "----- Dark Mode Selected ----- session state before:%s ---- current background:%s",
            st.session_state['backgroundColor'],
            st.get_option('theme.backgroundColor')
        )
        set_color('backgroundColor', theme['dark']['backgroundColor'])
        set_color('primaryColor', theme['dark']['primaryColor'])
        set_color('secondaryBackgroundColor',
                  theme['dark']['secondaryBackgroundColor'])
        set_color('textColor', theme['dark']['textColor'])

    else:
        logging.info(
            "----- Light Mode Selected ----- session state before:%s ---- current background:%s",
            st.session_state['backgroundColor'],
            st.get_option('theme.backgroundColor')
        )
        set_color('backgroundColor', theme['light']['backgroundColor'])
        set_color('primaryColor', theme['light']['primaryColor'])
        set_color('secondaryBackgroundColor',
                  theme['light']['secondaryBackgroundColor'])
        set_color('textColor', theme['light']['textColor'])

    reconcile_theme_config()
