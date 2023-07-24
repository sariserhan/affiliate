import os
import base64
import random
import logging

import streamlit as st
import streamlit_analytics

from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.app_logo import add_logo
from streamlit_extras.mention import mention
from streamlit_extras.colored_header import colored_header
from streamlit_toggle import st_toggle_switch

from st_pages import Page, hide_pages, show_pages

from backend.data.item import Item

from frontend.ads import get_ads
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from frontend.column_setup import set_form, get_image, open_page

from frontend.google_analytics import google_analytics_setup
from frontend.google_adsense import google_adsense_setup
from frontend.impact_com import impact_setup

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Disable DEBUG level logging for the PIL module
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
        
    if "is_mobile" not in st.session_state:
        st.session_state.is_mobile = False
        
    st.components.v1.html("""
        <script>
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            const data = JSON.stringify({ isMobile: isMobile });
            const event = new CustomEvent('message', { detail: data });
            parent.document.dispatchEvent(event);
        </script>
    """, height=0)

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
    
    night_mode = st_toggle_switch(
        label=None,
        key="theme_switch",
        default_value=False,
        label_after=False,
        inactive_color="#D3D3D3",  # optional
        active_color="#11567f",  # optional
        track_color="#29B5E8",  # optional
    )
    
    # --- HEADER
    colored_header(
        label='AI-Powered Picks: Unleashing the Future of Smart Shopping:exclamation:',
        description="""
                        Our recommendation engine analyzes data and trends for informed choices. Experience the future of intelligent shopping with AI-BestGoods.
                    """,
        color_name="red-70"
        )
    
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
    
    # --- ITEM LIST
    if selected_catalog == "All Items":
        logging.info("-------- ALL ITEMS SELECTED ----------")


        if not st.session_state.is_mobile:                
            ad_col_left, ad_col_right = st.columns(2)
            
            # Google Adsense
            with ad_col_right:         
                right_ad_on = st_toggle_switch(
                    label=None,
                    key="google_adsense_switch",
                    default_value=False,
                    label_after=False,
                    inactive_color="#D3D3D3",  # optional
                    active_color="#11567f",  # optional
                    track_color="#29B5E8",  # optional
                )
                
            # Amazon Ads
            with ad_col_left:        
                left_ad_on = st_toggle_switch(
                    label=None,
                    key="amazon_ad_switch",
                    default_value=False,
                    label_after=True,
                    inactive_color="#D3D3D3",  # optional
                    active_color="#11567f",  # optional
                    track_color="#29B5E8",  # optional
                )
                
            col1, col2, col3 = st.columns([1,1.8,1])
            items = Item().fetch_records()
            random.shuffle(items)        
            if left_ad_on:
                logging.info(f"Add is turned-off by {st.experimental_user.email}")
                with col1:
                    col1_1, col2_2 = st.columns(2)
                    ads_list = get_ads()
                    for i in range(0, len(ads_list), 4):
                        ads = ads_list[i:i+4]                        
                        if len(ads) != 4:
                            break
                        
                        with col1_1:
                            st.markdown(ads[0], unsafe_allow_html=True)
                            st.markdown(ads[1], unsafe_allow_html=True)                        
                        with col2_2:
                            st.markdown(ads[2], unsafe_allow_html=True)
                            st.markdown(ads[3], unsafe_allow_html=True)                    
                    
            if right_ad_on:
                pass
    
        for item in items:
            logging.info(f"{item['name']} is processing...")
            image = get_image(item['image_name'], item['catalog'])
            item_key = item["key"]
            name = item["name"]
            url = item['affiliate_link']
            description = item['description']
            clicked = item["clicked"]
            f_clicked = item["f_clicked"]
            viewed = clicked + f_clicked
            with col2:
                with st.form(item['name']):
                    st.write(f"<h2 class='element'><a href={url}>{name}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    
                    # --- ADD mentions to the text         
                    inline_mention = mention(
                        label=f"**_Visit Site:_ :green[{name}]**",
                        icon=":arrow_right:",
                        url=url,
                        write=False
                    )
                    st.image(image=image, caption=name, use_column_width=True)
                    st.markdown(description)
                    
                    # --- URL AND KEYBOARD TO URL            
                    st.write(
                        inline_mention, unsafe_allow_html=True
                    )
                    # CHECK PRICE BUTTON
                    counter_text = st.empty()
                    
                    form_button = st.form_submit_button(label='Check Price', on_click=open_page, args=(url,))
                    
                    counter_text.markdown(f'**:green[{viewed}]** times visited :exclamation:', unsafe_allow_html=True)
                    if form_button:
                        Item().update_record(key=item_key, updates={'clicked':clicked+1})
                                        
                        # Update the counter text on the page
                        counter_text.markdown(f"**:red[{viewed+1}]** times visited :white_check_mark:")
                        logging.info(f"{name} is clicked by {st.experimental_user.email} --> {url}")
        
    else:
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
        elif len(items) == 1:
            _, col1, _ = st.columns([0.1,1,0.1])
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
