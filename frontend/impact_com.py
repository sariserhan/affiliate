import os
import logging
import streamlit as st

from .index_html_head import index_html_add_to_head
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def impact_setup():
    
    # --- IMPACT.COM SETUP
    impact_id = os.getenv("IMPACT_ID")
    
    impact_script = f"\n<meta name='ir-site-verification-token' value='{impact_id}'>"                                                            
    return index_html_add_to_head(context='impact', add_head=impact_script, add_body='')