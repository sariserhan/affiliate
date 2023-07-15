import logging
import streamlit as st

from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from st_pages import Page, hide_pages, show_pages

from frontend.footer import footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.column_setup import set_form
from backend.data.item import Item

# Disable DEBUG level logging for the PIL module
logging.getLogger("PIL").setLevel(logging.INFO)


# --- ICON
icon = Image.open("./assets/icon.png")

# --- NAVIGATION BAR
st.set_page_config(
    layout='wide',
    page_icon=icon,
    page_title="AI-BestGoods"
)

# --- MAKE PAGES & HIDE
show_pages(
    [
        Page("streamlit_app.py", "home"),
        Page("pages/unsubscribe.py", "unsubscribe"),
        Page("pages/admin.py", "admin")
    ]
)
hide_pages(["admin", "home", "unsubscribe"])

# --- CSS 
with open('./styles/main.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- LOGO
add_logo("./assets/logo.png", height=100)

# --- CATALOG SIDE BAR
selected_catalog = sidebar()

# --- HEADER
colored_header(
    label=f'AI-Powered Picks: Unleashing the Future of Smart Shopping!',
    description="""
                    Welcome to AI-BestGoods, where cutting-edge artificial intelligence technology revolutionizes your shopping experience.
                    Powered by state-of-the-art artificial intelligence, we bring you a handpicked collection of the absolute best goods on the market.
                    Our AI-powered recommendation engine analyzes vast amounts of data, user insights, and emerging trends, to deliver recommendations.
                    From cutting-edge technology to trendy fashion and everything in between, AI-BestGoods ensures you make informed choices with confidence. 
                    Experience the future of shopping with AI-BestGoods – where intelligence meets excellence.
                """,
    color_name="red-70",
)

# --- POST LIST
col1,col2,_ = st.columns([4,4,2], gap='small')

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
    
st.divider()
    
# --- EMAIL SUBSCRIPTION
# subscription()

# --- BUY ME A COFFEE
button(username="serhansari", floating=True, width=221)
    
# --- FOOTER 
footer()
