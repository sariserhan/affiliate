import logging
import streamlit as st
import webbrowser

from io import BytesIO
from PIL import Image

from streamlit_extras.buy_me_a_coffee import button
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key
from streamlit_extras.mention import mention
from streamlit_extras.app_logo import add_logo
from streamlit_extras.colored_header import colored_header
from st_pages import Page, hide_pages, show_pages

from frontend.footer import footer
from frontend.sidebar import sidebar
from frontend.subscription import subscription
from backend.data.item import Item

# Disable DEBUG level logging for the PIL module
logging.getLogger("PIL").setLevel(logging.INFO)


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

add_logo("http://placekitten.com/140/120", height=100)


def number_to_words(number):
    words = [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    return " ".join(words[int(i)] for i in str(number))

# --- CATALOG SIDE BAR
selected_catalog = sidebar()

# --- POST LIST
col1, col2 = st.columns([0.7,0.3], gap="small")

with col1:
        # --- HEADER
        colored_header(
            label=f'Best products AI thinks - {selected_catalog}',
            description="We asked AI and here are the ones it thinks are the best!",
            color_name="red-70",
        )
        
        # --- ITEM LIST
        items = Item().get_record_by_catalog(catalog=selected_catalog)
        for item_index, item in enumerate(items, start=1):
            item_key = item["key"]
            name = item["name"]
            url = item['affiliate_link']
            description = item['description']
            image_name = item['image_name']
            
            with st.form(f'{name}_form', clear_on_submit=False):

                st.subheader(name)
                
                # --- ADD keyboard to URL
                number = number_to_words(item_index)
                keyboard_to_url(key=str(item_index), url=url)
                
                # --- ADD mentions to the text         
                inline_mention = mention(
                    label=f"**_Visit Site:_ :red[{name}]**",
                    icon=":arrow_right:",
                    url=item['affiliate_link'],
                    write=False
                )
                            
                # --- IMAGE
                image_data = Item().get_image_data(name=image_name, catalog=selected_catalog)
                image = Image.open(BytesIO(image_data))
                st.image(image=image, caption=item['name'], width=400)               
                
                # --- URL AND KEYBOARD TO URL
                st.write(
                    f'{inline_mention} or hit {key(number, False)} on your keyboard...!',
                    unsafe_allow_html=True,
                )     
                
                # --- DESCRIPTION
                st.markdown(description)
                
                # --- COUNTER
                if name not in st.session_state:
                    st.session_state.name = item['clicked'] + item['f_clicked']
                    
                counter_text = st.empty()
                counter_text.markdown(f'**:red[{st.session_state.name}]** times visited!', unsafe_allow_html=True)                             
                
                # CHECK PRICE BUTTON
                form_button = st.form_submit_button(label="Check Price")
                
                if form_button:
                    st.session_state.name += 1
                    Item().change_record(key=item_key, updates={'clicked':st.session_state.name})                    
                                        
                    # Update the counter text on the page
                    counter_text.markdown(f"**:red[{st.session_state.name}]** times visited!")
                    webbrowser.open_new_tab(url)
                
    
# --- EMAIL SUBSCRIPTION
        subscription()
        
    
# --- ADVERTISEMENT
with col2:
    st.header('Google Adsense')
    # st_lottie("https://lottie.host/8a1ba2d6-ce90-4731-a8df-39aa09d15db2/3bgWuyOp4z.json")
    

# --- BUY ME A COFFEE
    button(username="serhansari", floating=True, width=221)
    
# --- FOOTER 
    footer()