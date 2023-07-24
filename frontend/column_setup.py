import logging
import base64
import streamlit as st

from io import BytesIO
from PIL import Image

from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key
from streamlit_extras.mention import mention
from streamlit.components.v1 import html

from backend.data.item import Item

logging.basicConfig(level=logging.DEBUG)


def number_to_words(number):
    words = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    return " ".join(words[int(i)] for i in str(number))

@st.cache_data(show_spinner=False)
def get_image(image_name, selected_catalog, resize = None):
    image_data = Item().get_image_data(name=image_name, catalog=selected_catalog)
    image = Image.open(BytesIO(image_data))
    if resize:
        return image.resize((resize[0], resize[1]), Image.ANTIALIAS)
    return image

# Function to convert image to base64 encoding
def pil_image_to_base64(image):
    img_buffer = BytesIO()
    image.save(img_buffer, format="PNG")  # You can change the format to JPEG if needed
    return base64.b64encode(img_buffer.getvalue()).decode()

# Navigates in the new page
def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script> 
    """ % (url)
    html(open_script, height=0)
    
# Navigates in the same page
def nav_to(url): 
    nav_script = """
                    <meta http-equiv="refresh" content="0; url='%s'" target="_blank">                    
                 """ % (url)
    st.write(nav_script, unsafe_allow_html=True)

def set_form(items:dict, start: int, end:int, col_name: str, selected_catalog: str):
    for item_index in range(start, end):
        item_key = items[item_index]["key"]
        name = items[item_index]["name"]
        url = items[item_index]['affiliate_link']
        description = items[item_index]['description']
        image_name = items[item_index]['image_name']
        clicked = items[item_index]["clicked"]
        f_clicked = items[item_index]["f_clicked"]
        viewed = clicked + f_clicked
        
        with st.form(f'{name}_{col_name}', clear_on_submit=False):  
            
            # --- SUB-HEADER  
            st.markdown(f"<h2 class='element'><a href={url}>{name}</a></h2>", unsafe_allow_html=True)
            st.write('---')
            
            # --- ADD keyboard to URL
            number = number_to_words(item_index)
            keyboard_to_url(key=str(item_index+1), url=url)
            
            # --- ADD mentions to the text         
            inline_mention = mention(
                label=f"**_Visit Site:_ :green[{name}]**",
                icon=":arrow_right:",
                url=url,
                write=False
            )
            
            # -------------------------------------
            # THIS IS FOR AD
            # --- ADD mentions to the text for ad..
            # inline_ad_mention = mention(
            #     label="but don't click :red[THIS]",
            #     icon=':exclamation:',
            #     url="https://www.google.com",
            #     write=False
            # )
            # NOTE: Add ad link here
            # keyboard_to_url(key="a", url="https://www.google.com")            
            # st.write(
            #     f'{inline_mention} or hit {key(number, False)} on your keyboard {inline_ad_mention} nor hit {key(":a:", False)} :exclamation:',
            #     unsafe_allow_html=True,
            # )     
            # -------------------------------------                       

            # --- IMAGE
            try:
                image = get_image(image_name, selected_catalog)
                st.image(image=image, caption=name, use_column_width=True)
            except Exception as e:
                logging.error(f'Error for item: {name} ---> {e}')
            
            # --- DESCRIPTION
            st.markdown(description)
            
             # --- URL AND KEYBOARD TO URL            
            st.write(
                f'{inline_mention} or hit {key(number, False)} on your keyboard', unsafe_allow_html=True
            )
                                        
            # CHECK PRICE BUTTON
            counter_text = st.empty()
            counter_text.markdown(f'**:green[{viewed}]** times visited :exclamation:', unsafe_allow_html=True)   
            
            if st.form_submit_button(label='Check Price', on_click=open_page, args=(url,)):
                Item().update_record(key=item_key, updates={'clicked':clicked+1})
                                
                # Update the counter text on the page
                counter_text.markdown(f"**:red[{viewed+1}]** times visited :white_check_mark:")                
                logging.info(f"{name} is clicked by {st.experimental_user.email} --> {url}")
