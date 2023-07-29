import os
import streamlit as st

from pathlib import Path
from frontend.utils.utils import get_img_with_href

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_footer():
    current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
    gmail_file = current_dir / 'assets' / 'gmail.png'
    twitter_file = current_dir / 'assets' / 'twitter.png'
    instagram_file = current_dir / 'assets' / 'instagram.png'
    linkedin_file = current_dir / 'assets' / 'linkedin.png'
    instagram_icon = get_img_with_href(instagram_file, "Instagram")
    twitter_icon = get_img_with_href(twitter_file, "Twitter")
    gmail_icon = get_img_with_href(gmail_file, "Gmail")
    linkedin_icon = get_img_with_href(linkedin_file, "Linkedin")
    
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
                <a href='https:/linkedin.com/in/{os.getenv("buy_me_coffee")}/?locale=en_US' target='_blank' rel="noopener noreferrer">                    
                    {linkedin_icon}
                </a>                
                <a href = "mailto: serhan.sari83@gmail.com">                    
                    {gmail_icon}
                </a>           
                <br>                             
                © 2023, USCapita LLC. All rights reserved.  
                <br>
                <a style="text-decoration: none; filter: invert(50%)" href='https:/aibestgoods.com/privacy' target='_blank' rel="related">                    
                    Privacy Statement
                </a>              
                <a style="display: inline-block; margin-left: 10px; text-decoration: none; filter: invert(50%)" href='https:/aibestgoods.com/terms-conditions' target='_blank' rel="related">                    
                    Terms And Conditions
                </a>                      
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )                            
       