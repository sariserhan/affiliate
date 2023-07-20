import logging
import streamlit as st

from io import BytesIO
from PIL import Image
from bokeh.models.widgets import Div

from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key
from streamlit_extras.mention import mention

from backend.data.item import Item

logging.basicConfig(level=logging.DEBUG)


def number_to_words(number):
    words = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    return " ".join(words[int(i)] for i in str(number))

@st.cache_data(show_spinner=False)
def get_image(image_name, selected_catalog):
    image_data = Item().get_image_data(name=image_name, catalog=selected_catalog)
    return Image.open(BytesIO(image_data))

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
            st.markdown(f"<h2 style='text-align: center;'>{name}</h2>", unsafe_allow_html=True)
            
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
            # --- URL AND KEYBOARD TO URL
            st.write(
                f'{inline_mention} or hit {key(number, False)} on your keyboard', unsafe_allow_html=True
            )
                        
            # --- IMAGE
            try:
                image = get_image(image_name, selected_catalog)
                st.image(image=image, caption=name, use_column_width=True)
            except Exception as e:
                logging.error(f'Error for item: {name} ---> {e}')
            
            # --- DESCRIPTION
            st.markdown(description)
                                        
            col1, col2 = st.columns([1,2.5])
            
            with col2:
                counter_text = st.empty()
                counter_text.markdown(f'**:green[{viewed}]** times visited!', unsafe_allow_html=True)          
            
            with col1:
                # CHECK PRICE BUTTON
                form_button = st.form_submit_button(label="Check Price")
            
            if form_button:
                Item().update_record(key=item_key, updates={'clicked':clicked+1})
                                
                with col2:
                    # Update the counter text on the page
                    counter_text.markdown(f"**:red[{viewed+1}]** times visited!")

                js = f"window.open('{url}')"  # New tab or window
                html = '<img src onerror="{}">'.format(js)
                div = Div(text=html)
                st.bokeh_chart(div)
                logging.info(f"{name} is clicked by {st.experimental_user.email}")
                
