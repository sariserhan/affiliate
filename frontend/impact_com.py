import logging
import os

import streamlit as st
from dotenv import load_dotenv

from .index_html_head import index_html_add_to_head

logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()


@st.cache_resource
def impact_setup():

    # --- IMPACT.COM SETUP
    impact_id = os.getenv("IMPACT_ID")

    impact_script = f"\n<meta name='ir-site-verification-token' value='{impact_id}'>"
    return index_html_add_to_head(context='impact', add_head=impact_script, add_body='')
