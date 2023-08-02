import os
import streamlit as st

from pathlib import Path
from frontend.utils.utils import get_img_with_href

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_footer():
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    # gmail_file = current_dir / 'assets' / 'gmail.png'
    # twitter_file = current_dir / 'assets' / 'twitter.png'
    # instagram_file = current_dir / 'assets' / 'instagram.png'
    # linkedin_file = current_dir / 'assets' / 'linkedin.png'
    # instagram_icon = get_img_with_href(instagram_file, "Instagram")
    # twitter_icon = get_img_with_href(twitter_file, "Twitter")
    # gmail_icon = get_img_with_href(gmail_file, "Gmail")
    # linkedin_icon = get_img_with_href(linkedin_file, "Linkedin")

    st.markdown(
        """
        <div id="footer">
            <p>                                                 
                © 2023, USCapita LLC. All rights reserved.
                <br>
                <a style="text-decoration: none; filter: invert(50%)" href='https://aibestgoods.com/privacy' target='_blank' rel="noopener,noreferrer">                    
                    Privacy Statement
                </a>              
                <a style="display: inline-block; margin-left: 10px; text-decoration: none; filter: invert(50%)" href='https://aibestgoods.com/terms-conditions' target='_blank' rel="noopener,noreferrer">                    
                    Terms And Conditions
                </a>                
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )                            
       