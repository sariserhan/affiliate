import streamlit as st

from io import BytesIO
from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.mention import mention
from st_pages import Page, hide_pages, show_pages

from frontend.footer import footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from backend.data.item import Item


# --- NAVIGATION BAR
st.set_page_config(
    layout='wide',
    page_title="Affiliate App",
    page_icon=":books:"
)

show_pages(
    [
        Page("streamlit_app.py", "home"),
        Page("pages/admin.py", "admin")
    ]
)
hide_pages(["admin", "home"])



st.title('BestBuybyAI')
# load_key_css()

# --- CATALOG SIDE BAR
selected = sidebar()

# --- POST LIST
col1, col2 = st.columns([0.7,0.3], gap="small")

mentions_list = []

with col1:        
        st.header(selected)

        # --- ITEM LIST
        items = Item().get_record_by_catalog(catalog=selected)
        for item in items:
            with st.form(f'{item["name"]}_form'):
                                # ADD mentions to the text         
                mentions_list.append(mention(
                    label=item['name'],
                    icon="streamlit",  # Some icons are available... like Streamlit!
                    url=item['affiliate_link'],
                ))
                st.subheader(item['name'])      
            
                # IMAGE
                image_data = Item().get_image_data(name=item['image_name'], catalog=selected)
                image = Image.open(BytesIO(image_data))
                st.image(image=image, caption=item['name'], width=400)
                
                # Item Description
                st.markdown(item['description'])
                

                # st.write(f"check out this [link]({item['link']})")
                
                # --- ADD keyboard to URL
                key = item['name'][0]
                # keyboard_to_url(key=key, url=item['link'])        
                # st.write(
                #    f"""Now hit {key("S", False)} on your keyboard...!""",
                #     unsafe_allow_html=True
                # )
                
                # COUNTER
                count = item['clicked'] + item['f_clicked']

                
                # BUTTON
                st.form_submit_button()
            
            # st.divider()
    
# --- EMAIL SUBSCRIPTION
        subscription()
        
    
# --- ADVERTISEMENT
with col2:
    st.header('Links')
    st.text(mentions_list)
    

# --- BUY ME A COFFEE
    button(username="serhansari", floating=True, width=221)
    
# --- FOOTER 
    footer()