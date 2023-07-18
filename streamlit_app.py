import os
import time
import logging

import streamlit as st
import streamlit_analytics

from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from st_pages import Page, hide_pages, show_pages

from backend.data.item import Item

from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.column_setup import set_form

from frontend.google_analytics import google_analytics_setup
from frontend.google_adsense import google_adsense_setup
from frontend.impact_com import impact_setup
from frontend.vertical_ad import add_vertical_ad

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Disable DEBUG level logging for the PIL module
logging.basicConfig(level=logging.DEBUG)

def init():
    # --- ICON
    icon = Image.open("./assets/icon.png")

    # --- NAVIGATION BAR
    st.set_page_config(
        layout='wide',
        page_icon=icon,
        page_title="AIBestGoods"
    )

    # --- IMPACT.COM SETUP
    impact_setup()

    # --- GOOGLE ADSENSE SETUP
    google_adsense_setup()

    # --- GOOGLE ANALYTICS SETUP
    google_analytics_setup()

    # --- MAKE PAGES & HIDE
    show_pages(
        [
            Page("streamlit_app.py", "home"),
            Page("pages/unsubscribe.py", "unsubscribe"),
            Page("pages/admin.py", "admin"),
            Page("pages/privacy.py", "privacy")
        ]
    )
    hide_pages(["admin", "home", "unsubscribe", "privacy"])

    # --- CSS 
    with open('./styles/main.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # --- LOGO
    add_logo("./assets/logo.png", height=100)

    streamlit_analytics.start_tracking()

    # Retrieve the user agent string using a hidden input element
    user_agent_string = st.experimental_get_query_params().get("user_agent", [""])[0]

    # Detect the device type
    if "Mobile" in user_agent_string:
        logging.info("User accessed by Mobile device!")
    elif "Tablet" in user_agent_string:
        logging.info("User accessed by Tablet device!")
    else:
        logging.info("User accessed by Computer!")
        # --- HEADER
        colored_header(
            label=f'AI-Powered Picks: Unleashing the Future of Smart Shopping!',
            description="""
                            Our recommendation engine analyzes data and trends for informed choices. Experience the future of intelligent shopping with AI-BestGoods.
                        """,
            color_name="red-70",    
            )

def main():
    # --- CATALOG SIDE BAR
    selected_catalog = sidebar()

    # --- ITEM LIST
    items = Item().get_record_by_catalog(catalog=selected_catalog)
    
    # --- POST LIST
    if len(items) % 3 == 0:        
        col1, col2, col3 = st.columns([4,4,4], gap='small')
        col1_start, col1_end = 0, len(items)//3
        col2_start, col2_end = len(items)//3, (len(items)//3)*2
        col3_start, col3_end = (len(items)//3)*2, len(items)
    elif len(items) % 2 == 0:
        _, col1, col2, _ = st.columns([0.3,4,4,0.3], gap='large')
        col1_start, col1_end = 0, len(items)//2
        col2_start, col2_end = len(items)//2, len(items)
        col3 = None
    else:
        if len(items) == 1:
            col1 = st.columns(1)
            col1_start, col1_end = 0, len(items)
            col2 = None
            col3 = None
        elif len(items) == 5:
            col1, col2 = st.columns([4,4], gap='small')
            col1_start, col1_end = 0, 3
            col2_start, col2_end = 3, len(items)
            col3 = None
        elif len(items) == 7:
            col1, col2, col3 = st.columns([4,4,4], gap='small')
            col1_start, col1_end = 0, 3
            col2_start, col2_end = 3, 6
            col3_start, col3_end = 6, len(items)
        else:
            logging.warning(f'This should not happen: {len(items)}')
    
    # --- COLUMN-1
    with col1:        
        set_form(
            items=items, 
            start=col1_start, 
            end=col1_end, 
            col_name='col1', 
            selected_catalog=selected_catalog
        )
        
    # --- COLUMN-2
    if col2:
        with col2:
            set_form(
                items=items, 
                start=col2_start,
                end=col2_end,
                col_name='col2', 
                selected_catalog=selected_catalog
            )
        
    # --- COLUMN-3
    if col3:
        with col3:        
            set_form(
                items=items, 
                start=col3_start,
                end=col3_end,
                col_name='col3', 
                selected_catalog=selected_catalog
            )
        

    st.divider()
        
    # --- EMAIL SUBSCRIPTION
    # subscription()

    # --- BUY ME A COFFEE
    button(username=os.getenv("buy_me_coffee"), floating=False, width=220)
        
    # --- FOOTER
    st.write(
        """
        <div id="footer"> 
            <p>
                © 2023 AI-BestGoods. All rights reserved. 
                <a href='https://www.instagram.com/serhansari/' target='_blank'>@serhansari</a>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    streamlit_analytics.stop_tracking(unsafe_password=os.getenv("STREAMLIT_ANALYTICS"))
    
    
if __name__ == "__main__":
    init()
    main()
