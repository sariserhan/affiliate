import streamlit as st

from pathlib import Path
from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page
from frontend.footer import get_footer
from frontend.utils.utils import local_css

hide_pages(["admin", "unsubscribe", "app", "term-conditions", "privacy"])

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / '../styles' / 'main.css'
local_css(css_file)

with st.form('terms_and_conditions'):
    
    # HIDE SIDE BAR
    st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                display: none
            }

            [data-testid="collapsedControl"] {
                display: none
            }
            </style>
            """, unsafe_allow_html=True
            )


    st.subheader('TERMS AND CONDITIONS')
    st.write("""            

                These Terms and Conditions ("Terms") govern your use of [aibestgoods.com] (the "AIBestGoods"), operated by [USCapita LLC] ("we," "us," "our").

                By accessing and using the Website, you acknowledge that you have read, understood, and agree to be bound by these Terms. If you do not agree to these Terms, please refrain from using the Website.

                Content and Intellectual Property
                (a) All content provided on the Website, including but not limited to text, graphics, images, logos, videos, and software, is the property of [USCapita LLC] or its licensors and protected by intellectual property laws.

                (b) You may not copy, modify, reproduce, distribute, or create derivative works based on the content of the Website without our explicit written consent.

                User Conduct
                (a) You agree not to use the Website for any illegal, harmful, or malicious purposes.

                (b) You must not upload or transmit any content that is infringing, defamatory, obscene, or violates the rights of any third party.

                (c) Unauthorized access to restricted areas of the Website is strictly prohibited.

                Disclaimer
                (a) The information and content on the Website are provided "as is" without any warranties, express or implied.

                (b) We do not guarantee the accuracy, completeness, or reliability of the information presented on the Website.

                (c) Your use of any information or materials on the Website is at your own risk. We shall not be liable for any damages arising from your use of the Website.

                Third-Party Websites and Links
                (a) The Website may contain links to third-party websites or resources. We do not endorse and are not responsible for the content, products, or services offered by third parties.

                (b) Your interactions with any third-party websites are governed by their respective terms and policies. Please review them before proceeding.

                Privacy Policy
                (a) Your privacy is important to us. Please review our Privacy Policy [provide link] to understand how we collect, use, and protect your personal information.

                Changes to the Terms and Conditions
                (a) We reserve the right to modify or update these Terms at any time without prior notice.

                (b) Your continued use of the Website after the changes constitute your acceptance of the revised Terms.

                Governing Law and Jurisdiction
                (a) These Terms shall be governed by and construed in accordance with the laws of [USA/Maryland].

                (b) Any disputes arising from or related to these Terms shall be subject to the exclusive jurisdiction of the courts in [USA/Maryland].

                Contact Us
                If you have any questions or concerns regarding these Terms and Conditions, please contact us at [serhan.sari83@gmail.com].
            
         """, unsafe_allow_html=True)

    if st.form_submit_button('Home'):
        try:
            switch_page("home")
        except Exception:
            switch_page("app")

get_footer()