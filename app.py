import logging
import os
from pathlib import Path

import streamlit as st
import streamlit_analytics
from dotenv import load_dotenv
from PIL import Image
from st_pages import Page, hide_pages, show_pages
from streamlit_extras.app_logo import add_logo
from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.colored_header import colored_header
from streamlit_option_menu import option_menu
from streamlit_toggle import st_toggle_switch

from backend.data.item import Item
from frontend.all_and_best_items import all_and_best_items
from frontend.ask_ai import ask_ai_page
from frontend.column_setup import set_form
from frontend.compare_items import compare_items
from frontend.footer import get_footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.utils.ads import get_ads
from frontend.utils.google_adsense import google_adsense_setup
from frontend.utils.google_analytics import google_analytics_setup
from frontend.utils.impact_com import impact_setup
from frontend.utils.settings import disable_theme_switch
from frontend.utils.theme import set_theme
from frontend.utils.utils import local_css

from backend.data.category import Category

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)
logging.getLogger('fsevents').setLevel(logging.WARNING)


def init():
    # --- PATH SETTINGS
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    icon_file = current_dir / 'assets' / 'icon.png'
    logo_file = current_dir / 'assets' / 'logo.png'
    css_file = current_dir / 'styles' / 'main.css'
    toggle_icon_file = current_dir / 'assets' / 'toggle_icon.png'
    
    # --- ICON
    icon = Image.open(icon_file)
    
    if "state_dict" not in st.session_state:
        st.session_state.state_dict = {}
        
    # --- NAVIGATION BAR
    st.set_page_config(
        layout='wide',
        page_icon=icon,
        page_title="AIBestGoods"
    )
    
    # --- IMPACT.COM SETUP
    # impact_setup()

    # --- GOOGLE ADSENSE SETUP
    google_adsense_setup()

    # --- GOOGLE ANALYTICS SETUP
    google_analytics_setup()

    # --- MAKE PAGES & HIDE
    show_pages(
        [
            Page("app.py", "home"),
            Page("pages/unsubscribe.py", "unsubscribe"),
            Page("pages/admin.py", "admin"),
            Page("pages/privacy.py", "privacy"),
            Page("pages/terms-conditions.py", "terms and conditions")
        ]
    )
    hide_pages(["admin", "home", "unsubscribe", "privacy", "terms and conditions", "app", "terms-conditions"])

    # --- CSS 
    local_css(css_file)
    
    # hidden div with anchor
    st.markdown("<div id='linkto_top'></div>", unsafe_allow_html=True)
    
    # --- LOGO
    add_logo(logo_file.as_posix(), height=100)
  
    streamlit_analytics.start_tracking()
    
    if not disable_theme_switch:
        dark_mode = st_toggle_switch(
            label="\U0001F317",
            key="theme_switch",
            default_value=False,
            label_after=False,
            inactive_color="#D3D3D3",  # optional
            active_color="#11567f",  # optional
            track_color="#29B5E8",  # optional
        )
    
        set_theme(dark_mode)
    
    # --- HEADER
    colored_header(
        label='AI-Powered :mechanical_arm: Picks: Unleashing the Future of Smart Shopping :zap:',
        description="""
                        Our recommendation engine analyzes data and trends for informed choices. Experience the future of intelligent shopping with AI-BestGoods.
                    """,
        color_name="red-70"
    )
    
    # Create the floating button
    st.markdown("<a href='#linkto_top' class='floating-button-right'>:arrow_up:</a>", unsafe_allow_html=True)
    st.markdown("<a class='floating-button-left'>:nazar_amulet:</a>", unsafe_allow_html=True)


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
        ask_ai_page()
        logging.info("-------- ASK AI SELECTED ----------")
        st.write("""
                 <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4959375849193463"
                    crossorigin="anonymous"></script>
                <ins class="adsbygoogle"
                    style="display:block; text-align:center;"
                    data-ad-layout="in-article"
                    data-ad-format="fluid"
                    data-ad-client="ca-pub-4959375849193463"
                    data-ad-slot="4920781155"></ins>
                <script>
                    (adsbygoogle = window.adsbygoogle || []).push({});
                </script>                                  
                 """, unsafe_allow_html=True)
    
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
        category_key = selected_catalog.replace(' ','_')
        category = Category().get_record(category_key)
        
        catalog_sidebar = sidebar(category['catalog_list'])
        
        if catalog_sidebar:
        
            items = Item().get_record_by_catalog(catalog=catalog_sidebar)
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
        
    # --- FOOTER
    _, col2, col3 = st.columns(3)
    with col2:
        get_footer()
    # with col3:
    #     button(username=os.getenv('buy_me_coffee'), floating=True, width=220)
        
    streamlit_analytics.stop_tracking(unsafe_password=os.getenv("STREAMLIT_ANALYTICS"))
    
if __name__ == "__main__":
    init()
    main()
    