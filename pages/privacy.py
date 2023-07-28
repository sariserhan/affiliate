import streamlit as st

from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page

hide_pages(["admin", "unsubscribe"])

with st.form("privacy"):
    st.subheader("PRIVACY")
    
    st.write("""
                Effective Date: [07/28/2023]

                [Your Company Name] ("we," "us," "our") operates [aibestgoods.com] (the "AIBestGood"). This Privacy Policy informs you of our policies regarding the collection, use, and disclosure of Personal Information we receive from users of the Website.

                By using the Website, you agree to the collection and use of information in accordance with this Privacy Policy.

                Information Collection and Use
                (a) Personal Information: While using our Website, we may ask you to provide certain personally identifiable information ("Personal Information") that can be used to contact or identify you. Personal Information may include but is not limited to your name, email address, postal address, and phone number.

                (b) Log Data: Like many website operators, we collect information that your browser sends whenever you visit our Website ("Log Data"). This Log Data may include information such as your computer's Internet Protocol ("IP") address, browser type, browser version, the pages of our Website that you visit, the time and date of your visit, the time spent on those pages, and other statistics.

                Cookies
                (a) Cookies are files with a small amount of data, which may include an anonymous unique identifier. Cookies are sent to your browser from a website and stored on your computer's hard drive.

                (b) We use "cookies" to collect information. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some portions of our Website.

                Use of Personal Information
                (a) We may use your Personal Information to:
                - Provide, maintain, and improve our Website.
                - Respond to your comments, questions, and requests.
                - Send you administrative information, such as updates and notifications.
                - Send you promotional and marketing materials.
                - Monitor and analyze usage patterns and trends.
                
                (b) We will not share your Personal Information with third parties except as described in this Privacy Policy.

                Data Security
                (a) The security of your Personal Information is important to us. While we strive to use commercially acceptable means to protect your Personal Information, we cannot guarantee its absolute security.

                (b) We will make reasonable efforts to notify you in case of a data breach if required by applicable law.

                Third-Party Services
                (a) Our Website may contain links to third-party websites or services that are not operated by us. Please be aware that we have no control over the content and practices of these third-party sites.

                (b) We encourage you to review the privacy policies of any third-party sites you visit.

                Children's Privacy
                Our Website does not address anyone under the age of 13 ("Children"). We do not knowingly collect personally identifiable information from children under 13. If you are a parent or guardian and you are aware that your Children have provided us with Personal Information, please contact us. If we discover that a Child under 13 has provided us with Personal Information, we will take steps to remove such information from our servers.

                Changes to This Privacy Policy
                (a) This Privacy Policy is effective as of the date stated at the beginning of this document.

                (b) We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page. You are advised to review this Privacy Policy periodically for any changes.

                Contact Us
                If you have any questions or concerns about this Privacy Policy, please contact us at [serhan.sari83@gmail.com].
             """, unsafe_allow_html=True)
    
    if st.form_submit_button("Home"):
        switch_page("app")