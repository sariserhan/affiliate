import os
import logging
import streamlit as st

from .index_html_head import index_html_add_to_head
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def google_adsense_setup():
    
    # --- GOOGLE ADSENSE SETUP
    google_adsense_id = os.getenv("GOOGLE_ADSENSE_ID")
    
    google_adsense_script = f"""\n<!-- Google Adsense tracking code -->\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-{google_adsense_id}"crossorigin="anonymous"></script>
                              """                                                            
    return index_html_add_to_head(context='adsense', add_head=google_adsense_script, add_body='')