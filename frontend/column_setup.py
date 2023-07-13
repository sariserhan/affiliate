import streamlit as st
import webbrowser

from io import BytesIO
from PIL import Image

from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key
from streamlit_extras.mention import mention
from backend.data.item import Item


def number_to_words(number):
    words = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
    return " ".join(words[int(i)] for i in str(number))

def set_form(items:dict, start: int, end:int, col_name: str, selected_catalog: str):
    for item_index in range(start, end):
        item_key = items[item_index]["key"]
        name = items[item_index]["name"]
        url = items[item_index]['affiliate_link']
        description = items[item_index]['description']
        image_name = items[item_index]['image_name']
        clicked = items[item_index]["clicked"]
        f_clicked = items[item_index]["f_clicked"]
        
        with st.form(f'{name}_{col_name}', clear_on_submit=False):            
            # -- SUB-HEADER  
            # st.subheader(name)
            st.markdown(f"<h2 style='text-align: center;'>{name}</h2>", unsafe_allow_html=True)
            
            # st.markdown(link, unsafe_allow_html=True)
            
            # --- ADD keyboard to URL
            number = number_to_words(item_index)
            keyboard_to_url(key=str(item_index), url=url)
            
            # --- ADD mentions to the text         
            inline_mention = mention(
                label=f"**_Visit Site:_ :red[{name}]**",
                icon=":arrow_right:",
                url=url,
                write=False
            )
            
            # --- URL AND KEYBOARD TO URL
            st.write(
                f'{inline_mention} or hit {key(number, False)} on your keyboard...!',
                unsafe_allow_html=True,
            )     
                        
            # --- IMAGE
            image_data = Item().get_image_data(name=image_name, catalog=selected_catalog)
            image = Image.open(BytesIO(image_data))
            st.image(image=image, caption=name, use_column_width=True)               
            
            # --- DESCRIPTION
            st.markdown(description)
            
            # --- COUNTER
            if name not in st.session_state:
                st.session_state.name = clicked+ f_clicked
                
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