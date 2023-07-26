import os
import base64
import logging

import streamlit as st
import streamlit_analytics

from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header

from st_pages import Page, hide_pages, show_pages

from backend.data.item import Item

from frontend.ads import get_ads
from frontend.ask_ai import ask_ai
from frontend.compare_items import compare_items
from frontend.all_and_best_items import all_and_best_items
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.column_setup import set_form

from frontend.google_analytics import google_analytics_setup
from frontend.google_adsense import google_adsense_setup
from frontend.impact_com import impact_setup

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.DEBUG)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def get_img_with_href(local_img_path, context, target_url = None):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    if target_url:
        html_code = f'''
                        <a href="{target_url}">
                            <img src="data:image/{img_format};base64,{bin_str}" alt="{context}"/>
                        </a>
                    '''
    else:
        html_code = f'<img src="data:image/{img_format};base64,{bin_str}" alt="{context}" height="25" />'
        
    return html_code

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        

def init():
    # --- ICON
    icon = Image.open("./assets/icon.png")

    # --- NAVIGATION BAR
    st.set_page_config(
        layout='wide',
        page_icon=icon,
        page_title="AIBestGoods"
    )
    
    if "state_dict" not in st.session_state:
        st.session_state.state_dict = {}
    
    # --- IMPACT.COM SETUP
    # impact_setup()

    # --- GOOGLE ADSENSE SETUP
    # google_adsense_setup()

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
    local_css('./styles/main.css')
    
    # --- LOGO
    add_logo("./assets/logo.png", height=100)
  
    streamlit_analytics.start_tracking()
    
    try:
        from streamlit_toggle import st_toggle_switch
        night_mode = st_toggle_switch(
            label=None,
            key="theme_switch",
            default_value=False,
            label_after=False,
            inactive_color="#D3D3D3",  # optional
            active_color="#11567f",  # optional
            track_color="#29B5E8",  # optional
        )
    except:
        logging.info("streamlit_toggle is not available!")
    
    # SET DEFAULT THEME
    config_toml = open('.streamlit/config.toml', 'w')
    config_toml.write('[theme]\nbase="dark"')
    config_toml.close()
    
    # --- HEADER
    colored_header(
        label='AI-Powered Picks: Unleashing the Future of Smart Shopping:exclamation:',
        description="""
                        Our recommendation engine analyzes data and trends for informed choices. Experience the future of intelligent shopping with AI-BestGoods.
                    """,
        color_name="red-70"
        )
    
    # SET THEME FROM TOGGLE
    try:
        config_toml = open('.streamlit/config.toml', 'w')
        if night_mode:        
            config_toml.write('[theme]\nbase="dark"')       
        else:        
            config_toml.write('[theme]\nbase="light"')
    finally:
        config_toml.close()
    
def main():    
    # --- CATALOG SIDE BAR
    selected_catalog = sidebar()
    
    _, col2, _ = st.columns([1,2.5,1])    
    
    # --- ITEM LIST
    if selected_catalog == "All Items":        
        all_and_best_items(col2)
        logging.info("-------- ALL ITEMS SELECTED ----------")
    
    elif selected_catalog == "Compare Items with AI":
        compare_items(compare=True)
        logging.info("-------- COMPARE ITEMS SELECTED ----------")
    
    elif selected_catalog == "Ask AI":
        ask_ai()
        logging.info("-------- ASK AI SELECTED ----------")  
    
    elif selected_catalog == "Pros & Cons":
        compare_items()
        logging.info("-------- PROS & CONS SELECTED ----------")  
        
    elif selected_catalog == "Best Picks":        
        all_and_best_items(col2, is_best_pick=True)
        logging.info("-------- BEST PICKS SELECTED ----------")
        
    elif selected_catalog == 'Most Viewed':
        all_and_best_items(col2, is_most_viewed=True)
        logging.info("-------- MOST VIEWED SELECTED ----------")
        
    else:
        items = Item().get_record_by_catalog(catalog=selected_catalog)
        logging.info(f"-------- CATALOG - {selected_catalog} - SELECTED ----------")
    
        # --- POST LIST
        with col2:        
            set_form(
                items=items,
                col_name='col2', 
                selected_catalog=selected_catalog
            )
            
    st.divider()

    # --- EMAIL SUBSCRIPTION
    subscription()
    st.write('---')

    # --- BUY ME A COFFEE
    button(username=os.getenv("buy_me_coffee"), floating=False, width=220)
        
    # --- FOOTER
    instagram_icon = get_img_with_href("./assets/instagram.png", "Instagram")
    twitter_icon = get_img_with_href("./assets/twitter.png", "Twitter")
    gmail_icon = get_img_with_href("./assets/gmail.png", "Gmail")
    st.markdown(
        f"""
        <div id="footer"> 
            <p>                
                <a href='https://twitter.com/{os.getenv("buy_me_coffee")}_/' target='_blank' rel="noopener noreferrer">                    
                    {twitter_icon}
                </a>   
                <a href='https://www.instagram.com/{os.getenv("buy_me_coffee")}/' target='_blank' rel="noopener noreferrer">                    
                    {instagram_icon}
                </a>                
                <a href = "mailto: serhan.sari83@gmail.com">                    
                    {gmail_icon}
                </a>
            </p>
            © 2023 AIBestGoods. All rights reserved. 
        </div>
        """,
        unsafe_allow_html=True
    )

    streamlit_analytics.stop_tracking(unsafe_password=os.getenv("STREAMLIT_ANALYTICS"))
    
if __name__ == "__main__":
    init()
    main()
