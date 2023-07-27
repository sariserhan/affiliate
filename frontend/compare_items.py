import os
import time
import openai

import logging
import streamlit as st

from dotenv import load_dotenv

from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.mention import mention
from streamlit_extras.keyboard_url import keyboard_to_url
from streamlit_extras.keyboard_text import key

from backend.data.catalog import Catalog
from backend.data.item import Item
from frontend.utils.utils import get_image, open_page, get_progress_bar

logging.basicConfig(level=logging.DEBUG)

openai.organization = "org-KAv10qRlhbdtXmwkdkuET5TP"
openai.api_key = os.getenv("OPENAI_API_KEY")
models = openai.Model.list()

load_dotenv()
        
def compare_items(compare: bool = False):    
    catalog_list = [catalog['name'] for catalog in Catalog().fetch_records()]
    selected_catalog = selectbox(label="Choose Category", options=catalog_list)
    items_list = [item['name'] for item in Item().get_record_by_catalog(selected_catalog)]
    compare_form_container = st.empty()
    col1, col2 = st.columns(2)
    
    
    if selected_catalog:
        with col1:
            selected_item_left = selectbox(label='item left', options=items_list, key='item_left', label_visibility='collapsed')
            if selected_item_left:
                with st.form('left'):
                    key_left = selected_item_left.replace(' ','_')                                      
                    item_left = Item().get_record(key_left)                                                                    
                    item_left_image = get_image(item_left['image_name'], selected_catalog)
                    
                    # --- ADD keyboard to URL
                    keyboard_to_url(key=str(1), url=item_left['affiliate_link'])
                    
                    inline_mention_left = mention(
                        label=f"**_Visit Site:_ :green[{item_left['name']}]**",
                        icon=":arrow_right:",
                        url=item_left['affiliate_link'],
                        write=False
                    )
                    
                    st.markdown(f"<h2 class='element'><a href={item_left['affiliate_link']}>{item_left['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_left_image, use_column_width=True, caption=item_left['description'])
                    
                    # --- URL AND KEYBOARD TO URL            
                    st.write(
                        f'{inline_mention_left} or hit {key(":one:", False)} on your keyboard :exclamation:', unsafe_allow_html=True
                    )                        
                    
                    if not compare:
                        st.write('---')
                            
                        pros_left = item_left['pros'].split('.')
                        cons_left = item_left['cons'].split('.')
                        
                        for pros in pros_left:
                            if pros != '':
                                st.write(f':white_check_mark: {pros}')
                            
                        st.write('---')                                                        
                        for cons in cons_left:
                            if cons != '':
                                st.write(f':x: {cons}')                                                                                                 
                    
                    st.write('---')
                    button_row_1, _, button_row_3, _, _ = st.columns([1,0.1,1,0.1,0.1])
                    with button_row_3:
                        button = st.form_submit_button("Check Price", on_click=open_page, args=(item_left['affiliate_link'],))
                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(f'**:green[{item_left["clicked"]+item_left["f_clicked"]}]** times visited :exclamation:', unsafe_allow_html=True)                                    
                    
                        if button:
                            Item().update_record(key=item_left['key'], updates={'clicked':item_left['clicked']+1})
                                
                            # Update the counter text on the page
                            counter_text.markdown(f'**:red[{item_left["clicked"]+item_left["f_clicked"]+1}]** times visited :white_check_mark:')                
                            logging.info(f"{item_left['name']} is clicked by {st.experimental_user.email} --> {item_left['affiliate_link']}")
                
        with col2:                
            selected_item_right = selectbox(label='item right', options=items_list, key='item_right', label_visibility='collapsed')
            if selected_item_right:
                with st.form('right'):
                    key_right = selected_item_right.replace(' ','_')                        
                    item_right= Item().get_record(key_right)
                    item_right_image = get_image(item_right['image_name'], selected_catalog)
                    
                    # --- ADD keyboard to URL
                    keyboard_to_url(key=str(2), url=item_right['affiliate_link'])
                    
                    inline_mention_right = mention(
                        label=f"**_Visit Site:_ :green[{item_right['name']}]**",
                        icon=":arrow_right:",
                        url=item_right['affiliate_link'],
                        write=False
                    )
                    
                    st.markdown(f"<h2 class='element'><a href={item_right['affiliate_link']}>{item_right['name']}</a></h2>", unsafe_allow_html=True)
                    st.write('---')
                    st.image(item_right_image, use_column_width=True, caption=item_right['description'])
                    
                    # --- URL AND KEYBOARD TO URL            
                    st.write(
                        f'{inline_mention_right} or hit {key(":two:", False)} on your keyboard :exclamation:', unsafe_allow_html=True
                    )
                    
                    if not compare:
                        st.write('---')                            
                        pros_right = item_right['pros'].split('.')
                        cons_right = item_right['cons'].split('.')
                        
                        for pros in pros_right:
                            if pros != '':
                                st.write(f':white_check_mark: {pros}')
                            
                        st.write('---')                                                        
                        for cons in cons_right:
                            if cons != '':
                                st.write(f':x: {cons}')                                            
                        
                    st.write('---')
                    button_row_1, _, button_row_3, _, _ = st.columns([1,0.1,1,0.1,0.1])
                    with button_row_3:
                        button = st.form_submit_button("Check Price", on_click=open_page, args=(item_right['affiliate_link'],))                        
                    
                    with button_row_1:
                        counter_text = st.empty()
                        counter_text.markdown(f'**:green[{item_right["clicked"]+item_right["f_clicked"]}]** times visited :exclamation:', unsafe_allow_html=True)                                    
                    
                        if button:
                            Item().update_record(key=item_right['key'], updates={'clicked':item_right['clicked']+1})
                                
                            # Update the counter text on the page
                            counter_text.markdown(f'**:red[{item_right["clicked"]+item_right["f_clicked"]+1}]** times visited :white_check_mark:')                
                            logging.info(f"{item_right['name']} is clicked by {st.experimental_user.email} --> {item_right['affiliate_link']}")
        
        if compare and (selected_item_left and selected_item_right):
            with compare_form_container.form("Compare_with_AI"):
                if st.form_submit_button("Compare items with AI"):
                    if selected_item_right == selected_item_left:
                        st.warning("Please select different items to compare :exclamation:")
                    else:
                        logging.info(models.data[0].id)
                        progress_text = "Searching... Please wait..."
                        my_bar = st.empty()
                        my_bar.progress(0, text=progress_text)
                        
                        # create a chat completion
                        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                                    messages=[{"role": "user", 
                                                                                "content": os.getenv("AI_COMPARE").format(item_left['name'], item_right['name'])
                                                                                }])

                        get_progress_bar(my_bar, progress_text)
                        answer = chat_completion.choices[0].message.content
                        logging.info(f'--------> AI ANSWER:{answer}')
                        st.write(answer)

                