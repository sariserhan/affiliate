import os
import logging
import streamlit as st

from .index_html import index_html_add_to_head, alter_index_html
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def google_analytics_setup():
    
    # --- GOOGLE ANALYTICS SETUP
    google_tag_id = os.getenv("GOOGLE_ANALYTICS_TAG_ID")

    beginning = f'''\n<!-- Google Analytics tracking code -->\n<script async src="https://www.googletagmanager.com/gtag/js?id={google_tag_id}"></script>'''
    middle = "<script>window.dataLayer = window.dataLayer || [];function gtag(){dataLayer.push(arguments);}gtag('js', new Date());"
    end = f"gtag('config', '{google_tag_id}'); </script>\n"

    google_anayltics_script = beginning + middle + end
    
    # --- Change Title in index.html
    alter_index_html('<title>Streamlit', '<title>AIBestGoods')
        
    return index_html_add_to_head(context='analytics', add_head=google_anayltics_script)

