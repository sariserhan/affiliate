import os
import logging

import streamlit as st
import streamlit_analytics

from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from st_pages import Page, hide_pages, show_pages

from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.column_setup import set_form
from frontend.google_analytics import google_analytics_setup
from frontend.google_adsense import google_adsense_setup
from backend.data.item import Item

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Disable DEBUG level logging for the PIL module
logging.basicConfig(level=logging.DEBUG)

# --- ICON
icon = Image.open("./assets/icon.png")

# --- NAVIGATION BAR
st.set_page_config(
    layout='wide',
    page_icon=icon,
    page_title="AI-BestGoods"
)

# --- GOOGLE ANALYTICS SETUP
google_analytics_setup()
google_adsense_setup()

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

# --- CATALOG SIDE BAR
selected_catalog = sidebar()

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

# --- POST LIST
col1,col2,col3 = st.columns([4,4,2], gap='small')

# --- ITEM LIST
items = Item().get_record_by_catalog(catalog=selected_catalog)
    
# --- COLUMN-1
with col1:        
    set_form(
        items=items, 
        start=0, end=len(items) // 2, 
        col_name='col1', 
        selected_catalog=selected_catalog
    )
    
# --- COLUMN-2
with col2:
    set_form(
        items=items, 
        start=len(items) // 2,
        end=len(items) if len(items) % 2 == 0 else len(items)-1,
        col_name='col2', 
        selected_catalog=selected_catalog
    )
    
# --- COLUMN-3 for ADS
with col3:
    pass

st.divider()
    
# --- EMAIL SUBSCRIPTION
# subscription()

# --- BUY ME A COFFEE
button(username="serhansari", floating=True, width=221)
    
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
