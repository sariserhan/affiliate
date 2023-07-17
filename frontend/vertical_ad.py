import os
import streamlit as st

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@st.cache_resource
def add_vertical_ad():
    google_adsense_id = os.getenv("GOOGLE_ADSENSE_ID")
    begin = f'''<!-- vertical_ad -->
                <ins class="adsbygoogle"
                    style="display:block"
                    data-ad-client="ca-pub-{google_adsense_id}"
                    data-ad-slot="7465876417"
                    data-ad-format="auto"
                    data-full-width-responsive="true"></ins>
                <script>'''
    end = "(adsbygoogle = window.adsbygoogle || []).push({});</script>"
    print(begin + end)
    return begin + end